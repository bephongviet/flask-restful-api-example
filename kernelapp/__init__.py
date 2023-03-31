import logging
from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from kernelapp.extensions import rbac
from kernelapp.extensions import db, login_manager, migrate
from kernelapp.models.user import User
from kernelapp.resources.authentication import AuthenticateResource
from flask import send_from_directory

def create_app(testing=False):
    app = Flask(__name__, instance_relative_config=True)
    if testing:
        app.config.from_object('tests.test_config')
    else:
        app.config.from_pyfile('config.py')
    config = app.config
    app.debug = config.get('DEBUG')
    api = Api(app)
    app.config["SECRET_KEY"] = config.get('SECRET_KEY')
    app.config["JWT_SECRET_KEY"] = config.get('JWT_SECRET_KEY')  # Change this!
    jwt = JWTManager(app)

    # SQL Al-chemy
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}'.format(
        username=config.get('MYSQL_DB_USER'),
        password=config.get('MYSQL_DB_PASS'),
        host=config.get('MYSQL_DB_HOST'),
        port=config.get('MYSQL_DB_PORT'),
        database=config.get('MYSQL_DB_NAME'))
    app.config['SQLALCHEMY_ECHO'] = config.get('SQLALCHEMY_ECHO')
    # init SQLAlchemy
    db.init_app(app)

    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(uuid):
        return User.query.get(uuid)

    # RBAC
    rbac.init_app(app)

    # init Migrate
    migrate.init_app(app, db)

    # declare CORS allowed path and origins
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # logging setup
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s [%(levelname)s] - [%(name)s]: %(message)s',
                        handlers=[logging.StreamHandler()])
    app.logger.debug("App starting...")

    # API resources
    api.add_resource(AuthenticateResource, '/api/authenticate')

    app.logger.debug("App STARTED and RUNNING...")
    return app

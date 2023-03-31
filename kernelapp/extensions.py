from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_rbac import RBAC
rbac = RBAC()

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

TESTING=environ.get('TESTING')
DEBUG=environ.get('DEBUG')
FLASK_ENV=environ.get('FLASK_ENV')
SECRET_KEY=environ.get('SECRET_KEY')
SECRET_KEY=environ.get('JWT_SECRET_KEY')
MYSQL_DB_HOST=environ.get('MYSQL_DB_HOST')
MYSQL_DB_PORT=environ.get('MYSQL_DB_PORT')
MYSQL_DB_USER=environ.get('MYSQL_DB_USER')
MYSQL_DB_PASS=environ.get('MYSQL_DB_PASS')
MYSQL_DB_NAME=environ.get('MYSQL_DB_NAME')
UPLOAD_FOLDER=environ.get('UPLOAD_FOLDER')
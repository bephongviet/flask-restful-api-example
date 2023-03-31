import string
import secrets
import uuid

from flask_login import UserMixin
from flask_rbac import RoleMixin
from kernelapp.extensions import db

class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name, description=None):
        self.name = name
        self.description = description

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String(50), primary_key=True, default=str(uuid.uuid1()))
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean, default=True)

    # Relationship with SocialProfile
    social_profiles = db.relationship("SocialProfile", backref="user", foreign_keys="SocialProfile.user_id", lazy=True)

    # Roles for RBAC
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))

    def __init__(self, username, password, active=True):
        self.username = username
        self.password = password
        self.active = active

    @staticmethod
    def generate_secure_password(length=12):
        """
        Generate a secure random password.

        :param length: The length of the generated password, defaults to 12.
        :type length: int, optional
        :return: A secure random password.
        :rtype: str
        """
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(characters) for _ in range(length))
        return password

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

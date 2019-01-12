from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from market_bucket import db, app
from market_bucket.helpers.helpers import validation_preparation
import re
import datetime
import jwt


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(64),
                           unique=True, nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    description = db.Column(db.Text)
    company_logo = db.Column(db.String())
    marketplaces = db.relationship(
        "Marketplace", backref="users", cascade="delete, delete-orphan")
    images = db.relationship("Image", backref="users", lazy=True,
                             order_by="desc(Image.id)", cascade="delete, delete-orphan")
    products = db.relationship("Product", backref="users",
                             order_by="desc(Product.id)", cascade="delete, delete-orphan")

    def __init__(self, store_name, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.store_name = store_name
        self.set_password(password)

    def __repr__(self):
        return f"{self.store_name} with email {self.email} saved to database!"

    @validates('first_name')
    @validation_preparation
    def validate_first_name(self, key, first_name):
        if not first_name:
            self.validation_errors.append('No First Name provided')

        return first_name

    @validates('last_name')
    @validation_preparation
    def validate_last_name(self, key, last_name):
        if not last_name:
            self.validation_errors.append('No Last Name provided')

        return last_name

    @validates('store_name')
    @validation_preparation
    def validate_store_name(self, key, store_name):
        if not store_name:
            self.validation_errors.append('No Store Name provided')

        if (not self.store_name == store_name):
            if User.query.filter_by(store_name=store_name).first():
                self.validation_errors.append('Store Name is already in use')

        if len(store_name) > 0 and (len(store_name) < 3 or len(store_name) > 50):
            self.validation_errors.append(
                'Store Name must be between 3 and 50 characters')

        return store_name

    @validates('email')
    @validation_preparation
    def validate_email(self, key, email):
        if not email:
            self.validation_errors.append('No email provided')

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.validation_errors.append(
                'Provided email is not an email address')

        if (not self.email == email):
            if User.query.filter_by(email=email).first():
                self.validation_errors.append('Email is already in use')

        return email

    def set_password(self, password):
        if not password:
            self.validation_errors.append('Password not provided')

        if len(password) > 0 and (len(password) < 8 or len(password) > 50):
            self.validation_errors.append(
                'Password must be between 8 and 50 characters')

        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            print(e)
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 0
        except jwt.InvalidTokenError:
            return 0

# -*- coding: utf-8 -*-


"""Database models using SQLAlchemy."""


# Python Standard Library
import datetime
import os
import binascii

# Third Party Modules
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from flask_login import UserMixin
from flask_login import AnonymousUserMixin

# Project specific modules
from api.database import Column
from api.database import Model
from api.database import SurrogatePK
from api.database import Integer
from api.database import ForeignKey
from api.database import db
from api.database import relationship
from api.database import ModelSerializer
from api.settings import Config


def gen_uuid():
    return binascii.hexlify(os.urandom(16)).decode('utf-8')


class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.username = None


class User(UserMixin, SurrogatePK, Model, ModelSerializer):
    """User model."""

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String)
    facebook_id = db.Column(db.String)
    facebook_access_token = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    photo = db.Column(db.String)
    email = db.Column(db.String)
    auth_token = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def generate_auth_token(self, expiration=1000000):
        s = Serializer(Config.SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.uuid})

    def verify_auth_token(token):
        s = Serializer(Config.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.filter_by(uuid=data['uuid']).first()
        return user

    def __init__(self, photo=None, first_name=None, last_name=None,
                 email=None, facebook_id=None, facebook_token=None):
        """ Define what will be loaded up on model instantiation here """
        self.uuid = gen_uuid()
        self.facebook_id = facebook_id
        self.facebook_access_token = facebook_token
        self.photo = photo
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def __repr__(self):
        return '<User {}:{}>'.format(self.uuid, self.username)


class HammockLocation(SurrogatePK, Model, ModelSerializer):
    """Hammock Location model."""

    __tablename__ = 'hammock_location'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String)
    title = db.Column(db.String)
    capacity = db.Column(db.BigInteger)
    photo = db.Column(db.String)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    description = db.Column(db.String)
    user_uuid = Column(Integer, ForeignKey('user.id'))
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    comments = relationship('Comment', back_populates='hammock_location')

    def __init__(self, title=None, capcity=None, photo=None, latitude=None,
                 longitude=None, description=None, user_uuid=None):
        self.uuid = gen_uuid()
        self.title = title
        self.capacity = capcity
        self.photo = photo
        self.latitude = latitude
        self.longitude = longitude
        self.description = description
        self.user_uuid = user_uuid

    def __repr__(self):
        return '<HammockLocation {}:{}>'.format(self.uuid, self.title)


class Comment(SurrogatePK, Model, ModelSerializer):
    """Comment model."""

    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String)
    text = db.Column(db.String)
    user_uuid = Column(Integer, ForeignKey('user.id'))
    location_uuid = Column(Integer, ForeignKey('hammock_location.id'))
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, text=None, user_uuid=None, location_uuid=None):
        self.text = text
        self.user_uuid = user_uuid
        self.location_uuid = location_uuid

    def __repr__(self):
        return '<Comment {}:{}>'.format(self.uuid, self.text)


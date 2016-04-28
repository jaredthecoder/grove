"""documents.py"""


# Python Standard Library
import datetime
import uuid

from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentListField
from mongoengine import GeoPointField, IntField
from mongoengine import StringField, DateTimeField

from api.settings import Config


class Comment(EmbeddedDocument):
    uuid = StringField()
    text = StringField()
    date_created = DateTimeField(default=datetime.datetime.now())
    user_uuid = StringField()
    location_uuid = StringField()

    def to_json(self, *args, **kwargs):
        data = dict()
        data["text"] = self.text
        data["date_created"] = self.date_created.strftime("%Y-%m-%d %H:%M:%S")
        data["user_id"] = self.user_uuid
        data["location_id"] = self.location_uuid
        data["id"] = self.uuid
        return data


class HammockLocation(Document):
    uuid = StringField()
    title = StringField()
    capacity = IntField()
    photo = StringField()
    loc = GeoPointField()
    description = StringField()
    comments = EmbeddedDocumentListField(Comment)
    date_created = DateTimeField(default=datetime.datetime.now())
    user_uuid = StringField()

    def to_json(self, *args, **kwargs):
        data = dict()
        data["title"] = self.title
        data["photo"] = self.photo
        data["capacity"] = self.capacity
        data["description"] = self.description
        encoded_comments = []
        for comment in self.comments:
            encoded_comments.append(comment.to_json())
        data["comments"] = encoded_comments
        data["date_created"] = self.date_created.strftime("%Y-%m-%d %H:%M:%S")
        data["user_id"] = self.user_uuid
        data["id"] = self.uuid
        data["latitude"] = self.loc[0]
        data["longitude"] = self.loc[1]
        return data


class User(Document):
    uuid = StringField()
    facebook_id = StringField()
    facebook_access_token = StringField()
    first_name = StringField()
    last_name = StringField()
    photo = StringField()
    email = StringField()
    auth_token = StringField()
    date_created = DateTimeField(default=datetime.datetime.now())

    def to_json(self, *args, **kwargs):
        data = dict()
        data["date_created"] = self.date_created.strftime("%Y-%m-%d %H:%M:%S")
        data["id"] = self.uuid
        data["first_name"] = self.first_name
        data["last_name"] = self.last_name
        data["photo"] = self.photo
        data["auth_token"] = self.auth_token
        return data

    def generate_auth_token(self, expiration=1000000):
        s = Serializer(Config.SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.uuid})

    def verify_auth_token(token):
        s = Serializer(Config.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.objects(uuid=data['uuid']).first()
        return user

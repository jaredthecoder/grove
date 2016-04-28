"""documents.py"""


# Python Standard Library
import binascii
import datetime
import os

from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentListField
from mongoengine import GeoPointField, IntField
from mongoengine import StringField, DateTimeField


def gen_uuid():
    return binascii.hexlify(os.urandom(16)).decode('utf-8')


class Comment(EmbeddedDocument):
    uuid = StringField(default=gen_uuid())
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
    uuid = StringField(default=gen_uuid())
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
    uuid = StringField(default=gen_uuid())
    auth_token = StringField()
    date_created = DateTimeField(default=datetime.datetime.now())

    def to_json(self, *args, **kwargs):
        data = dict()
        data["date_created"] = self.date_created.strftime("%Y-%m-%d %H:%M:%S")
        data["id"] = self.uuid
        data["auth_token"] = self.auth_token
        return data


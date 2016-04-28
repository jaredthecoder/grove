# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located
in app.py."""

from flask.ext.bcrypt import Bcrypt
from flask.ext.cache import Cache
from flask.ext.mongoengine import MongoEngine

bcrypt = Bcrypt()
cache = Cache()
db = MongoEngine()


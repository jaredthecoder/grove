# -*- coding: utf-8 -*-


"""Extensions module. Each extension is initialized in the app factory located
in app.py."""


# Third-Party modules
from flask.ext.bcrypt import Bcrypt
from flask.ext.cache import Cache
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


bcrypt = Bcrypt()
cache = Cache()
db = SQLAlchemy()
migrate = Migrate()

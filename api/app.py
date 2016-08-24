# -*- coding: utf-8 -*-


"""This file contains the application factory for making instances of the API"""

# Python standard library
import os

# Third-Party modules
from flask import Flask
from flask.ext.restful import Api

# Project specific modules
from api.extensions import bcrypt, cache, db, migrate
from api.settings import ProdConfig


def create_app(config_object=ProdConfig, static_path=''):
    """An application factory for this API."""

    app = Flask(__name__, static_url_path=static_path)

    try:
        app.config.from_object(os.environ['GROVE_SETTINGS'] or config_object)
    except KeyError:
        raise KeyError('GROVE_SETTINGS environment variable is not ' +
                       'declared. Please declare it to point to the ' +
                       'application configs..')

    register_extensions(app)
    register_database(app)
    register_api(app)

    return app


def register_endpoints():
    """Register API endpoints with resources."""

    api = Api()

    from api.resources.RootResource import RootResource
    from api.resources.LocationResource import LocationResource
    from api.resources.FeedResource import FeedResource
    from api.resources.CommentResource import CommentResource
    from api.resources.LoginResource import LoginResource
    from api.resources.LoginResource import FacebookLoginCallbackResource
    from api.resources.UserResource import UserResource

    api.add_resource(LoginResource,
                     '/login/<string:provider_name>',
                     '/login/<string:provider_name>/')
    api.add_resource(UserResource,
                     '/user')
    api.add_resource(FacebookLoginCallbackResource,
                     '/login/<string:provider_name>/callback')
    api.add_resource(RootResource, '/')
    api.add_resource(LocationResource, '/location/<string:location_uuid>',
                     '/location')
    api.add_resource(CommentResource, '/comment/<string:location_uuid>',
                     '/comment')
    api.add_resource(FeedResource, '/feed')

    return api


def register_api(app):
    """Register API endpoints and Flask-RESTful instance."""

    api = register_endpoints()
    api.init_app(app)


def register_database(app):
    """Register database and the migrate command."""

    db.init_app(app)
    migrate.init_app(app)


def register_extensions(app):
    """Register Flask extensions."""

    bcrypt.init_app(app)
    cache.init_app(app)

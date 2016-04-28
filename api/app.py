# -*- coding: utf-8 -*-


import os

from flask import Flask
from flask.ext.restful import Api

from api.extensions import bcrypt, cache, db
from api.settings import ProdConfig


def create_app(config_object=ProdConfig, static_path=''):
    """An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """

    app = Flask(__name__, static_url_path=static_path)
    try:
        app.config.from_object(os.environ['WHERENO_SETTINGS'] or config_object)
    except KeyError:
        raise KeyError('WHERENO_SETTINGS environment variable is not ' +
                       'declared. Please declare it to point to the ' +
                       'application configs..')

    app.config['MONGODB_SETTINGS'] = {
            'db': os.environ.get('MONGODB_DB'),
            'host': os.environ.get('MONGODB_URI')
        }
    register_extensions(app)
    register_mongo(app)
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

    api.add_resource(LoginResource,
                     '/login/<string:provider_name>')
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


def register_mongo(app):
    """Register MongoKit documents."""

    db.init_app(app)


def register_extensions(app):
    """Register Flask extensions."""

    bcrypt.init_app(app)
    cache.init_app(app)

# -*- coding: utf-8 -*-


"""Module containing various utility functions"""


# Python standard libraries
import os
import urllib.request

# Third-Party modules
from flask.ext.restful import abort, current_app
from flask import request

# Project specific modules
from api.models import User


def parse_auth_header(auth_header):
    """Parse the authentication header sent on authenticated requests"""

    if auth_header is None:
        return None
    try:
        auth_type, param_strs = auth_header.split(" ", 1)
        items = urllib.request.parse_http_list(param_strs)
        opts = urllib.request.parse_keqv_list(items)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return None
    return opts


def require_login(func):
    """Decorator function that checks if the current user is logged in"""

    def new_func(*args, **kwargs):
        auth_opts = parse_auth_header(request.headers.get('Authorization'))
        try:
            token = auth_opts['token']
        except (KeyError, TypeError) as e:
            abort(401)
            return
        user = User.query.filter_by(auth_token=token).first()
        if len(user) > 1:
            current_app.logger.error(
                'More than one user with id: {}'.format(token))
            abort(401)
        if user is None or len(user) == 0:
            current_app.logger.error(
                "User for the given authorization token does not exist.")
            abort(401)
            return

        return func(user=user.first(), *args, **kwargs)
    return new_func


# External OAuth Configs
social_config = {
    'facebook': {
        'consumer_key': str(os.environ.get('FB_CONSUMER_KEY')),
        'consumer_secret': str(os.environ.get('FB_CONSUMER_SECRET')),
        'scope': ['public_profile', 'user_friends', 'email'],
    }
}


def abort_not_exist(_id, _type):
    """Abort the request if the entity does not exist."""

    abort(404,
          message="{} {} does not exist. Please try again with a different {}".format(_type, _id, _type))


def abort_cannot_update(_id, _type):
    """Abort the request if the entity cannot be updated."""

    abort(400,
          message="Cannot update {} {}. Please try again.".format(_type, _id))


def abort_cannot_create(_type):
    """Abort the request if the entity cannot be created."""

    abort(400,
          message='Cannot create {} because you have not supplied the proper parameters.'.format(_type))

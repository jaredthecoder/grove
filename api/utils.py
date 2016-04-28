"""utils.py - Module containing various utility functions"""

import urllib.request

from flask.ext.restful import abort
from flask import request

from api.documents import User


def parse_auth_header(auth_header):
    try:
        auth_type, param_strs = auth_header.split(" ", 1)
        items = urllib.request.parse_http_list(param_strs)
        opts = urllib.request.parse_keqv_list(items)
    except:
        import traceback
        traceback.print_exc()
        return None
    return opts


def require_login(func):
    def new_func(*args, **kwargs):
        auth_opts = parse_auth_header(request.headers.get('Authorization'))
        try:
            token = auth_opts['token']
        except KeyError as e:
            abort(401)
            return
        user = User.objects(auth_token=token)
        if len(user) > 1:
            print('More than one user with id: {}'.format(token))
            abort(401)
        if user is None:
            abort(401)
            return

        return func(user=user, *args, **kwargs)
    return new_func


# External OAuth Configs
social_config = {}


def abort_not_exist(_id, _type):
    abort(404,
          message="{} {} does not exist. Please try again with a different {}".format(_type, _id, _type))


def abort_cannot_update(_id, _type):
    abort(400,
          message="Cannot update {} {}. Please try again.".format(_type, _id))


def abort_cannot_create(_type):
    abort(400,
          message='Cannot create {} because you have not supplied the proper parameters.'.format(_type))

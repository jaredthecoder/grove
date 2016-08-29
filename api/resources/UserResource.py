# -*- coding: utf-8 -*-


"""HTTP resources for the comment entities."""


# Third-Party modules
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import current_app

# Project specific modules
from api.models import User
from api.utils import abort_not_exist, require_login


class UserResource(Resource):
    """Class for handling User model API interactions"""

    user_fields = {
        'date_created': fields.DateTime,
        'id': fields.String(attribute='uuid'),
        'email': fields.String,
        'first_name': fields.String,
        'last_name': fields.String,
        'photo': fields.String
    }

    def __init__(self):
        pass

    @marshal_with(user_fields)
    @require_login
    def get(self, user, user_id=None):
        """Get a user based on user_id"""

        current_app.logger.debug(repr(user))

        user = User.query.filter_by(uuid=user_id).first()
        if user is None:
            abort_not_exist(user_id, 'User')

        return user

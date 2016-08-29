# -*- coding: utf-8 -*-


"""HTTP resources for the comment entities."""


# Third-Party modules
from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import current_app

# Project specific modules
from api.models import db, Comment, HammockLocation
from api.utils import abort_not_exist, require_login


class CommentResource(Resource):
    """Class for handling Comment model API interactions"""

    comment_fields = {
        'id': fields.String(attribute='uuid'),
        'text': fields.String,
        'user_id': fields.String(attribute='user_uuid'),
        'location_id': fields.String(attribute='location_uuid'),
        'date_created': fields.DateTime
    }

    def __init__(self):
        self.put_parser = self.setup_put_parser()
        self.post_parser = self.setup_post_parser()

    def setup_post_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('text', type=str)
        parser.add_argument('location_id', required=True, type=str)
        return parser

    def setup_put_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('text', required=True, type=str)
        return parser

    @marshal_with(comment_fields)
    @require_login
    def get(self, user, location_uuid):
        current_app.logger.debug(repr(user))
        location = HammockLocation.query.filter_by(uuid=location_uuid).first()
        if location is None:
            abort_not_exist(location_uuid, 'Location')

        comments = location.comments

        return comments

    @marshal_with(comment_fields)
    @require_login
    def post(self, user):
        current_app.logger.debug(repr(user))
        parsed_args = self.post_parser.parse_args()

        comment = Comment(text=parsed_args['text'],
                          location_uuid=parsed_args['location_id'],
                          user_uuid=user.uuid)

        location = HammockLocation.query.filter_by(
            uuid=parsed_args['location_id']).first()
        location.comments.append(comment)

        db.session.add(comment)
        db.session.add(location)
        db.session.commit()

        return comment

    @marshal_with(comment_fields)
    @require_login
    def put(self, user, comment_id=None):
        current_app.logger.debug(repr(user))
        parsed_args = self.put_parser.parse_args()

        comment = Comment.query.filter_by(uuid=comment_id).first()
        if comment is None:
            abort_not_exist(comment_id, 'Comment')

        comment.text = parsed_args['text']

        db.session.add(user)
        db.session.commit()

        return comment

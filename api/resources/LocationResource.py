# -*- coding: utf-8 -*-


"""HTTP resources for the hammock location entities."""


# Third-Party modules
from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import current_app

# Project specific modules
from api.models import db, Comment, HammockLocation
from api.utils import abort_not_exist, require_login


class LocationResource(Resource):
    """Class for handling HammockLocation model API interactions"""

    comment_fields = {
        'id': fields.String(attribute='uuid'),
        'text': fields.String,
        'user_id': fields.String(attribute='user_uuid'),
        'location_id': fields.String(attribute='location_uuid'),
        'date_created': fields.DateTime
    }

    loc_fields = {
        'id': fields.String(attribute='uuid'),
        'user_id': fields.String(attribute='user_uuid'),
        'title': fields.String,
        'capacity': fields.String,
        'description': fields.String,
        'latitude': fields.Float,
        'longitude': fields.Float,
        'date_created': fields.DateTime,
        'comments': fields.List(fields.Nested(comment_fields))
    }

    def __init__(self):
        self.put_parser = self.setup_put_parser()
        self.post_parser = self.setup_post_parser()

    def setup_post_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', default=None, type=str)
        parser.add_argument('capacity', default=None, type=int)
        parser.add_argument('latitude', required=True, type=float)
        parser.add_argument('longitude', required=True, type=float)
        parser.add_argument('photo', required=True, type=str)
        parser.add_argument('description', default=None, type=str)
        return parser

    def setup_put_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', default=None, type=str)
        parser.add_argument('capacity', default=None, type=int)
        parser.add_argument('latitude', default=None, type=float)
        parser.add_argument('image_url', default=None, type=str)
        parser.add_argument('longitude', default=None, type=float)
        parser.add_argument('description', default=None, type=str)
        return parser

    @marshal_with(loc_fields)
    @require_login
    def get(self, user, location_uuid=None):
        current_app.logger.debug(repr(user))

        location = HammockLocation.query.filter_by(uuid=location_uuid).first()
        if location is None:
            abort_not_exist(location_uuid, 'HammockLocation')

        return location

    @marshal_with(loc_fields)
    @require_login
    def post(self, user):
        current_app.logger.debug(repr(user))

        parsed_args = self.post_parser.parse_args()

        location = HammockLocation(title=parsed_args['title'],
                                   capacity=parsed_args['capacity'],
                                   latitude=parsed_args['latitude'],
                                   longitude=parsed_args['longitude'],
                                   description=parsed_args['description'],
                                   user_uuid=user.uuid,
                                   photo=parsed_args['photo'])

        db.session.add(location)
        db.session.commit()

        return location

    @marshal_with(loc_fields)
    @require_login
    def put(self, user, location_id=None):
        current_app.logger.debug(repr(user))

        parsed_args = self.put_parser.parse_args()

        location = HammockLocation.objects(uuid=location_id).first()

        if parsed_args['latitude'] is not None \
                and parsed_args['longitude'] is not None:
            location.loc.coordinates = \
                [parsed_args['latitude'], parsed_args['longitude']]

        if parsed_args['title'] is not None:
            location.title = parsed_args['title']
        if parsed_args['capacity'] is not None:
            location.capacity = parsed_args['capacity']
        if parsed_args['description'] is not None:
            location.description = parsed_args['description']
        if parsed_args['photo'] is not None:
            location.photo = parsed_args['photo']

        location.save()

        return location.to_json()

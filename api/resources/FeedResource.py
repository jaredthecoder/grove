# -*- coding: utf-8 -*-


"""Gets a feed of hammock locations in a given area."""


# Third-Party modules
from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import current_app
from sqlalchemy import text

# Project specific modules
from api.models import db, HammockLocation
from api.utils import require_login


class FeedResource(Resource):
    """Feed Resource Class"""

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
        self.get_parser = self.setup_get_parser()

    def setup_get_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('latitude', location='args',
                            required=True, type=float)
        parser.add_argument('longitude', location='args',
                            required=True, type=float)
        parser.add_argument('distance', location='args',
                            default=20.0, type=float)
        return parser

    @marshal_with(loc_fields)
    @require_login
    def get(self, user):
        current_app.logger.debug(user.to_json())

        parser_args = self.get_parser.parse_args()

        latitude = parser_args['latitude']
        longitude = parser_args['longitude']
        distance = parser_args['distance']

        raw_locations = db.engine.execute(text(
            'select id, distance from ( select id, (6371 * acos(cos('
            'radians(:lat)) * cos(radians(lat)) * cos(radians(lon) - '
            'radians(:lon)) + sin(radians(:lat)) * sin(radians(lat)))) '
            'as distance from rental_item) as dt where distance < :dist'),
            lon=longitude, lat=latitude, dist=distance)

        locations = []
        for loc_id in raw_locations.fetchall():
            location = HammockLocation.query.filter_by(id=loc_id[0]).first()
            locations.append(location)

        return locations

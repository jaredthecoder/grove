"""FeedResource.py"""


from flask.ext.restful import Resource, reqparse, current_app

from api.documents import HammockLocation
from api.utils import require_login


class FeedResource(Resource):
    """Feed Resource Class"""

    def __init__(self):
        self.get_parser = self.setup_get_parser()

    def setup_get_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('latitude', location='args',
                            required=True, type=float)
        parser.add_argument('longitude', location='args',
                            required=True, type=float)
        parser.add_argument('latitude_delta', location='args',
                            required=True, type=float)
        parser.add_argument('longitude_delta', location='args',
                            required=True, type=float)
        """parser.add_argument('distance', location='args',
                            default=20.0, type=float)"""
        return parser

    @require_login
    def get(self, user):
        current_app.logger.debug(user.to_json())

        parser_args = self.get_parser.parse_args()

        latitude = parser_args['latitude']
        longitude = parser_args['longitude']
        latitude_delta = parser_args['latitude_delta']
        longitude_delta = parser_args['longitude_delta']

        locations = HammockLocation.objects(
            loc__within_box=[(latitude - latitude_delta,
                              longitude - longitude_delta),
                             (latitude + latitude_delta,
                              longitude + longitude_delta)])

        encoded_locations = []
        for location in locations:
            encoded_locations.append(location.to_json())

        return encoded_locations

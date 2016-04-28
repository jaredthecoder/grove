"""CommentResource.py"""

from flask.ext.restful import Resource, reqparse

from api.documents import HammockLocation
from api.utils import abort_not_exist


class LocationResource(Resource):
    """Location Resource class"""

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
        parser.add_argument('user_id', required=True, type=str)
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

    def get(self, location_uuid=None):
        location = HammockLocation.objects(uuid=location_uuid).first()
        if location is None:
            abort_not_exist(location_uuid, 'HammockLocation')
        return location.to_json()

    def post(self):
        parsed_args = self.post_parser.parse_args()
        location = HammockLocation(title=parsed_args['title'],
                                   capacity=parsed_args['capacity'],
                                   loc=[parsed_args['latitude'],
                                        parsed_args['longitude']],
                                   description=parsed_args['description'],
                                   user_uuid=parsed_args['user_id'],
                                   photo=parsed_args['photo'],
                                   id=str(uuid.uuid4()))

        location.save()

        return location.to_json()

    def put(self, location_id=None):
        parsed_args = self.put_parser.parse_args()

        location = HammockLocation.objects(uuid=location_id).first()

        if parsed_args['latitude'] is not None and parsed_args['longitude'] is not None:
            location.loc.coordinates = [parsed_args['latitude'], parsed_args['longitude']]

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

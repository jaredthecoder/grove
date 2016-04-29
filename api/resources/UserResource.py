"""UserResource.py"""


import uuid

from flask.ext.restful import Resource, reqparse, abort

from api.documents import User
from api.utils import abort_not_exist


class UserResource(Resource):
    """user Resource Class"""

    def __init__(self):
        self.post_parser = self.setup_post_parser()

    def setup_post_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', default='Richard', type=str)
        parser.add_argument('last_name', default='Hendricks', type=str)
        parser.add_argument('photo',
                            default='http://i.lv3.hbo.com/assets/images/' +
                                    'series/silicon-valley/characters/s1/' +
                                    'richard-1920.jpg',
                            type=str)
        parser.add_argument('email', default='cto@piedpiper.com')
        return parser

    def get(self, user_id=None):
        user = User.objects(uuid=user_id).first()
        if user is None:
            abort_not_exist(user_id, 'User')

        return user.to_json()

    def post(self):
        parsed_args = self.post_parser.parse_args()

        user = User(first_name=parsed_args['first_name'],
                    last_name=parsed_args['last_name'],
                    photo=parsed_args['photo'],
                    email=parsed_args['email'],
                    uuid=str(uuid.uuid4()))
        user.save()

        return user.to_json()

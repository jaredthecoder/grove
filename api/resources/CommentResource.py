"""CommentResource.py"""

from flask.ext.restful import Resource, reqparse

from api.documents import Comment, HammockLocation
from api.utils import abort_not_exist

import uuid

class CommentResource(Resource):
    """Comment Resource class"""

    def __init__(self):
        self.put_parser = self.setup_put_parser()
        self.post_parser = self.setup_post_parser()

    def setup_post_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('text', type=str)
        parser.add_argument('location_id', required=True, type=str)
        parser.add_argument('user_id', required=True, type=str)
        return parser

    def setup_put_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('text', required=True, type=str)
        return parser

    def get(self, location_uuid):
        location = HammockLocation.objects(uuid=location_uuid).first()
        if location is None:
            abort_not_exist(location_uuid, 'Location')

        encoded_comments = []
        for comment in location.comments:
            encoded_comments.append(comment.to_json())

        return encoded_comments

    def post(self):
        parsed_args = self.post_parser.parse_args()

        comment = Comment(text=parsed_args['text'],
                          location_uuid=parsed_args['location_id'],
                          user_uuid=parsed_args['user_id'],
                          id=str(uuid.uuid4()))

        HammockLocation.objects(
            uuid=parsed_args['location_id']).update_one(push__comments=comment)

        return comment.to_json()

    def put(self, comment_id=None):
        parsed_args = self.put_parser.parse_args()

        comment = Comment.objects(uuid=comment_id).first()
        if comment is None:
            abort_not_exist(comment_id, 'Comment')

        comment.update(text=parsed_args['text'])
        comment.save()

        return comment.to_json()

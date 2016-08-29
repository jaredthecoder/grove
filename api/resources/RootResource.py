# -*- coding:utf-8 -*-


"""HTTP Resources for the root endpoint in the API."""


from flask.ext.restful import Resource


class RootResource(Resource):
    """Root Resource of the API"""

    def __init__(self):
        pass

    def get(self):
        return {'message': 'Welcome to Eno Heaven!'}

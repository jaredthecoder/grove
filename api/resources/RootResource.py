"""RootResource.py - contains the code for the / (root) API endpoint."""


from flask.ext.restful import Resource


class RootResource(Resource):
    """Root Resource Class"""

    def __init__(self):
        pass

    def get(self):
        return {'message': 'Welcome to Eno Heaven!'}

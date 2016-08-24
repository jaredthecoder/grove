# -*- coding: utf-8 -*-


"""Package __init__.py module"""


from api.app import create_app


app = create_app()

__version__ = '0.1.0'
__author__ = 'Jared Michael Smith'
__license__ = 'MIT'
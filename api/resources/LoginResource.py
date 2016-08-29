"""LoginResource.py - contains the code for the /login API endpoint.


This is extremely hacky code at times simply because of how much of a pain
it is to work with Facebook's Login API.
"""

# Python standard library
import json
import urllib.parse
import uuid

# Third Party modules
import requests
from flask import request, redirect, session, current_app, abort
from flask.ext.restful import Resource

# Project modules
from api.utils import social_config
from api.models import User


class LoginResource(Resource):
    """Resource for handling logins from Facebook."""

    def get(self, provider_name):
        redirect_uri = 'https://grove-api.herokuapp.com/login/facebook/callback'
        scope = ','.join(social_config[provider_name]['scope'])

        session['state'] = uuid.uuid4()
        return redirect('https://www.facebook.com/dialog/oauth?' +
                        'client_id={app_id}&redirect_uri={'
                        'redirect_uri}&state={state}&scope={scope}'.format(
                            app_id=social_config[provider_name]['consumer_key'],
                            redirect_uri=redirect_uri, state=session['state'],
                            scope=scope))


class FacebookLoginCallbackResource(Resource):

    def get_canonical_facebook_profile_pic_url(self, user_id):
        resp = requests.get('http://graph.facebook.com/' +
                            '{user_id}/picture?type=large'.format(
                                user_id=user_id))
        return urllib.parse.quote(resp.url)

    def validate_token(self, access_token):
        params = dict(access_token=access_token)

        resp = requests.get('https://graph.facebook.com/me', params=params)

        try:
            data = json.loads(resp.text)
        except ValueError:
            current_app.logger.error('Could not load data.')
            return None

        if 'id' in data:
            return data['id']
        else:
            current_app.logger.error('ID not in data.')
            return None

    def get_user_data(self, user_id, access_token):
        user_data = {}
        params = {
            'access_token': access_token,
            'fields': 'id,email,first_name,last_name'
        }

        resp = requests.get('https://graph.facebook.com/' +
                            'v2.4/{user_id}'.format(user_id=user_id),
                            params=params)

        try:
            data = json.loads(resp.text)
        except ValueError:
            current_app.logger.error(
                'Loading json data for getting user data failed.')
            return None

        if 'id' in data:
            user_data['id'] = data['id']
            user_data['first_name'] = data.get('first_name')
            user_data['last_name'] = data.get('last_name')
            user_data['email'] = data.get('email')

            user_data['profile_photo_url'] = \
                self.get_canonical_facebook_profile_pic_url(user_id)
        else:
            current_app.logger.error(
                'User id was blank, returning None from get user data.')
            return None

        return user_data

    def get(self, provider_name):
        if 'state' in session:
            current_app.logger.debug(
                'Session state: {0}'.format(str(session['state'])))
            current_app.logger.debug('Session args state: {0}'.format(
                str(request.args.get('state'))))
            if str(session['state']) == str(request.args.get('state')):
                code = request.args.get('code')

                redirect_uri = \
                    'https://grove-api.herokuapp.com/login/facebook/callback'

                params = {
                    'client_id':
                        social_config[provider_name]['consumer_key'],
                    'redirect_uri':
                        redirect_uri,
                    'client_secret':
                        social_config[provider_name]['consumer_secret'],
                    'code':
                        code
                }

                resp = requests.get('https://graph.facebook.com/' +
                                    'v2.4/oauth/access_token', params=params)

                try:
                    data = json.loads(resp.text)
                    current_app.logger.error('Data: ' + str(data))
                except ValueError:
                    # Deeplink to iOS app
                    return redirect('grove://login_error?' +
                                    'message=unable+to+load+json+i' +
                                    'from+access+token+validation')

                access_token = data['access_token']
                user_id = self.validate_token(access_token)

                if user_id is not None:
                    existing_user = User.objects(facebook_id=user_id).first()
                    if existing_user is None:
                        user_data = self.get_user_data(user_id, access_token)
                        if not user_data:
                            return redirect('grove://login_error?' +
                                            'message=unable+to+parse+user+data')

                        new_user = User(facebook_id=user_id,
                                        first_name=user_data['first_name'],
                                        last_name=user_data['last_name'],
                                        email=user_data['email'],
                                        photo=user_data['profile_photo_url'],
                                        facebook_access_token=access_token,
                                        uuid=str(uuid.uuid4()))
                        auth_token = new_user.generate_auth_token()
                        new_user.auth_token = auth_token.decode('ascii')

                        new_user.save()

                        # Deeplink to iOS App
                        return redirect('grove://signup/' +
                                        '{id}/{auth_token}?first_name={'
                                        'first_name}&last_name={'
                                        'last_name}'.format(
                                            id=new_user.uuid,
                                            auth_token=new_user.auth_token,
                                            first_name=new_user.first_name,
                                            last_name=new_user.last_name) +
                                        '&photo={photo}'.format(
                                            photo=new_user.photo))
                    else:
                        # Deeplink to iOS App
                        return redirect('grove://login/' +
                                        '{id}/{auth_token}?first_name={'
                                        'first_name}&last_name={'
                                        'last_name}'.format(
                                            id=existing_user.uuid,
                                            auth_token=existing_user.auth_token,
                                            first_name=existing_user.first_name,
                                            last_name=existing_user.last_name) +
                                        '&photo={photo}'.format(
                                            photo=existing_user.photo))
            else:
                current_app.logger.error(
                    'Session state does not match what is' +
                    'in session request.')
                abort(401)
        else:
            current_app.logger.error('State not in session.')
            abort(401)

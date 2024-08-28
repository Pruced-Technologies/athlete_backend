import requests
from google.auth.transport import requests
from google.oauth2 import id_token
from football.models import CustomUser
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
# import random
from django.utils.crypto import get_random_string
from rest_framework_simplejwt.tokens import RefreshToken
import facebook


class Google():
    @staticmethod
    def validate(access_token):
        try:
            id_info=id_token.verify_oauth2_token(access_token, requests.Request())
            if 'accounts.google.com' in id_info['iss']:
                print(id_info)
                return id_info
        except:
            return "the token is either invalid or has expired"

class Facebook:
    """
    Facebook class to fetch the user info and return it
    """

    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the facebook GraphAPI to fetch the user info
        """
        try:
            # print(auth_token)
            graph = facebook.GraphAPI(access_token=auth_token)
            # print(graph)
            profile = graph.request('/me?fields=first_name,last_name,email')
            # print(profile)
            return profile
        except:
            return "The token is invalid or expired."



def register_social_user(provider, email, first_name, last_name):
    old_user=CustomUser.objects.filter(email=email)
    if old_user.exists():
        if provider == old_user[0].auth_provider:
            # register_user=authenticate(email=email, password=settings.SOCIAL_AUTH_PASSWORD)

            # return {
            #     'full_name':register_user.get_full_name,
            #     'email':register_user.email,
            #     'tokens':register_user.tokens()
            # }
            refresh = RefreshToken.for_user(old_user[0])
            
            refresh['first_name'] = old_user[0].first_name
            refresh['last_name'] = old_user[0].last_name
            refresh['username'] = old_user[0].username
            refresh['is_flag'] = old_user[0].is_flag

            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        else:
            raise AuthenticationFailed(
                detail=f"You are registered with {old_user[0].auth_provider}. Please continue your login with {old_user[0].auth_provider}"
            )
    else:
        # contact_no = ''.join(['9'] + [str(random.randint(2, 9)) for _ in range(1, 10)])
        new_user={
            'email':email,
            'username': get_random_string(7),
            'first_name':first_name,
            'last_name':last_name,
            'password':get_random_string(7)
        }
        user=CustomUser.objects.create_user(**new_user)
        user.auth_provider=provider
        user.is_verified=True
        user.save()
        
        # login_user=authenticate(email=email, password=settings.SOCIAL_AUTH_PASSWORD)
       
        # tokens=login_user.tokens()
        # return {
        #     'email':login_user.email,
        #     'full_name':login_user.get_full_name,
        #     "access_token":str(tokens.get('access')),
        #     "refresh_token":str(tokens.get('refresh'))
        # }
        
        refresh = RefreshToken.for_user(user)
        
        refresh['first_name'] = user.first_name
        refresh['last_name'] = user.last_name
        refresh['username'] = user.username
        refresh['is_flag'] = user.is_flag

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
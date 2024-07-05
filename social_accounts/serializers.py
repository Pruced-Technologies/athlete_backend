from rest_framework import serializers
from .helpers import Google, register_social_user, Facebook
# from .github import Github
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


class GoogleSignInSerializer(serializers.Serializer):
    access_token=serializers.CharField(min_length=6)


    def validate_access_token(self, access_token):
        user_data=Google.validate(access_token)
        try:
            user_data['sub']
            
        except:
            raise serializers.ValidationError("this token has expired or invalid please try again")
        
        if user_data['aud'] != settings.GOOGLE_CLIENT_ID:
                raise AuthenticationFailed('Could not verify user.')

        user_id=user_data['sub']
        email=user_data['email']
        first_name=user_data['given_name']
        last_name=user_data['family_name']
        provider='google'

        return register_social_user(provider, email, first_name, last_name)
    
class FacebookSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of facebook related data"""
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = Facebook.validate(auth_token)

        try:
            user_id = user_data['id']
            email = user_data['email']
            name = user_data['name']
            provider = 'facebook'
            name_list = name.split(' ') 
            first_name = name_list[0]
            last_name = name_list[1]
            
            return register_social_user(provider, email, first_name, last_name)
        
            # return register_social_user(
            #     provider=provider,
            #     user_id=user_id,
            #     email=email,
            #     name=name
            # )
        except Exception as identifier:

            raise serializers.ValidationError(
                'The token  is invalid or expired. Please login again.'
            )


# class GithubLoginSerializer(serializers.Serializer):
#     code = serializers.CharField()

#     def validate_code(self, code):   
#         access_token = Github.exchange_code_for_token(code)

#         if access_token:
#             user_data=Github.get_github_user(access_token)

#             full_name=user_data['name']
#             email=user_data['email']
#             names=full_name.split(" ")
#             firstName=names[1]
#             lastName=names[0]
#             provider='github'
#             return register_social_user(provider, email, firstName, lastName)

        
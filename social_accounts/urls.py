from django.urls import path
from .views import GoogleOauthSignInview, FacebookSocialAuthView


urlpatterns=[
    path('google/', GoogleOauthSignInview.as_view(), name='google'),
    path('facebook/', FacebookSocialAuthView.as_view(), name='facebook'),
    # path('github/', GithubOauthSignInView.as_view(), name='github')
]
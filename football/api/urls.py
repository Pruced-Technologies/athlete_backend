from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import MyTokenObtainPairView,registerView,PlayerViewSet,ClubViewSet,UserViewSet,FootballCoachViewSet,SportProfileTypeViewSet,AddressViewSet,ProfilePhotoViewSet,PlayerAcheivementsViewSet,VideoClipViewSet,ProfileDescriptionViewSet,PlayerCareerHistoryViewSet,FootballCoachCareerHistoryViewSet,FootballTournamentViewSet
from rest_framework import routers

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Routers provide an easy way of automatically determining the URL conf.


router = routers.DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'sportprofiletype', SportProfileTypeViewSet, basename='sportprofiletype')
router.register(r'address', AddressViewSet, basename='address')
router.register(r'profilephoto', ProfilePhotoViewSet, basename='profilephoto')
router.register(r'club', ClubViewSet, basename='club')
router.register(r'player', PlayerViewSet, basename='player')
router.register(r'coach', FootballCoachViewSet, basename='coach')
router.register(r'acheivements', PlayerAcheivementsViewSet, basename='acheivements')
router.register(r'videoclip', VideoClipViewSet, basename='videoclip')
router.register(r'profiledescription', ProfileDescriptionViewSet, basename='profiledescription')
router.register(r'playercareerhistory', PlayerCareerHistoryViewSet, basename='playercareerhistory')
router.register(r'coachcareerhistory', FootballCoachCareerHistoryViewSet, basename='coachcareerhistory')
router.register(r'footballtournament', FootballTournamentViewSet, basename='footballtournament')
# router.register(r'register/', registerView.as_view(), basename='register')
# router.register(r'login/', MyTokenObtainPairView.as_view(), basename='token_obtain_pair')
# router.register(r'token/refresh/', TokenRefreshView.as_view(), basename='token_refresh')
# router.register(r'footballplayer/', views.player, basename='football_player')

urlpatterns = [
    # path('', views.getRoutes),
    path('register/', registerView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('footballplayer/', views.footballPlayer, name='football_player'),
    path('footballplayer/', views.player, name='football_player'),
    path('footballplayer/<int:pk>/', views.player),
    # path('footballplayer/ ([0-9]+)$', views.player, name='football_player'),
    # path('footballclub/', views.footballClub, name='football_club'),
    path('', include(router.urls)),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
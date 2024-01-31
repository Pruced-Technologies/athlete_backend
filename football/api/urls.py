from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
# from .views import MyTokenObtainPairView,registerView,PlayerViewSet,ClubViewSet,UserViewSet,PlayerSearchViewSet,FootballCoachViewSet,SportProfileTypeViewSet,AddressViewSet,ProfilePhotoViewSet,PlayerAcheivementsViewSet,VideoClipViewSet,ProfileDescriptionViewSet,PlayerCareerHistoryViewSet,FootballCoachCareerHistoryViewSet,FootballTournamentViewSet,MyNetworkRequestViewSet,NetworkConnectedViewSet, NetworkConnectionsViewSet, FootballClubViewSet, ReferenceViewSet, ReferenceOutsideViewSet, AgentInsideViewSet, AgentOutsideViewSet, GetAgentInsideViewSet, VerifyRequestViewSet, CoachSearchViewSet
from .views import *
from rest_framework import routers

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Routers provide an easy way of automatically determining the URL conf.


router = routers.DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'sportprofiletype', SportProfileTypeViewSet, basename='sportprofiletype')
router.register(r'sportprofiletype/:pk/request_list', SportProfileTypeViewSet, basename='sportprofiletypepk')
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
router.register(r'networkrequest', MyNetworkRequestViewSet, basename='networkrequest')
router.register(r'networkrequest/:pk/request_list', MyNetworkRequestViewSet, basename='networkrequestpk')
router.register(r'networkconnect', NetworkConnectedViewSet, basename='networkconnect')
router.register(r'networkconnect/:pk/request_list', NetworkConnectedViewSet, basename='networkconnectpk')
router.register(r'networkconnections', NetworkConnectionsViewSet, basename='networkconnections')
router.register(r'instituition', FootballClubViewSet, basename='instituition')
router.register(r'instituitionhistory', FootballClubHistoryViewSet, basename='instituitionhistory')
router.register(r'instituitionofficebearer', FootballClubOfficeBearerViewSet, basename='instituitionofficebearer')
router.register(r'referenceinside', ReferenceViewSet, basename='referenceinside')
router.register(r'referenceoutside', ReferenceOutsideViewSet, basename='referenceoutside')
router.register(r'agentoutside', AgentOutsideViewSet, basename='agentoutside')
router.register(r'agentinside', AgentInsideViewSet, basename='agentinside')
router.register(r'getagentinside', GetAgentInsideViewSet, basename='getagentinside')
router.register(r'verifyrequest', VerifyRequestViewSet, basename='verifyrequest')
router.register(r'verifyrequest/:pk/request_list', VerifyRequestViewSet, basename='verifyrequestpk')
router.register(r'likes', PostLikesViewSet, basename='likes')
router.register(r'comments', PostCommentsViewSet, basename='comments')
router.register(r'getallcomments', GetAllPostCommentsListViewSet, basename='getallcomments')
router.register(r'postitem', PostItemsViewSet, basename='postitem')
router.register(r'getpostitem', GetPostItemsViewSet, basename='getpostitem')
router.register(r'news', NewsViewSet, basename='news')
router.register(r'newsall', NewsAllViewSet, basename='newsall')
router.register(r'newsall/:pk/request_list', NewsAllViewSet, basename='newsallpk')
router.register(r'getnews', GetNewsViewSet, basename='getnews')

urlpatterns = [
    # path('', views.getRoutes),
    path('register/', registerView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('search/player', PlayerSearchViewSet.as_view(), name='search_player'),
    path('search/coach', CoachSearchViewSet.as_view(), name='search_coach'),
    path('search/agent', AgentSearchViewSet.as_view(), name='search_agent'),
    path('search/instituition', ClubSearchViewSet.as_view(), name='search_instituition'),
    path('send/mail', Sendmail.as_view(), name='send_mail'),
    path('get/comments/<slug:slug>/<int:limit>/', GetPostCommentsViewSet.as_view(), name='get_comments'),
    path('connectrequest/<int:id>/', views.networkConnect),
    # path('get/comments/', GetPostCommentsViewSet.as_view(), name='get_comments_list'),
    path('', include(router.urls)),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
# from .views import MyTokenObtainPairView,registerView,PlayerViewSet,ClubViewSet,UserViewSet,PlayerSearchViewSet,FootballCoachViewSet,SportProfileTypeViewSet,AddressViewSet,ProfilePhotoViewSet,PlayerAcheivementsViewSet,VideoClipViewSet,ProfileDescriptionViewSet,PlayerCareerHistoryViewSet,FootballCoachCareerHistoryViewSet,FootballTournamentViewSet,MyNetworkRequestViewSet,NetworkConnectedViewSet, NetworkConnectionsViewSet, FootballClubViewSet, ReferenceViewSet, ReferenceOutsideViewSet, AgentInsideViewSet, AgentOutsideViewSet, GetAgentInsideViewSet, VerifyRequestViewSet, CoachSearchViewSet
from .views import *
from rest_framework import routers

from rest_framework_simplejwt.views import (
    # TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

# Routers provide an easy way of automatically determining the URL conf.


router = routers.DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'instituitioninfo', InstitutionViewSet, basename='instituitioninfo')
router.register(r'sportprofiletype', SportProfileTypeViewSet, basename='sportprofiletype')
router.register(r'sportprofiletype/:pk/request_list', SportProfileTypeViewSet, basename='sportprofiletypepk')
router.register(r'address', AddressViewSet, basename='address')
router.register(r'profilephoto', ProfilePhotoViewSet, basename='profilephoto')
router.register(r'club', ClubViewSet, basename='club')
router.register(r'footballplayerendorsementrequest', FootballPlayerEndorsementRequestViewSet, basename='footballplayerendorsementrequest')
router.register(r'getfootballplayerendorsementrequest', GetFootballPlayerEndorsementRequestViewSet, basename='footballplayerendorsementrequest')
router.register(r'getfootballcoachendorsementrequest', GetFootballCoachEndorsementRequestViewSet, basename='getfootballcoachendorsementrequest')
# router.register(r'getfootballplayerendorsementrequest/:pk/request_list', GetPlayerEndorsementRequest, basename='getfootballplayerendorsementrequest')
router.register(r'player', PlayerViewSet, basename='player')
router.register(r'coach', FootballCoachViewSet, basename='coach')
# router.register(r'acheivements', PlayerAcheivementsViewSet, basename='acheivements')
# router.register(r'personalachievements', PersonalAchievementsViewSet, basename='personalachievements')
router.register(r'videoclip', VideoClipViewSet, basename='videoclip')
router.register(r'profiledescription', ProfileDescriptionViewSet, basename='profiledescription')
# router.register(r'playercareerhistory', PlayerCareerHistoryViewSet, basename='playercareerhistory')
router.register(r'coachcareerhistory', FootballCoachCareerHistoryViewSet, basename='coachcareerhistory')
router.register(r'footballcoachendorsementrequest', FootballCoachEndorsementRequestViewSet, basename='footballcoachendorsementrequest')
router.register(r'footballtournament', FootballTournamentViewSet, basename='footballtournament')
router.register(r'networkrequest', MyNetworkRequestViewSet, basename='networkrequest')
router.register(r'networkrequest/:pk/request_list', MyNetworkRequestViewSet, basename='networkrequestpk')
router.register(r'networkconnect', NetworkConnectedViewSet, basename='networkconnect')
router.register(r'networkconnect/:pk/request_list', NetworkConnectedViewSet, basename='networkconnectpk')
router.register(r'networkconnections', NetworkConnectionsViewSet, basename='networkconnections')
router.register(r'instituition', FootballClubViewSet, basename='instituition')
router.register(r'instituitionhistory', FootballClubHistoryViewSet, basename='instituitionhistory')
router.register(r'instituitionofficebearer', FootballClubOfficeBearerViewSet, basename='instituitionofficebearer')
# router.register(r'referenceinside', ReferenceViewSet, basename='referenceinside')
# router.register(r'referenceoutside', ReferenceOutsideViewSet, basename='referenceoutside')
# router.register(r'agentoutside', AgentOutsideViewSet, basename='agentoutside')
router.register(r'agent', AgentViewSet, basename='agent')
router.register(r'getagent', GetAgentViewSet, basename='getagent')
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
router.register(r'teams', TeamsViewSet, basename='teams')
router.register(r'leagues', LeaguesViewSet, basename='leagues')
router.register(r'country', CountryViewSet, basename='country')
router.register(r'sportlicense', SportLicenseViewSet, basename='sportlicense')
router.register(r'coachlicense', CoachLicenseViewSet, basename='coachlicense')
router.register(r'agentlicense', AgentLicenseViewSet, basename='agentlicense')
router.register(r'instituitionlicense', FootballClubLicenseViewSet, basename='instituitionlicense')
router.register(r'agentcareerhistory', AgentCareerHistoryViewSet, basename='agentcareerhistory')
router.register(r'playerandcoachesunderagent', PlayersCoachesUnderAgentViewSet, basename='playerandcoachesunderagent')
router.register(r'playerandcoachesendorsementunderagent', PlayersCoachesEndorsementUnderAgentViewSet, basename='playerandcoachesendorsementunderagent')
router.register(r'playerandcoachesendorsementunderagent/:pk/request_list', PlayersCoachesEndorsementUnderAgentViewSet, basename='playerandcoachesendorsementunderagentpk')
router.register(r'getplayerandcoachesendorsementunderagent', GetPlayersCoachesEndorsementUnderAgentViewSet, basename='getplayerandcoachesendorsementunderagent')
router.register(r'getfootballplayerandcoachesendorsementunderagent', GetFootballPlayersCoachesEndorsementUnderAgentViewSet, basename='getfootballplayerandcoachesendorsementunderagent')
router.register(r'opportunities', OpportunityViewSet, basename='opportunities')
router.register(r'opportunityapplications', OpportunityApplicationsViewSet,basename='oppapplications')
router.register(r'help', HelpViewSet, basename='help')
router.register(r'helpsupport', HelpSupportViewSet, basename='helpSupport') 
router.register(r'wellnessscore', WellnessScoreViewSet, basename='wellnessscore')
router.register(r'condiotioninglog', ConditioningLogViewSet, basename='condiotioninglog')

urlpatterns = [
    path('email-verify/resend/token/', views.getExpiredToken, name='resend-token'),
    path('register/', registerView.as_view(), name='register'),
    path('register/institute/', CreateInstituteProfileView.as_view(), name='register_institute'),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('login/', LoginAPIView.as_view(), name="login"),
    # path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('search/alluser', AllUserSearchViewSet.as_view(), name='search_all_user'),
    path('search/player', PlayerSearchViewSet.as_view(), name='search_player'),
    path('search/coach', CoachSearchViewSet.as_view(), name='search_coach'),
    path('search/agent', AgentSearchViewSet.as_view(), name='search_agent'),
    path('search/instituition', ClubSearchViewSet.as_view(), name='search_instituition'),
    path('send/mail/', Sendmail.as_view(), name='send_mail'),
    path('get/comments/<slug:slug>/<int:limit>/', GetPostCommentsViewSet.as_view(), name='get_comments'),
    path('connectrequest/<int:id>/', views.networkConnect),
    path('changepassword/', views.change_password, name='change_password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('changepresentaddress/', PresentAddressUpdateView.as_view(), name='changepresentaddress'),
    path('addaddress/', AddAddressAPIViewSet.as_view(), name='addaddress'),
    path('playerhistory/', MultiModelCreateAPIView.as_view(), name='playerhistory'),
    path('playerhistorycreate/', MultiModelCreateUpdateAPIView.as_view(), name='playerhistorycreate'),
    path('playerhistoryleagueupdate/', PlayerLeagueModelUpdateAPIView.as_view(), name='playerhistoryleagueupdate'),
    path('playerhistoryteamleagueupdate/', PlayerTeamLeagueModelUpdateAPIView.as_view(), name='playerhistoryteamleagueupdate'),
    path('getplayerendorsementrequest/', GetPlayerEndorsementRequest.as_view(), name='getplayerendorsementrequest'),
    # path('footballcoachupdate/', FootballCoachUpdateModelAPIView.as_view(), name='footballcoachupdate'),
    path('footballcoachlicensecreate/', FootballCoachLicenseCreateModelAPIView.as_view(), name='footballcoachlicensecreate'),
    path('footballcoachlicenseupdate/', FootballCoachLicenseUpdateModelAPIView.as_view(), name='footballcoachlicenseupdate'),
    path('footballcoachcareerhistorycreate/', CoachCareerHistoryModelCreateAPIView.as_view(), name='footballcoachcareerhistorycreate'),
    path('footballcoachcareerhistoryleaguecreate/', CoachCareerHistoryLeagueModelCreateUpdateAPIView.as_view(), name='footballcoachcareerhistoryleaguecreate'),
    path('footballcoachcareerhistoryteamandleagueupdate/', CoachCareerHistoryTeamAndLeagueModelUpdateAPIView.as_view(), name='footballcoachcareerhistoryteamandleagueupdate'),
    path('footballcoachcareerhistoryandleagueupdate/', CoachCareerHistoryAndLeagueModelUpdateAPIView.as_view(), name='footballcoachcareerhistoryandleagueupdate'),
    path('getcoachendorsementrequest/', GetCoachEndorsementRequest.as_view(), name='getcoachendorsementrequest'),
    path('footballagentcareerhistory/', AgentCareerHisrtoryAPIView.as_view(), name='footballagentcareerhistory'),
    path('footballagentcareerhistoryupdate/', AgentCareerHistoryUpdateAPIView.as_view(), name='footballagentcareerhistoryupdate'),
    path('footballagentplayerscoachesupdate/', AgentPlayerAndCoachesEndorsementUpdateAPIView.as_view(), name='footballagentplayerscoachesupdate'),
    path('footballagentlicensecreate/', FootballAgentLicenseCreateModelAPIView.as_view(), name='footballagentlicensecreate'),
    path('footballagentlicenseupdate/', FootballAgentLicenseUpdateModelAPIView.as_view(), name='footballagentlicenseupdate'),
    path('createplayerscoachesendorsementunderagent/', AgentCreatePlayersAndCoachesEndorsementAPIView.as_view(), name='createplayerscoachesendorsementunderagent'),
    # path('sportprofilechangeuserstatus/', SportProfileTypeStatusChangeCreateAndUpdateAPIView.as_view(), name='sportprofilechangeuserstatus'),
    path('sportprofile/', SportProfileTypeCreateAndUpdateAPIView.as_view(), name='sportprofile'),
    path('changesportprofile/', ChangeSportProfileTypeAPIView.as_view(), name='changesportprofile'),
    path('instituitionlicensecreate/', FootballClubLicenseCreateModelAPIView.as_view(), name='footballcoachlicensecreate'),
    path('instituitionlicenseupdate/', FootballClubLicenseUpdateModelAPIView.as_view(), name='footballcoachlicenseupdate'),
    path('instituitioncareerhistorycreate/', FootballClubHistoryCreateAPIView.as_view(), name='instituitioncareerhistorycreate'),
    path('instituitioncareerhistoryupdate/', FootballClubHistoryUpdateAPIView.as_view(), name='instituitioncareerhistoryupdate'),
    path('get/instituition/<slug:slug>/', GetInstitutionViewSet.as_view(), name='get_instituition'),
    path('createnetworkrequest/', MyNetworkRequestAPIView.as_view(), name='createnetworkrequest'),
    path('', include(router.urls)),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
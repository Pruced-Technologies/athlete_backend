from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, filters, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView, status
from .serializers import UserSerializer,PlayerSerializer,GetPlayerSerializer,ClubSerializer,FootballCoachSerializer,SportProfileTypeSerializer,AddressSerializer,ProfilePhotoSerializer,AcheivementsSerializer,PlayerVideoClipSerializer,ProfileDescriptionSerializer,PlayerCareerHistorySerializer,FootballCoachCareerHistorySerializer,FootballTournamentsSerializer,MyNetworkRequestSerializer, GetMyNetworkRequestSerializer, NetworkConnectedSerializer,NetworkConnectionsSerializer,FootballClubSerializer,FootballClubHistorySerializer,FootballClubOfficeBearerSerializer,ReferenceSerializer, ReferenceOutsideSerializer,AgentInsideSerializer,AgentOutsideSerializer,GetAgentInsideSerializer, VerifyRequestSerializer, GetVerifyRequestSerializer, GetFootballCoachSerializer, PostCommentsSerializer, PostItemSerializer, GetPostItemSerializer, PostLikesSerializer, GetPostCommentsSerializer, NewsSerializer, GetNewsSerializer, GetFootballClubSerializer
from football.models import Club,Player,CustomUser,FootballCoach,SportProfileType,Address,ProfilePhoto,Acheivements,PlayerVideoClip,ProfileDescription,PlayerCareerHistory,FootballCoachCareerHistory,FootballTournaments,MyNetworkRequest,NetworkConnected,FootballClub, FootballClubHistory,FootballClubOfficeBearer,Reference,ReferenceOutside,Agent,AgentOutside, VerifyRequest, PostItem, PostComments, PostLikes, News
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from django_filters import rest_framework as filters
from django.db import models
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone

# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['username'] = user.username
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'football/api/register',
        'football/api/login',
        'football/api/token/refresh',
    ]

    return Response(routes)

class registerView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class UserViewSet(viewsets.ModelViewSet):
    """
    List all workkers, or create a new worker.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    # filter_backends = [filters.OrderingFilter]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class SportProfileTypeViewSet(viewsets.ModelViewSet):
    """
    List all workkers, or create a new worker.
    """
    queryset = SportProfileType.objects.all()
    serializer_class = SportProfileTypeSerializer

    @action(detail=True, methods=['get'])
    def request_list(self, request, pk=None):
    #    users = self.get_object() # retrieve an object by pk provided
       users = SportProfileType.objects.filter(user_id = pk)
    #    user_list = MyNetworkRequest.objects.filter(id=users).distinct()
       user_list_json = SportProfileTypeSerializer(users, many=True)
       return Response(user_list_json.data)

class AddressViewSet(viewsets.ModelViewSet):
    """
    List all workkers, or create a new worker.
    """
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class PlayerAcheivementsViewSet(viewsets.ModelViewSet):
    """
    List all acheivements, or create a new acheivement.
    """
    queryset = Acheivements.objects.all()
    serializer_class = AcheivementsSerializer

class VideoClipViewSet(viewsets.ModelViewSet):
    """
    List all acheivements, or create a new acheivement.
    """
    queryset = PlayerVideoClip.objects.all()
    serializer_class = PlayerVideoClipSerializer

class ProfileDescriptionViewSet(viewsets.ModelViewSet):
    """
    List all profile description, or create a new description.
    """
    queryset = ProfileDescription.objects.all()
    serializer_class = ProfileDescriptionSerializer

class PlayerCareerHistoryViewSet(viewsets.ModelViewSet):
    """
    List all workkers, or create a new worker.
    """
    queryset = PlayerCareerHistory.objects.all()
    serializer_class = PlayerCareerHistorySerializer
    
class ProfilePhotoViewSet(viewsets.ModelViewSet):
    """
    List all workkers, or create a new worker.
    """
    queryset = ProfilePhoto.objects.all()
    serializer_class = ProfilePhotoSerializer

class ClubViewSet(viewsets.ModelViewSet):
    """
    List all workkers, or create a new worker.
    """
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    

class PlayerViewSet(viewsets.ModelViewSet):
    """
    List all workers, or create a new worker.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    # filter_backends = [filters.OrderingFilter]
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def player(request, pk = None):
#     if request.method == 'GET':
#         id = pk
#         if id is not None:
#             football_player = Player.objects.get(user = id)
#             football_player_serializer = PlayerSerializer(football_player)
#             return Response(football_player_serializer.data)   
    
#         user = request.user
#         print(user)
#         football_player = Player.objects.all()
#         football_player_serializer = PlayerSerializer(football_player, many=True)
#         return Response(football_player_serializer.data)
    
class FootballCoachViewSet(viewsets.ModelViewSet):
    """
    List all workkers, or create a new worker.
    """
    queryset = FootballCoach.objects.all()
    serializer_class = FootballCoachSerializer

class FootballCoachCareerHistoryViewSet(viewsets.ModelViewSet):
    """
    List all workkers, or create a new worker.
    """
    queryset = FootballCoachCareerHistory.objects.all()
    serializer_class = FootballCoachCareerHistorySerializer

class FootballTournamentViewSet(viewsets.ModelViewSet):
    """
    List all workkers, or create a new worker.
    """
    queryset = FootballTournaments.objects.all()
    serializer_class = FootballTournamentsSerializer

class MyNetworkRequestViewSet(viewsets.ModelViewSet):
    
    queryset = MyNetworkRequest.objects.all()
    serializer_class = MyNetworkRequestSerializer

    @action(detail=True, methods=['get'])
    def request_list(self, request, pk=None):
    #    users = self.get_object() # retrieve an object by pk provided
       users = MyNetworkRequest.objects.filter(to_user = pk)
    #    user_list = MyNetworkRequest.objects.filter(id=users).distinct()
       user_list_json = GetMyNetworkRequestSerializer(users, many=True)
       return Response(user_list_json.data)

# @api_view(['GET'])
# def networkRequest(request, username = None):
#     if request.method == 'GET':
#         id = username
#         if id is not None:
#             touser = MyNetworkRequest.objects.get(to_user = id)
#             touser_serializer = MyNetworkRequestSerializer(touser, many=True)
#             return Response(touser_serializer.data)   
    
#         user = request.user
#         print(user)
#         touser = MyNetworkRequest.objects.all()
#         touser_serializer = MyNetworkRequestSerializer(touser, many=True)
#         return Response(touser_serializer.data)
    
@api_view(['PATCH'])
def networkConnect(request, id):
    my_models = NetworkConnected.objects.filter(network_request_id=id)
    for my_model in my_models:
        serializer = NetworkConnectionsSerializer(my_model, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
    return Response
        
class NetworkConnectedViewSet(viewsets.ModelViewSet):
    
    queryset = NetworkConnected.objects.all()
    serializer_class = NetworkConnectedSerializer

    def get_serializer(self, *args, **kwargs):
        """ if an array is passed, set serializer to many """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(NetworkConnectedViewSet, self).get_serializer(*args, **kwargs)

    @action(detail=True, methods=['get'])
    def request_list(self, request, pk=None):
    #    users = self.get_object() # retrieve an object by pk provided
       users = NetworkConnected.objects.filter(user_id = pk).order_by('-id')
    #    user_list = MyNetworkRequest.objects.filter(id=users).distinct()
       user_list_json = NetworkConnectedSerializer(users, many=True)
       return Response(user_list_json.data)
    
class NetworkConnectionsViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    ViewSet create and list books

    Usage single : POST
    {
        "name":"Killing Floor: A Jack Reacher Novel", 
        "author":"Lee Child"
    }

    Usage array : POST
    [{  
        "name":"Mr. Mercedes: A Novel (The Bill Hodges Trilogy)",
        "author":"Stephen King"
    },{
        "name":"Killing Floor: A Jack Reacher Novel", 
        "author":"Lee Child"
    }]
    """
    queryset = NetworkConnected.objects.all()
    serializer_class = NetworkConnectionsSerializer
    search_fields = ('connect_to_user','status','user_id','network_request_id')

    def create(self, request, *args, **kwargs):
        """
        #checks if post request data is an array initializes serializer with many=True
        else executes default CreateModelMixin.create function 
        """
        is_many = isinstance(request.data, list)
        if not is_many:
            return super(NetworkConnectionsViewSet, self).create(request, *args, **kwargs)
        else:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
class FootballClubViewSet(viewsets.ModelViewSet):
    """
    List all workkers, or create a new worker.
    """
    queryset = FootballClub.objects.all()
    serializer_class = FootballClubSerializer

class FootballClubHistoryViewSet(viewsets.ModelViewSet):
    """
    List all workkers, or create a new worker.
    """
    queryset = FootballClubHistory.objects.all()
    serializer_class = FootballClubHistorySerializer

class FootballClubOfficeBearerViewSet(viewsets.ModelViewSet):
    """
    List all workkers, or create a new worker.
    """
    queryset = FootballClubOfficeBearer.objects.all()
    serializer_class = FootballClubOfficeBearerSerializer

class ReferenceViewSet(viewsets.ModelViewSet):
    """
    List all workkers, or create a new worker.
    """
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer

class ReferenceOutsideViewSet(viewsets.ModelViewSet):
    """
    List all workkers, or create a new worker.
    """
    queryset = ReferenceOutside.objects.all()
    serializer_class = ReferenceOutsideSerializer

class AgentOutsideViewSet(viewsets.ModelViewSet):
    """
    List all workkers, or create a new worker.
    """
    queryset = AgentOutside.objects.all()
    serializer_class = AgentOutsideSerializer

class AgentInsideViewSet(viewsets.ModelViewSet):
    """
    List all workkers, or create a new worker.
    """
    queryset = Agent.objects.all()
    serializer_class = AgentInsideSerializer

class GetAgentInsideViewSet(viewsets.ModelViewSet):
    """
    List all workkers, or create a new worker.
    """
    queryset = Agent.objects.all()
    serializer_class = GetAgentInsideSerializer

class VerifyRequestViewSet(viewsets.ModelViewSet):
    
    queryset = VerifyRequest.objects.all()
    serializer_class = VerifyRequestSerializer

    @action(detail=True, methods=['get'])
    def request_list(self, request, pk=None):
    #    users = self.get_object() # retrieve an object by pk provided
       users = VerifyRequest.objects.filter(to_user = pk)
    #    user_list = MyNetworkRequest.objects.filter(id=users).distinct()
       user_list_json = GetVerifyRequestSerializer(users, many=True)
       return Response(user_list_json.data)
    

class PlayerFilter(filters.FilterSet):

    class Meta:
        model = Player
        fields = ['user__first_name', 'user__last_name', 'primary_position', 'secondary_position', 'top_speed', 'preferred_foot', 'current_club_inside_name']
        filter_overrides = {
            models.CharField: {
                'filter_class': filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }
    
class PlayerSearchViewSet(ListAPIView):
    queryset = Player.objects.all()
    serializer_class = GetPlayerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PlayerFilter

class CoachFilter(filters.FilterSet):

    class Meta:
        model = FootballCoach
        fields = ['user__first_name', 'user__last_name', 'current_team']
        filter_overrides = {
            models.CharField: {
                'filter_class': filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }

class CoachSearchViewSet(ListAPIView):
    queryset = FootballCoach.objects.all()
    serializer_class = GetFootballCoachSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CoachFilter

class AgentFilter(filters.FilterSet):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'sport_type']
        filter_overrides = {
            models.CharField: {
                'filter_class': filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }

class AgentSearchViewSet(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AgentFilter

class ClubFilter(filters.FilterSet):

    class Meta:
        model = FootballClub
        fields = ['user__first_name', 'user__sport_type']
        filter_overrides = {
            models.CharField: {
                'filter_class': filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }

class ClubSearchViewSet(ListAPIView):
    queryset = FootballClub.objects.all()
    serializer_class = GetFootballClubSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClubFilter
    
class Sendmail(APIView):
    def post(self,request):
        email=request.data['to']
        email_body=request.data['message']
        emailmes=EmailMessage(
            'Invitaion from Scouting',
            email_body,
            settings.EMAIL_HOST_USER,
            [email]
        )
        emailmes.send(fail_silently=False)
        return Response({'status':True,'message':'Email sent successfully'})
    
class PostLikesViewSet(viewsets.ModelViewSet):
    
    queryset = PostLikes.objects.all()
    serializer_class = PostLikesSerializer
    
class GetAllPostCommentsListViewSet(viewsets.ModelViewSet):
    
    queryset = PostComments.objects.all()
    serializer_class = GetPostCommentsSerializer
    
class GetPostCommentsViewSet(APIView):
    def get(self, request, slug, limit):
        try:
            item = PostComments.objects.get(post_id=slug)
        except PostComments.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except PostComments.MultipleObjectsReturned:
            # limit = request.query_params.get('limit', 10)
            items = PostComments.objects.filter(post_id=slug).order_by('-posted')[:int(limit)]
            serializer = GetPostCommentsSerializer(items, many=True)
            return Response(serializer.data)
        serializer = GetPostCommentsSerializer(item)
        return Response(serializer.data)

class PostCommentsViewSet(viewsets.ModelViewSet):
    
    queryset = PostComments.objects.all()
    serializer_class = PostCommentsSerializer

class PostItemsViewSet(viewsets.ModelViewSet):
    
    queryset = PostItem.objects.all()
    serializer_class = PostItemSerializer

class GetPostItemsViewSet(viewsets.ModelViewSet):
    
    queryset = PostItem.objects.all().order_by('-posted')
    serializer_class = GetPostItemSerializer

class NewsAllViewSet(viewsets.ModelViewSet):
    
    queryset = News.objects.all().order_by('-id')
    serializer_class = NewsSerializer

    @action(detail=True, methods=['get'])
    def request_list(self, request, pk=None):
    #    users = self.get_object() # retrieve an object by pk provided
       users = News.objects.filter(user = pk)
    #    user_list = MyNetworkRequest.objects.filter(id=users).distinct()
       user_list_json = NewsSerializer(users, many=True)
       return Response(user_list_json.data)

class GetNewsViewSet(viewsets.ModelViewSet):
    
    queryset = News.objects.all().order_by('-id')
    serializer_class = GetNewsSerializer

class NewsFilter(filters.FilterSet):
  end_date = filters.DateFilter(field_name='end_date', lookup_expr='lt')
  class Meta:
    model = News
    fields = ['end_date']

class NewsViewSet(viewsets.ModelViewSet):
    
    # queryset = News.objects.all().order_by('-start_date')
    today = timezone.localtime().date()
    queryset = News.objects.filter(end_date__gt=today).order_by('-start_date')
    serializer_class = NewsSerializer
    # filter_backends = [filters.DjangoFilterBackend]
    # filter_class = NewsFilter


# class GetNewsViewSet(viewsets.ModelViewSet):
    
#     queryset = News.objects.all().order_by('-start_date')
#     serializer_class = GetNewsSerializer
#     filter_backends = [filters.DjangoFilterBackend]
#     filter_class = NewsFilter

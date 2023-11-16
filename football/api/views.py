from django.shortcuts import render
from rest_framework import viewsets, filters, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView, status
from .serializers import UserSerializer,PlayerSerializer,ClubSerializer,FootballCoachSerializer,SportProfileTypeSerializer,AddressSerializer,ProfilePhotoSerializer,AcheivementsSerializer,PlayerVideoClipSerializer,ProfileDescriptionSerializer,PlayerCareerHistorySerializer,FootballCoachCareerHistorySerializer,FootballTournamentsSerializer,MyNetworkRequestSerializer, NetworkConnectedSerializer,NetworkConnectionsSerializer,FootballClubSerializer, ReferenceSerializer, ReferenceOutsideSerializer,AgentInsideSerializer,AgentOutsideSerializer,GetAgentInsideSerializer, VerifyRequestSerializer, GetVerifyRequestSerializer
from football.models import Club,Player,CustomUser,FootballCoach,SportProfileType,Address,ProfilePhoto,Acheivements,PlayerVideoClip,ProfileDescription,PlayerCareerHistory,FootballCoachCareerHistory,FootballTournaments,MyNetworkRequest,NetworkConnected,FootballClub,Reference,ReferenceOutside,Agent,AgentOutside, VerifyRequest
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView

# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['first_name'] = user.first_name
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
    filter_backends = [filters.OrderingFilter]
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
    filter_backends = [filters.OrderingFilter]
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
       user_list_json = MyNetworkRequestSerializer(users, many=True)
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
    search_fields = ('connect_to_user','status','user_id')

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
    
class PlayerSearchViewSet(ListAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user__first_name', 'user__last_name', 'primary_position', 'secondary_position', 'top_speed', 'preferred_foot']
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['user__first_name', 'user__last_name', 'primary_position', 'secondary_position', 'top_speed', 'preferred_foot']
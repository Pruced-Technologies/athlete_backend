from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from .serializers import UserSerializer,PlayerSerializer,ClubSerializer,FootballCoachSerializer,SportProfileTypeSerializer,AddressSerializer,ProfilePhotoSerializer,AcheivementsSerializer,PlayerVideoClipSerializer,ProfileDescriptionSerializer,PlayerCareerHistorySerializer,FootballCoachCareerHistorySerializer,FootballTournamentsSerializer
from football.models import Club,Player,CustomUser,FootballCoach,SportProfileType,Address,ProfilePhoto,Acheivements,PlayerVideoClip,ProfileDescription,PlayerCareerHistory,FootballCoachCareerHistory,FootballTournaments
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.first_name
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def player(request, pk = None):
    if request.method == 'GET':
        id = pk
        if id is not None:
            football_player = Player.objects.get(user = id)
            football_player_serializer = PlayerSerializer(football_player)
            return Response(football_player_serializer.data)   
    
        user = request.user
        print(user)
        football_player = Player.objects.all()
        football_player_serializer = PlayerSerializer(football_player, many=True)
        return Response(football_player_serializer.data)
    
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
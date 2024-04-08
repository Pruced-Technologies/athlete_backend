from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, filters, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView, status
from .serializers import *
from football.models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, UpdateAPIView
from django_filters import rest_framework as filters
from django_filters import FilterSet, AllValuesFilter, NumberFilter, CharFilter
from django.db import models
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.utils import timezone
from .emails import *
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
# import datetime

from django_rest_passwordreset.signals import reset_password_token_created

# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['username'] = user.username
        token['sport_type'] = user.sport_type
        # ...

        # print(token)
        # print(user.email)
        # send_token_via_email(user.email,token)
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    # print(serializer_class.data)


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
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    # filter_backends = [filters.OrderingFilter]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class SportProfileTypeViewSet(viewsets.ModelViewSet):
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
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

# class PlayerAcheivementsViewSet(viewsets.ModelViewSet):
#     queryset = Acheivements.objects.all()
#     serializer_class = AcheivementsSerializer

class VideoClipViewSet(viewsets.ModelViewSet):
    queryset = PlayerVideoClip.objects.all()
    serializer_class = PlayerVideoClipSerializer

class ProfileDescriptionViewSet(viewsets.ModelViewSet):
    queryset = ProfileDescription.objects.all()
    serializer_class = ProfileDescriptionSerializer
    
# class PersonalAchievementsViewSet(viewsets.ModelViewSet):
#     queryset = PersonalAchievements.objects.all()
#     serializer_class = PersonalAchievementsSerializer

# class PlayerCareerHistoryViewSet(viewsets.ModelViewSet):
#     queryset = PlayerCareerHistory.objects.all()
#     serializer_class = PlayerCareerHistorySerializer
    
class ProfilePhotoViewSet(viewsets.ModelViewSet):
    queryset = ProfilePhoto.objects.all()
    serializer_class = ProfilePhotoSerializer

class ClubViewSet(viewsets.ModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    # filter_backends = [filters.OrderingFilter]
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    
class FootballCoachViewSet(viewsets.ModelViewSet):
    queryset = FootballCoach.objects.all()
    serializer_class = FootballCoachSerializer

class FootballCoachCareerHistoryViewSet(viewsets.ModelViewSet):
    queryset = FootballCoachCareerHistory.objects.all()
    serializer_class = FootballCoachCareerHistorySerializer

class FootballTournamentViewSet(viewsets.ModelViewSet):
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
    queryset = FootballClub.objects.all()
    serializer_class = FootballClubSerializer

class FootballClubHistoryViewSet(viewsets.ModelViewSet):
    queryset = FootballClubHistory.objects.all()
    serializer_class = FootballClubHistorySerializer

class FootballClubOfficeBearerViewSet(viewsets.ModelViewSet):
    queryset = FootballClubOfficeBearer.objects.all()
    serializer_class = FootballClubOfficeBearerSerializer

# class ReferenceViewSet(viewsets.ModelViewSet):
#     queryset = Reference.objects.all()
#     serializer_class = ReferenceSerializer

# class ReferenceOutsideViewSet(viewsets.ModelViewSet):
#     queryset = ReferenceOutside.objects.all()
#     serializer_class = ReferenceOutsideSerializer

# class AgentOutsideViewSet(viewsets.ModelViewSet):
#     queryset = AgentOutside.objects.all()
#     serializer_class = AgentOutsideSerializer

class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

class GetAgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

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
    user__min_height = NumberFilter(field_name='user__height', lookup_expr='gte')
    user__max_height = NumberFilter(field_name='user__height', lookup_expr='lte')
    user__min_weight = NumberFilter(field_name='user__weight', lookup_expr='gte')
    user__max_weight = NumberFilter(field_name='user__weight', lookup_expr='lte')
    min_top_speed = NumberFilter(field_name='top_speed', lookup_expr='gte')
    max_top_speed = NumberFilter(field_name='top_speed', lookup_expr='lte')
    primary_position = AllValuesFilter(field_name='primary_position')
    secondary_position = AllValuesFilter(field_name='secondary_position')
    preferred_foot = AllValuesFilter(field_name='preferred_foot')
    current_club = AllValuesFilter(field_name='current_club')
    user__citizenship = AllValuesFilter(field_name='user__citizenship')
    user__first_name = CharFilter(field_name='user__first_name', lookup_expr='icontains')
    user__last_name = CharFilter(field_name='user__last_name', lookup_expr='icontains')
    user__dob = filters.DateFromToRangeFilter(field_name='user__dob')
    # age = NumberFilter(method='filter_by_age')
    # user__min_age = NumberFilter(field_name='user__dob', lookup_expr='year__gte')
    # user__max_age = NumberFilter(field_name='user__dob', lookup_expr='year__lte')

    class Meta:
        model = Player
        fields = (
            'user__min_height',
            'user__max_height',
            'user__min_weight',
            'user__max_weight',
            'min_top_speed',
            'max_top_speed',
            'primary_position',
            'secondary_position',
            'preferred_foot',
            'current_club',
            'user__citizenship',
            'user__dob',
            'user__first_name',
            'user__last_name'
        )
    
class PlayerSearchViewSet(ListAPIView):
    queryset = Player.objects.all()
    serializer_class = GetPlayerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PlayerFilter


class CoachFilter(filters.FilterSet):
    user__min_height = NumberFilter(field_name='user__height', lookup_expr='gte')
    user__max_height = NumberFilter(field_name='user__height', lookup_expr='lte')
    user__min_weight = NumberFilter(field_name='user__weight', lookup_expr='gte')
    user__max_weight = NumberFilter(field_name='user__weight', lookup_expr='lte')
    user__citizenship = AllValuesFilter(field_name='user__citizenship')
    user__first_name = CharFilter(field_name='user__first_name', lookup_expr='icontains')
    user__last_name = CharFilter(field_name='user__last_name', lookup_expr='icontains')
    user__dob = filters.DateFromToRangeFilter(field_name='user__dob')
    # current_team = AllValuesFilter(field_name='current_team')
    # from_date = NumberFilter(field_name='from_date', lookup_expr='gte')
    # to_date = NumberFilter(field_name='to_date', lookup_expr='lte')
    # min_playoffs_games_coached_in = NumberFilter(field_name='playoffs_games_coached_in', lookup_expr='gte')
    # max_playoffs_games_coached_in = NumberFilter(field_name='playoffs_games_coached_in', lookup_expr='lte')
    # min_playoffs_games_won = NumberFilter(field_name='playoffs_games_won', lookup_expr='gte')
    # max_playoffs_games_won = NumberFilter(field_name='playoffs_games_won', lookup_expr='lte')
    # min_playoffs_games_lost = NumberFilter(field_name='playoffs_games_lost', lookup_expr='gte')
    # max_playoffs_games_lost = NumberFilter(field_name='playoffs_games_lost', lookup_expr='lte')

    class Meta:
        model = FootballCoach
        fields = (
            'user__min_height',
            'user__max_height',
            'user__min_weight',
            'user__max_weight',
            'user__citizenship',
            'user__first_name',
            'user__last_name',
            'user__dob'
        )
        
        
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                # update_session_auth_hash(request, user)  # To update session after password change
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    # context = {
    #     'current_user': reset_password_token.user,
    #     'username': reset_password_token.user.username,
    #     'email': reset_password_token.user.email,
    #     'reset_password_url': "{}?token={}".format(
    #         instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
    #         reset_password_token.key)
    # }

    # render email text
    # email_html_message = render_to_string('email/password_reset_email.html', context)
    # email_plaintext_message = render_to_string('email/password_reset_email.txt', context)

    # msg = EmailMultiAlternatives(
    #     # title:
    #     "Password Reset for {title}".format(title="Scouting"),
    #     # message:
    #     email_plaintext_message,
    #     # from:
    #     "athletescouting@gmail.com",
    #     # to:
    #     [reset_password_token.user.email]
    # )
    # msg.attach_alternative(email_html_message, "text/html")
    # msg.send()

    # email_plaintext_message = "{}?token={}".format(
    #     instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')), 
    #     reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Scouting"),
        # message:
        # email_plaintext_message,
        "Your token is {token}".format(token=reset_password_token.key),
        # from:
        "athletescouting@gmail.com",
        # to:
        [reset_password_token.user.email]
    )

class PresentAddressUpdateView(APIView):
    def post(self, request):
        data = request.data
        instances_to_update = []
        for obj in data:
            instance_id = obj.get('id')
            try:
                instance = Address.objects.get(id=instance_id)
            except Address.DoesNotExist:
                return Response(f"Instance with ID {instance_id} not found", status=404)
            instances_to_update.append((instance, obj))

        updated_instances = []
        for instance, obj in instances_to_update:
            serializer = AddressSerializer(instance, data=obj, partial=True)
            if serializer.is_valid():
                serializer.save()
                updated_instances.append(serializer.data)
            else:
                return Response(serializer.errors, status=400)
        
        return Response(updated_instances, status=200)
    
class TeamsViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    
class LeaguesViewSet(viewsets.ModelViewSet):
    # queryset = League.objects.filter(league_type='international').order_by('-league_name')
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    
class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    
class MultiModelCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Assuming the request data contains a 'type' field indicating the model
        data_type = request.data.get('flag')
        # print(data_type)

        if data_type == 'league':
            data = request.data

            # Separate the data based on the models
            league_data = {key: data[key] for key in ['sport_type', 'league_name', 'league_type']}
            player_data = {key: data[key] for key in ['club_id', 'club_name', 'period', 'games_played', 'club_goals', 'club_assists', 'club_passes', 'club_saved_goals', 'interceptions_per_game', 'takles_per_game', 'shots_per_game', 'key_passes_per_game', 'dribles_completed_per_game', 'clean_sheets_per_game', 'club_yellow_card', 'club_red_card', 'league_id', 'league_name', 'country_name', 'league_type', 'status', 'remarks', 'achievements', 'players']}
            # And so on...

            # Serialize the data for each model
            league_serializer = LeagueSerializer(data=league_data)
            # player_serializer = ClubSerializer(data=player_data)
            # And so on...

            # Validate the data for each model
            # Validate the data for each model
            if league_serializer.is_valid():
                league_instance = league_serializer.save()
                
                # Extract 'id' from model1_instance
                league_id = league_instance.id
                
                # Assign id to the appropriate field in Model2
                player_data['league_id'] = league_id    
                coach_serializer = ClubSerializer(data=player_data)
                if coach_serializer.is_valid():
                    coach_serializer.save()
        
                    # Return any relevant data or success message
                    return Response({"message": "Data saved successfully"}, status=201)
                else:
                    errors = {}
                    errors['coach_errors'] = coach_serializer.errors
                    
                    return Response(errors, status=400)
            else:
                # If any serializer data is invalid, return errors
                errors = {}
                if not league_serializer.is_valid():
                    errors['league_errors'] = league_serializer.errors
               
                return Response(errors, status=400)
            
        elif data_type == 'team':
             # Get the data sent through HTTP POST
            data = request.data
            
            if 'league_id' in data:
                # If 'id' is present, it's an update operation
                flag=1
                league_id = data.get('league_id')
                sport_type = data.get('sport_type')
                print(league_id)
                # league_data = {key: data[key] for key in ['sport_type', 'league_name', 'league_type']}
                my_object = League.objects.get(id=league_id)
                print(my_object.sport_type)
                substrings = my_object.sport_type.split(',')
                print(f"Substrings are {substrings}")
                for substring in substrings:
                    print(f"Sport type: {sport_type} found in the list.")
                    if(substring.lower() == sport_type.lower()):
                        print(f"Substring: {substring} found in the list.")
                        flag = 0
                if(flag == 1):
                    my_object.sport_type = my_object.sport_type + "," + sport_type
                    print(my_object.sport_type)
                    my_object.save()

            # Separate the data based on the models
            team_data = {key: data[key] for key in ['club_name', 'reg_id', 'country_name', 'sport_type']}
            player_data = {key: data[key] for key in ['club_id', 'club_name', 'period', 'games_played', 'club_goals', 'club_assists', 'club_passes', 'club_saved_goals', 'interceptions_per_game', 'takles_per_game', 'shots_per_game', 'key_passes_per_game', 'dribles_completed_per_game', 'clean_sheets_per_game', 'club_yellow_card', 'club_red_card', 'league_id', 'league_name', 'country_name', 'league_type', 'status', 'remarks', 'achievements', 'players']}
            # And so on...

            # Serialize the data for each model
            team_serializer = TeamSerializer(data=team_data)

            # Validate the data for each model
            if team_serializer.is_valid():
                team_instance = team_serializer.save()
                
                # Extract 'id' from model1_instance
                team_id = team_instance.id
                
                # Assign id to the appropriate field in Model2
                player_data['club_id'] = team_id    
                player_serializer = ClubSerializer(data=player_data)
                if player_serializer.is_valid():
                    player_serializer.save()
        
                    # Return any relevant data or success message
                    return Response({"message": "Data saved successfully"}, status=201)
                else:
                    errors = {}
                    errors['player_errors'] = player_serializer.errors
                    
                    return Response(errors, status=400)
            else:
                # If any serializer data is invalid, return errors
                errors = {}
                if not team_serializer.is_valid():
                    errors['team_errors'] = team_serializer.errors
               
                return Response(errors, status=400)
        
        elif data_type == 'teamleague':
             # Get the data sent through HTTP POST
            data = request.data

            # Separate the data based on the models
            league_data = {key: data[key] for key in ['sport_type', 'league_name', 'league_type']}
            team_data = {key: data[key] for key in ['club_name', 'reg_id', 'country_name', 'sport_type']}
            player_data = {key: data[key] for key in ['club_id', 'club_name', 'period', 'games_played', 'club_goals', 'club_assists', 'club_passes', 'club_saved_goals', 'interceptions_per_game', 'takles_per_game', 'shots_per_game', 'key_passes_per_game', 'dribles_completed_per_game', 'clean_sheets_per_game', 'club_yellow_card', 'club_red_card', 'league_id', 'league_name', 'country_name', 'league_type', 'status', 'remarks', 'achievements', 'players']}

            # Serialize the data for each model
            league_serializer = LeagueSerializer(data=league_data)
            team_serializer = TeamSerializer(data=team_data)

            # Validate the data for each model
            if team_serializer.is_valid() and league_serializer.is_valid():
                team_instance = team_serializer.save()
                league_instance = league_serializer.save()
                
                # Extract 'id' from model1_instance
                team_id = team_instance.id
                league_id = league_instance.id
                
                # Assign id to the appropriate field in Model2
                player_data['club_id'] = team_id    
                player_data['league_id'] = league_id    
                player_serializer = ClubSerializer(data=player_data)
                if player_serializer.is_valid():
                    player_serializer.save()
        
                    # Return any relevant data or success message
                    return Response({"message": "Data saved successfully"}, status=201)
                else:
                    errors = {}
                    errors['player_errors'] = player_serializer.errors
                    
                    return Response(errors, status=400)
            else:
                # If any serializer data is invalid, return errors
                errors = {}
                if not team_serializer.is_valid():
                    errors['team_errors'] = team_serializer.errors
                if not league_serializer.is_valid():
                    errors['league_errors'] = league_serializer.errors
               
                return Response(errors, status=400)
            
        else:
            return Response({"error": "Invalid data type provided"}, status=400)
        

class MultiModelCreateUpdateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Check if 'id' is present in request data
        if 'league_id' in request.data:
            # If 'id' is present, it's an update operation
            flag=1
            data = request.data
            league_id = data.get('league_id')
            sport_type = data.get('sport_type')
            print(league_id)
            my_object = League.objects.get(id=league_id)
            print(my_object.sport_type)
            substrings = my_object.sport_type.split(',')
            print(f"Substrings are {substrings}")
            for substring in substrings:
                print(f"Sport type: {sport_type} found in the list.")
                if(substring.lower() == sport_type.lower()):
                    print(f"Substring: {substring} found in the list.")
                    flag = 0
            if(flag == 1):
                my_object.sport_type = my_object.sport_type + "," + sport_type
                print(my_object.sport_type)
                my_object.save()
            return self.create(request, *args, **kwargs)
        else:
            # If 'id' is not present, it's a create operation
            return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
       
        serializer = ClubSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)
    
class PlayerLeagueModelUpdateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        value = request.data.get('league_id')
        # Check if 'id' is present in request data
        if value != '':
            # If 'id' is present, it's an update operation
            flag=1
            data = request.data
            league_id = data.get('league_id')
            sport_type = data.get('sport_type')
            print(league_id)
            my_object = League.objects.get(id=league_id)
            print(my_object.sport_type)
            # Split the string into multiple substrings based on comma
            substrings = my_object.sport_type.split(',')
            print(f"Substrings are {substrings}")
            for substring in substrings:
                print(f"Sport type: {sport_type} found in the list.")
                if(substring.lower() == sport_type.lower()):
                    print(f"Substring: {substring} found in the list.")
                    flag = 0
            if(flag == 1):
                my_object.sport_type = my_object.sport_type + "," + sport_type
                print(my_object.sport_type)
                my_object.save()
            return self.update(request, *args, **kwargs)
        else:
            # If 'id' is not present, it's a create operation
            return self.update(request, *args, **kwargs)
            # return Response({"No data found"}, status=400)

    def update(self, request, *args, **kwargs):
        # Get the instance to update
        instance_id = request.data.get('id')  # Remove 'id' from data
        try:
            instance = Club.objects.get(pk=instance_id)
        except Club.DoesNotExist:
            return Response({"error": "Instance does not exist"}, status=404)

        # Update the instance
        serializer = ClubSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
class PlayerTeamLeagueModelUpdateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Assuming the request data contains a 'type' field indicating the model
        data_type = request.data.get('flag')
        # print(data_type)

        if data_type == 'league':
            data = request.data

            # Separate the data based on the models
            league_data = {key: data[key] for key in ['sport_type', 'league_name', 'league_type']}
            player_data = {key: data[key] for key in ['id', 'club_id', 'club_name', 'period', 'games_played', 'club_goals', 'club_assists', 'club_passes', 'club_saved_goals', 'interceptions_per_game', 'takles_per_game', 'shots_per_game', 'key_passes_per_game', 'dribles_completed_per_game', 'clean_sheets_per_game', 'club_yellow_card', 'club_red_card', 'league_name', 'country_name', 'league_type', 'status', 'remarks', 'achievements', 'players']}
            # And so on...

            # Serialize the data for each model
            league_serializer = LeagueSerializer(data=league_data)

            # Validate the data for each model
            if league_serializer.is_valid():
                # Perform any additional processing or actions as needed
                # For example, save the data to the respective models
                league_serializer.save()
    
                # Get the instance to update
                instance_id = request.data.get('id')  # Remove 'id' from data
                try:
                    instance = Club.objects.get(pk=instance_id)
                except Club.DoesNotExist:
                    return Response({"error": "Instance does not exist"}, status=404)

                # Update the instance
                serializer = ClubSerializer(instance, data=player_data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=200)
                return Response(serializer.errors, status=400)
            else:
                # If any serializer data is invalid, return errors
                errors = {}
                if not league_serializer.is_valid():
                    errors['league_errors'] = league_serializer.errors
        
                return Response(errors, status=400)
            
        elif data_type == 'team':
             # Get the data sent through HTTP POST
            data = request.data
            
            if 'league_id' in data:
                # If 'id' is present, it's an update operation
                flag=1
                league_id = data.get('league_id')
                sport_type = data.get('sport_type')
                print(league_id)
                my_object = League.objects.get(id=league_id)
                print(my_object.sport_type)
                substrings = my_object.sport_type.split(',')
                print(f"Substrings are {substrings}")
                for substring in substrings:
                    print(f"Sport type: {sport_type} found in the list.")
                    if(substring.lower() == sport_type.lower()):
                        print(f"Substring: {substring} found in the list.")
                        flag = 0
                if(flag == 1):
                    my_object.sport_type = my_object.sport_type + "," + sport_type
                    print(my_object.sport_type)
                    my_object.save()

            # Separate the data based on the models
            team_data = {key: data[key] for key in ['club_name', 'reg_id', 'country_name', 'sport_type']}
            player_data = {key: data[key] for key in ['id', 'club_id', 'club_name', 'period', 'games_played', 'club_goals', 'club_assists', 'club_passes', 'club_saved_goals', 'interceptions_per_game', 'takles_per_game', 'shots_per_game', 'key_passes_per_game', 'dribles_completed_per_game', 'clean_sheets_per_game', 'club_yellow_card', 'club_red_card', 'league_name', 'country_name', 'league_type', 'status', 'remarks', 'achievements', 'players']}
            # And so on...

            # Serialize the data for each model
            team_serializer = TeamSerializer(data=team_data)

            # Validate the data for each model
            if team_serializer.is_valid():
                team_instance = team_serializer.save()
                
                # Extract 'id' from model1_instance
                team_id = team_instance.id
                
                # Assign id to the appropriate field in Model2
                player_data['club_id'] = team_id   
                instance_id = data.get('id')  # Remove 'id' from data
                try:
                    instance = Club.objects.get(pk=instance_id)
                except Club.DoesNotExist:
                    return Response({"error": "Instance does not exist"}, status=404)

                # Update the instance
                serializer = ClubSerializer(instance, data=player_data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=200)
                return Response(serializer.errors, status=400)
            else:
                # If any serializer data is invalid, return errors
                errors = {}
                if not team_serializer.is_valid():
                    errors['team_errors'] = team_serializer.errors
               
                return Response(errors, status=400)
        
        elif data_type == 'teamleague':
             # Get the data sent through HTTP POST
            data = request.data

            # Separate the data based on the models
            league_data = {key: data[key] for key in ['sport_type', 'league_name', 'league_type']}
            team_data = {key: data[key] for key in ['club_name', 'reg_id', 'country_name', 'sport_type']}
            player_data = {key: data[key] for key in ['id', 'club_id', 'club_name', 'period', 'games_played', 'club_goals', 'club_assists', 'club_passes', 'club_saved_goals', 'interceptions_per_game', 'takles_per_game', 'shots_per_game', 'key_passes_per_game', 'dribles_completed_per_game', 'clean_sheets_per_game', 'club_yellow_card', 'club_red_card', 'league_name', 'country_name', 'league_type', 'status', 'remarks', 'achievements', 'players']}

            # Serialize the data for each model
            league_serializer = LeagueSerializer(data=league_data)
            team_serializer = TeamSerializer(data=team_data)

            # Validate the data for each model
            if team_serializer.is_valid() and league_serializer.is_valid():
                team_instance = team_serializer.save()
                league_serializer.save()
                
                # Extract 'id' from model1_instance
                team_id = team_instance.id
                
                # Assign id to the appropriate field in Model2
                player_data['club_id'] = team_id    
                instance_id = data.get('id')  # Remove 'id' from data
                try:
                    instance = Club.objects.get(pk=instance_id)
                except Club.DoesNotExist:
                    return Response({"error": "Instance does not exist"}, status=404)

                # Update the instance
                serializer = ClubSerializer(instance, data=player_data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=200)
                return Response(serializer.errors, status=400)
            else:
                # If any serializer data is invalid, return errors
                errors = {}
                if not team_serializer.is_valid():
                    errors['team_errors'] = team_serializer.errors
                if not league_serializer.is_valid():
                    errors['league_errors'] = league_serializer.errors
               
                return Response(errors, status=400)
            
        else:
            return Response({"error": "Invalid data type provided"}, status=400)
        
class SportLicenseViewSet(viewsets.ModelViewSet):
    queryset = SportLicense.objects.all()
    serializer_class = SportLicenseSerializer
    
class CoachLicenseViewSet(viewsets.ModelViewSet):
    queryset = CoachLicense.objects.all()
    serializer_class = CoachLicenseSerializer
    
# class FootballCoachUpdateModelAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         # Check if 'id' is present in request data
#         if 'license_id' in request.data:
#             # If 'id' is present, it's an update operation
#             return self.update(request, *args, **kwargs)
#         else:
#             # If 'id' is not present, it's a create operation
#             return self.create(request, *args, **kwargs)

#     def update(self, request, *args, **kwargs):
#         # Get the instance to update
#         instance_id = request.data.get('id')  # Remove 'id' from data
#         try:
#             instance = FootballCoach.objects.get(pk=instance_id)
#         except FootballCoach.DoesNotExist:
#             return Response({"error": "Instance does not exist"}, status=404)

#         # Update the instance
#         serializer = FootballCoachSerializer(instance, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=200)
#         return Response(serializer.errors, status=400)
    
#     def create(self, request, *args, **kwargs):
#         data = request.data
        
#         # Separate the data based on the models
#         license_data = {key: data[key] for key in ['license_name']}
#         coach_data = {key: data[key] for key in ['id', 'user', 'license_name', 'certificate']}
#         # And so on...

#         # Serialize the data for each model
#         license_serializer = SportLicenseSerializer(data=license_data)

#         # Validate the data for each model
#         if license_serializer.is_valid():
#             # Perform any additional processing or actions as needed
#             # For example, save the data to the respective models
#             license_serializer.save()
    
#             # Get the instance to update
#             instance_id = request.data.get('id')  # Remove 'id' from data
#             try:
#                 instance = FootballCoach.objects.get(pk=instance_id)
#             except FootballCoach.DoesNotExist:
#                 return Response({"error": "Instance does not exist"}, status=404)

#             # Update the instance
#             serializer = FootballCoachSerializer(instance, data=coach_data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=200)
#             return Response(serializer.errors, status=400)
#         else:
#             # If any serializer data is invalid, return errors
#             errors = {}
#             if not license_serializer.is_valid():
#                 errors['license_errors'] = license_serializer.errors
        
#             return Response(errors, status=400)


class FootballCoachLicenseCreateModelAPIView(APIView):
    def post(self, request, *args, **kwargs):
        value = request.data.get('license_id')
        # Check if 'id' is present in request data
        if value != '':
            # If 'id' is present, it's an update operation
            # return self.update(request, *args, **kwargs)
            serializer = CoachLicenseSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        else:
            # If 'id' is not present, it's a create operation
            if 'certificate' in request.data:
                data = request.data
        
                # Separate the data based on the models
                license_data = {key: data[key] for key in ['license_name']}
                coach_data = {key: data[key] for key in ['license_id', 'license_name', 'certificate', 'coach']}
                # And so on...

                # Serialize the data for each model
                license_serializer = SportLicenseSerializer(data=license_data)

                # Validate the data for each model
                if license_serializer.is_valid():
                    license_instance = license_serializer.save()
                        
                    # Extract 'id' from model1_instance
                    license_id = license_instance.id
                        
                    # Assign id to the appropriate field in Model2
                    coach_data['license_id'] = license_id    
                    coach_serializer = CoachLicenseSerializer(data=coach_data)
                    if coach_serializer.is_valid():
                        coach_serializer.save()
                
                        # Return any relevant data or success message
                        return Response({"message": "Data saved successfully"}, status=201)
                    else:
                        errors = {}
                        errors['coach_errors'] = coach_serializer.errors
                            
                        return Response(errors, status=400)
                else:
                    # If any serializer data is invalid, return errors
                    errors = {}
                    if not license_serializer.is_valid():
                        errors['license_errors'] = license_serializer.errors
                
                    return Response(errors, status=400)
            else:
                return self.create(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        data = request.data
        
        # Separate the data based on the models
        license_data = {key: data[key] for key in ['license_name']}
        coach_data = {key: data[key] for key in ['license_id', 'license_name', 'coach']}
        # And so on...

        # Serialize the data for each model
        license_serializer = SportLicenseSerializer(data=license_data)

        # Validate the data for each model
        if license_serializer.is_valid():
            license_instance = license_serializer.save()
                
            # Extract 'id' from model1_instance
            license_id = license_instance.id
                
            # Assign id to the appropriate field in Model2
            coach_data['license_id'] = license_id    
            coach_serializer = CoachLicenseSerializer(data=coach_data)
            if coach_serializer.is_valid():
                coach_serializer.save()
        
                # Return any relevant data or success message
                return Response({"message": "Data saved successfully"}, status=201)
            else:
                errors = {}
                errors['coach_errors'] = coach_serializer.errors
                    
                return Response(errors, status=400)
        else:
            # If any serializer data is invalid, return errors
            errors = {}
            if not license_serializer.is_valid():
                errors['license_errors'] = license_serializer.errors
        
            return Response(errors, status=400)

class FootballCoachLicenseUpdateModelAPIView(APIView):
    def post(self, request, *args, **kwargs):
        value = request.data.get('license_id')
        # Check if 'id' is present in request data
        if value != '':
            # If 'id' is present, it's an update operation
            return self.update(request, *args, **kwargs)
        else:
            # If 'id' is not present, it's a create operation
            if 'certificate' in request.data:
                data = request.data
        
                # Separate the data based on the models
                license_data = {key: data[key] for key in ['license_name']}
                coach_data = {key: data[key] for key in ['id', 'license_id', 'license_name', 'certificate', 'coach']}
                # And so on...

                # Serialize the data for each model
                license_serializer = SportLicenseSerializer(data=license_data)

                # Validate the data for each model
                if license_serializer.is_valid():
                    license_instance = license_serializer.save()
                
                    # Extract 'id' from model1_instance
                    license_id = license_instance.id
                        
                    # Assign id to the appropriate field in Model2
                    coach_data['license_id'] = license_id 
            
                    # Get the instance to update
                    instance_id = request.data.get('id')  # Remove 'id' from data
                    try:
                        instance = CoachLicense.objects.get(pk=instance_id)
                    except CoachLicense.DoesNotExist:
                        return Response({"error": "Instance does not exist"}, status=404)

                    # Update the instance
                    serializer = CoachLicenseSerializer(instance, data=coach_data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=200)
                    return Response(serializer.errors, status=400)
                else:
                    # If any serializer data is invalid, return errors
                    errors = {}
                    if not license_serializer.is_valid():
                        errors['license_errors'] = license_serializer.errors
                
                    return Response(errors, status=400)
            else:
                return self.create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # Get the instance to update
        instance_id = request.data.get('id')  # Remove 'id' from data
        try:
            instance = CoachLicense.objects.get(pk=instance_id)
        except CoachLicense.DoesNotExist:
            return Response({"error": "Instance does not exist"}, status=404)

        # Update the instance
        serializer = CoachLicenseSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    def create(self, request, *args, **kwargs):
        data = request.data
        
        # Separate the data based on the models
        license_data = {key: data[key] for key in ['license_name']}
        coach_data = {key: data[key] for key in ['id', 'license_id', 'license_name', 'coach']}
        # And so on...

        # Serialize the data for each model
        license_serializer = SportLicenseSerializer(data=license_data)

        # Validate the data for each model
        if license_serializer.is_valid():
            license_instance = license_serializer.save()
                
            # Extract 'id' from model1_instance
            license_id = license_instance.id
                
            # Assign id to the appropriate field in Model2
            coach_data['license_id'] = license_id 
    
            # Get the instance to update
            instance_id = request.data.get('id')  # Remove 'id' from data
            try:
                instance = CoachLicense.objects.get(pk=instance_id)
            except CoachLicense.DoesNotExist:
                return Response({"error": "Instance does not exist"}, status=404)

            # Update the instance
            serializer = CoachLicenseSerializer(instance, data=coach_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        else:
            # If any serializer data is invalid, return errors
            errors = {}
            if not license_serializer.is_valid():
                errors['license_errors'] = license_serializer.errors
        
            return Response(errors, status=400)
        
class CoachCareerHistoryModelCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Assuming the request data contains a 'type' field indicating the model
        data_type = request.data.get('flag')
        # print(data_type)

        if data_type == 'league':
            data = request.data

            # Separate the data based on the models
            league_data = {key: data[key] for key in ['sport_type', 'league_name', 'league_type']}
            coach_data = {key: data[key] for key in ['club_id', 'club_name', 'period', 'league_id', 'league_name', 'country_name', 'league_type', 'status', 'remarks', 'achievements', 'coach_id']}
            # And so on...

            # Serialize the data for each model
            league_serializer = LeagueSerializer(data=league_data)
            # coach_serializer = FootballCoachCareerHistorySerializer(data=coach_data)
            # And so on...

            # Validate the data for each model
            if league_serializer.is_valid():
                league_instance = league_serializer.save()
                
                # Extract 'id' from model1_instance
                league_id = league_instance.id
                
                # Assign id to the appropriate field in Model2
                coach_data['league_id'] = league_id    
                coach_serializer = FootballCoachCareerHistorySerializer(data=coach_data)
                if coach_serializer.is_valid():
                    coach_serializer.save()
        
                    # Return any relevant data or success message
                    return Response({"message": "Data saved successfully"}, status=201)
                else:
                    errors = {}
                    errors['coach_errors'] = coach_serializer.errors
                    
                    return Response(errors, status=400)
            else:
                # If any serializer data is invalid, return errors
                errors = {}
                if not league_serializer.is_valid():
                    errors['league_errors'] = league_serializer.errors
               
                return Response(errors, status=400)
            
        elif data_type == 'team':
             # Get the data sent through HTTP POST
            data = request.data
            
            if 'league_id' in data:
                # If 'id' is present, it's an update operation
                flag=1
                league_id = data.get('league_id')
                sport_type = data.get('sport_type')
                print(league_id)
                # league_data = {key: data[key] for key in ['sport_type', 'league_name', 'league_type']}
                my_object = League.objects.get(id=league_id)
                print(my_object.sport_type)
                substrings = my_object.sport_type.split(',')
                print(f"Substrings are {substrings}")
                for substring in substrings:
                    print(f"Sport type: {sport_type} found in the list.")
                    if(substring.lower() == sport_type.lower()):
                        print(f"Substring: {substring} found in the list.")
                        flag = 0
                if(flag == 1):
                    my_object.sport_type = my_object.sport_type + "," + sport_type
                    print(my_object.sport_type)
                    my_object.save()

            # Separate the data based on the models
            team_data = {key: data[key] for key in ['club_name', 'reg_id', 'country_name', 'sport_type']}
            coach_data = {key: data[key] for key in ['club_id', 'club_name', 'period', 'league_id', 'league_name', 'country_name', 'league_type', 'status', 'remarks', 'achievements', 'coach_id']}
            # And so on...

            # Serialize the data for each model
            team_serializer = TeamSerializer(data=team_data)

            # Validate the data for each model
            if team_serializer.is_valid():
                team_instance = team_serializer.save()
                
                # Extract 'id' from model1_instance
                team_id = team_instance.id
                
                # Assign id to the appropriate field in Model2
                coach_data['club_id'] = team_id    
                coach_serializer = FootballCoachCareerHistorySerializer(data=coach_data)
                if coach_serializer.is_valid():
                    coach_serializer.save()
        
                    # Return any relevant data or success message
                    return Response({"message": "Data saved successfully"}, status=201)
                else:
                    errors = {}
                    errors['coach_errors'] = coach_serializer.errors
                    
                    return Response(errors, status=400)
            else:
                # If any serializer data is invalid, return errors
                errors = {}
                if not team_serializer.is_valid():
                    errors['team_errors'] = team_serializer.errors
               
                return Response(errors, status=400)
        
        elif data_type == 'teamleague':
             # Get the data sent through HTTP POST
            data = request.data

            # Separate the data based on the models
            league_data = {key: data[key] for key in ['sport_type', 'league_name', 'league_type']}
            team_data = {key: data[key] for key in ['club_name', 'reg_id', 'country_name', 'sport_type']}
            coach_data = {key: data[key] for key in ['club_id', 'club_name', 'period', 'league_id', 'league_name', 'country_name', 'league_type', 'status', 'remarks', 'achievements', 'coach_id']}

            # Serialize the data for each model
            league_serializer = LeagueSerializer(data=league_data)
            team_serializer = TeamSerializer(data=team_data)

            # Validate the data for each model
            if team_serializer.is_valid() and league_serializer.is_valid():
                team_instance = team_serializer.save()
                league_instance = league_serializer.save()
                
                # Extract 'id' from model1_instance
                team_id = team_instance.id
                league_id = league_instance.id
                
                # Assign id to the appropriate field in Model2
                coach_data['club_id'] = team_id    
                coach_data['league_id'] = league_id    
                coach_serializer = FootballCoachCareerHistorySerializer(data=coach_data)
                if coach_serializer.is_valid():
                    coach_serializer.save()
        
                    # Return any relevant data or success message
                    return Response({"message": "Data saved successfully"}, status=201)
                else:
                    errors = {}
                    errors['coach_errors'] = coach_serializer.errors
                    
                    return Response(errors, status=400)
            else:
                # If any serializer data is invalid, return errors
                errors = {}
                if not team_serializer.is_valid():
                    errors['team_errors'] = team_serializer.errors
                if not league_serializer.is_valid():
                    errors['league_errors'] = league_serializer.errors
               
                return Response(errors, status=400)
            
        else:
            return Response({"error": "Invalid data type provided"}, status=400)
        
class CoachCareerHistoryLeagueModelCreateUpdateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Check if 'id' is present in request data
        if 'league_id' in request.data:
            # If 'id' is present, it's an update operation
            flag=1
            data = request.data
            league_id = data.get('league_id')
            sport_type = data.get('sport_type')
            print(league_id)
            my_object = League.objects.get(id=league_id)
            print(my_object.sport_type)
            substrings = my_object.sport_type.split(',')
            print(f"Substrings are {substrings}")
            for substring in substrings:
                print(f"Sport type: {sport_type} found in the list.")
                if(substring.lower() == sport_type.lower()):
                    print(f"Substring: {substring} found in the list.")
                    flag = 0
            if(flag == 1):
                my_object.sport_type = my_object.sport_type + "," + sport_type
                print(my_object.sport_type)
                my_object.save()
            return self.create(request, *args, **kwargs)
        else:
            # If 'id' is not present, it's a create operation
            return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
       
        serializer = FootballCoachCareerHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)
    

class CoachCareerHistoryAndLeagueModelUpdateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Check if 'id' is present in request data
        value = request.data.get('league_id')
        
        if value != '':
            # If 'id' is present, it's an update operation
            flag=1
            data = request.data
            league_id = data.get('league_id')
            sport_type = data.get('sport_type')
            print(league_id)
            my_object = League.objects.get(id=league_id)
            print(my_object.sport_type)
            # Split the string into multiple substrings based on comma
            substrings = my_object.sport_type.split(',')
            print(f"Substrings are {substrings}")
            for substring in substrings:
                print(f"Sport type: {sport_type} found in the list.")
                if(substring.lower() == sport_type.lower()):
                    print(f"Substring: {substring} found in the list.")
                    flag = 0
            if(flag == 1):
                my_object.sport_type = my_object.sport_type + "," + sport_type
                print(my_object.sport_type)
                my_object.save()
            return self.update(request, *args, **kwargs)
        else:
            # If 'id' is not present, it's a create operation
            return self.update(request, *args, **kwargs)
            # return Response({"No data found"}, status=400)

    def update(self, request, *args, **kwargs):
        # Get the instance to update
        instance_id = request.data.get('id')  # Remove 'id' from data
        try:
            instance = FootballCoachCareerHistory.objects.get(pk=instance_id)
        except FootballCoachCareerHistory.DoesNotExist:
            return Response({"error": "Instance does not exist"}, status=404)

        # Update the instance
        serializer = FootballCoachCareerHistorySerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
class CoachCareerHistoryTeamAndLeagueModelUpdateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Assuming the request data contains a 'type' field indicating the model
        data_type = request.data.get('flag')
        # print(data_type)

        if data_type == 'league':
            data = request.data

            # Separate the data based on the models
            league_data = {key: data[key] for key in ['sport_type', 'league_name', 'league_type']}
            coach_data = {key: data[key] for key in ['id', 'club_id', 'club_name', 'period', 'league_id', 'league_name', 'country_name', 'league_type', 'status', 'remarks', 'achievements', 'coach_id']}
            # And so on...

            # Serialize the data for each model
            league_serializer = LeagueSerializer(data=league_data)

            # Validate the data for each model
            if league_serializer.is_valid():
                league_instance = league_serializer.save()
                
                # Extract 'id' from model1_instance
                league_id = league_instance.id
                
                # Assign id to the appropriate field in Model2
                coach_data['league_id'] = league_id
    
                # Get the instance to update
                instance_id = data.get('id')  # Remove 'id' from data
                try:
                    instance = FootballCoachCareerHistory.objects.get(pk=instance_id)
                except FootballCoachCareerHistory.DoesNotExist:
                    return Response({"error": "Instance does not exist"}, status=404)

                # Update the instance
                serializer = FootballCoachCareerHistorySerializer(instance, data=coach_data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=200)
                return Response(serializer.errors, status=400)
            else:
                # If any serializer data is invalid, return errors
                errors = {}
                if not league_serializer.is_valid():
                    errors['league_errors'] = league_serializer.errors
        
                return Response(errors, status=400)
            
        elif data_type == 'team':
             # Get the data sent through HTTP POST
            data = request.data
            
            if 'league_id' in data:
                # If 'id' is present, it's an update operation
                flag=1
                league_id = data.get('league_id')
                sport_type = data.get('sport_type')
                print(league_id)
                my_object = League.objects.get(id=league_id)
                print(my_object.sport_type)
                substrings = my_object.sport_type.split(',')
                print(f"Substrings are {substrings}")
                for substring in substrings:
                    print(f"Sport type: {sport_type} found in the list.")
                    if(substring.lower() == sport_type.lower()):
                        print(f"Substring: {substring} found in the list.")
                        flag = 0
                if(flag == 1):
                    my_object.sport_type = my_object.sport_type + "," + sport_type
                    print(my_object.sport_type)
                    my_object.save()

            # Separate the data based on the models
            team_data = {key: data[key] for key in ['club_name', 'reg_id', 'country_name', 'sport_type']}
            coach_data = {key: data[key] for key in ['id', 'club_id', 'club_name', 'period', 'league_id', 'league_name', 'country_name', 'league_type', 'status', 'remarks', 'achievements', 'coach_id']}
            # And so on...

            # Serialize the data for each model
            team_serializer = TeamSerializer(data=team_data)

            # Validate the data for each model
            if team_serializer.is_valid():
                team_instance = team_serializer.save()
                
                # Extract 'id' from model1_instance
                team_id = team_instance.id
                
                # Assign id to the appropriate field in Model2
                coach_data['club_id'] = team_id   
                instance_id = data.get('id')  # Remove 'id' from data
                try:
                    instance = FootballCoachCareerHistory.objects.get(pk=instance_id)
                except FootballCoachCareerHistory.DoesNotExist:
                    return Response({"error": "Instance does not exist"}, status=404)

                # Update the instance
                serializer = FootballCoachCareerHistorySerializer(instance, data=coach_data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=200)
                return Response(serializer.errors, status=400)
            else:
                # If any serializer data is invalid, return errors
                errors = {}
                if not team_serializer.is_valid():
                    errors['team_errors'] = team_serializer.errors
               
                return Response(errors, status=400)
        
        elif data_type == 'teamleague':
             # Get the data sent through HTTP POST
            data = request.data

            # Separate the data based on the models
            league_data = {key: data[key] for key in ['sport_type', 'league_name', 'league_type']}
            team_data = {key: data[key] for key in ['club_name', 'reg_id', 'country_name', 'sport_type']}
            coach_data = {key: data[key] for key in ['id', 'club_id', 'club_name', 'period', 'league_id', 'league_name', 'country_name', 'league_type', 'status', 'remarks', 'achievements', 'coach_id']}

            # Serialize the data for each model
            league_serializer = LeagueSerializer(data=league_data)
            team_serializer = TeamSerializer(data=team_data)

            # Validate the data for each model
            if team_serializer.is_valid() and league_serializer.is_valid():
                team_instance = team_serializer.save()
                league_instance = league_serializer.save()
                
                # Extract 'id' from model1_instance
                team_id = team_instance.id
                league_id = league_instance.id
                
                # Assign id to the appropriate field in Model2
                coach_data['club_id'] = team_id    
                coach_data['league_id'] = league_id    
                instance_id = data.get('id')  # Remove 'id' from data
                try:
                    instance = FootballCoachCareerHistory.objects.get(pk=instance_id)
                except FootballCoachCareerHistory.DoesNotExist:
                    return Response({"error": "Instance does not exist"}, status=404)

                # Update the instance
                serializer = FootballCoachCareerHistorySerializer(instance, data=coach_data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=200)
                return Response(serializer.errors, status=400)
            else:
                # If any serializer data is invalid, return errors
                errors = {}
                if not team_serializer.is_valid():
                    errors['team_errors'] = team_serializer.errors
                if not league_serializer.is_valid():
                    errors['league_errors'] = league_serializer.errors
               
                return Response(errors, status=400)
            
        else:
            return Response({"error": "Invalid data type provided"}, status=400)
        
# class FootballAgentUpdateModelAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         # Check if 'id' is present in request data
#         if 'license_id' in request.data:
#             # If 'id' is present, it's an update operation
#             print(request.data)
#             return self.update(request, *args, **kwargs)
#         else:
#             # If 'id' is not present, it's a create operation
#             return self.create(request, *args, **kwargs)

#     def update(self, request, *args, **kwargs):
#         # Get the instance to update
#         instance_id = request.data.get('id')  # Remove 'id' from data
#         try:
#             instance = Agent.objects.get(pk=instance_id)
#         except Agent.DoesNotExist:
#             return Response({"error": "Instance does not exist"}, status=404)

#         # Update the instance
#         serializer = AgentSerializer(instance, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=200)
#         return Response(serializer.errors, status=400)
    
#     def create(self, request, *args, **kwargs):
#         data = request.data
        
#         # Separate the data based on the models
#         license_data = {key: data[key] for key in ['license_name']}
#         agent_data = {key: data[key] for key in ['id', 'user', 'license_name', 'certificate', 'country_name']}
#         # And so on...

#         # Serialize the data for each model
#         license_serializer = SportLicenseSerializer(data=license_data)

#         # Validate the data for each model
#         if license_serializer.is_valid():
#             # Perform any additional processing or actions as needed
#             # For example, save the data to the respective models
#             license_serializer.save()
    
#             # Get the instance to update
#             instance_id = request.data.get('id')  # Remove 'id' from data
#             try:
#                 instance = Agent.objects.get(pk=instance_id)
#             except Agent.DoesNotExist:
#                 return Response({"error": "Instance does not exist"}, status=404)

#             # Update the instance
#             serializer = AgentSerializer(instance, data=agent_data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=200)
#             return Response(serializer.errors, status=400)
#         else:
#             # If any serializer data is invalid, return errors
#             errors = {}
#             if not license_serializer.is_valid():
#                 errors['license_errors'] = license_serializer.errors
        
#             return Response(errors, status=400)

class AgentLicenseViewSet(viewsets.ModelViewSet):
    queryset = AgentLicense.objects.all()
    serializer_class = AgentLicenseSerializer

class FootballAgentLicenseCreateModelAPIView(APIView):
    def post(self, request, *args, **kwargs):
        value = request.data.get('license_id')
        # Check if 'id' is present in request data
        if value != '':
            # If 'id' is present, it's an update operation
            # return self.update(request, *args, **kwargs)
            serializer = AgentLicenseSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        else:
            # If 'id' is not present, it's a create operation
            if 'certificate' in request.data:
                data = request.data
        
                # Separate the data based on the models
                license_data = {key: data[key] for key in ['license_name']}
                agent_data = {key: data[key] for key in ['license_id', 'license_name', 'certificate', 'agent']}
                # And so on...

                # Serialize the data for each model
                license_serializer = SportLicenseSerializer(data=license_data)

                # Validate the data for each model
                if license_serializer.is_valid():
                    license_instance = license_serializer.save()
                        
                    # Extract 'id' from model1_instance
                    license_id = license_instance.id
                        
                    # Assign id to the appropriate field in Model2
                    agent_data['license_id'] = license_id    
                    agent_serializer = AgentLicenseSerializer(data=agent_data)
                    if agent_serializer.is_valid():
                        agent_serializer.save()
                
                        # Return any relevant data or success message
                        return Response({"message": "Data saved successfully"}, status=201)
                    else:
                        errors = {}
                        errors['agent_errors'] = agent_serializer.errors
                            
                        return Response(errors, status=400)
                else:
                    # If any serializer data is invalid, return errors
                    errors = {}
                    if not license_serializer.is_valid():
                        errors['license_errors'] = license_serializer.errors
                
                    return Response(errors, status=400)
            else:
                return self.create(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        data = request.data
        
        # Separate the data based on the models
        license_data = {key: data[key] for key in ['license_name']}
        agent_data = {key: data[key] for key in ['license_id', 'license_name', 'agent']}
        # And so on...

        # Serialize the data for each model
        license_serializer = SportLicenseSerializer(data=license_data)

        # Validate the data for each model
        if license_serializer.is_valid():
            license_instance = license_serializer.save()
                
            # Extract 'id' from model1_instance
            license_id = license_instance.id
                
            # Assign id to the appropriate field in Model2
            agent_data['license_id'] = license_id    
            agent_serializer = AgentLicenseSerializer(data=agent_data)
            if agent_serializer.is_valid():
                agent_serializer.save()
        
                # Return any relevant data or success message
                return Response({"message": "Data saved successfully"}, status=201)
            else:
                errors = {}
                errors['coach_errors'] = agent_serializer.errors
                    
                return Response(errors, status=400)
        else:
            # If any serializer data is invalid, return errors
            errors = {}
            if not license_serializer.is_valid():
                errors['license_errors'] = license_serializer.errors
        
            return Response(errors, status=400)

class FootballAgentLicenseUpdateModelAPIView(APIView):
    def post(self, request, *args, **kwargs):
        value = request.data.get('license_id')
        # Check if 'id' is present in request data
        if value != '':
            # If 'id' is present, it's an update operation
            return self.update(request, *args, **kwargs)
        else:
            # If 'id' is not present, it's a create operation
            if 'certificate' in request.data:
                data = request.data
        
                # Separate the data based on the models
                license_data = {key: data[key] for key in ['license_name']}
                agent_data = {key: data[key] for key in ['id', 'license_id', 'license_name', 'certificate', 'agent']}
                # And so on...

                # Serialize the data for each model
                license_serializer = SportLicenseSerializer(data=license_data)

                # Validate the data for each model
                if license_serializer.is_valid():
                    license_instance = license_serializer.save()
                
                    # Extract 'id' from model1_instance
                    license_id = license_instance.id
                        
                    # Assign id to the appropriate field in Model2
                    agent_data['license_id'] = license_id 
            
                    # Get the instance to update
                    instance_id = request.data.get('id')  # Remove 'id' from data
                    try:
                        instance = AgentLicense.objects.get(pk=instance_id)
                    except AgentLicense.DoesNotExist:
                        return Response({"error": "Instance does not exist"}, status=404)

                    # Update the instance
                    serializer = AgentLicenseSerializer(instance, data=agent_data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=200)
                    return Response(serializer.errors, status=400)
                else:
                    # If any serializer data is invalid, return errors
                    errors = {}
                    if not license_serializer.is_valid():
                        errors['license_errors'] = license_serializer.errors
                
                    return Response(errors, status=400)
            else:
                return self.create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # Get the instance to update
        instance_id = request.data.get('id')  # Remove 'id' from data
        try:
            instance = AgentLicense.objects.get(pk=instance_id)
        except AgentLicense.DoesNotExist:
            return Response({"error": "Instance does not exist"}, status=404)

        # Update the instance
        serializer = AgentLicenseSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    def create(self, request, *args, **kwargs):
        data = request.data
        
        # Separate the data based on the models
        license_data = {key: data[key] for key in ['license_name']}
        agent_data = {key: data[key] for key in ['id', 'license_id', 'license_name', 'agent']}
        # And so on...

        # Serialize the data for each model
        license_serializer = SportLicenseSerializer(data=license_data)

        # Validate the data for each model
        if license_serializer.is_valid():
            license_instance = license_serializer.save()
                
            # Extract 'id' from model1_instance
            license_id = license_instance.id
                
            # Assign id to the appropriate field in Model2
            agent_data['license_id'] = license_id 
    
            # Get the instance to update
            instance_id = request.data.get('id')  # Remove 'id' from data
            try:
                instance = AgentLicense.objects.get(pk=instance_id)
            except AgentLicense.DoesNotExist:
                return Response({"error": "Instance does not exist"}, status=404)

            # Update the instance
            serializer = AgentLicenseSerializer(instance, data=agent_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        else:
            # If any serializer data is invalid, return errors
            errors = {}
            if not license_serializer.is_valid():
                errors['license_errors'] = license_serializer.errors
        
            return Response(errors, status=400)
        
class AgentCareerHistoryViewSet(viewsets.ModelViewSet):
    queryset = AgentCareerHistory.objects.all()
    serializer_class = AgentCareerHistorySerializer
    
class PlayersCoachesUnderAgentViewSet(viewsets.ModelViewSet):
    queryset = FootballPlayersAndCoachesUnderMe.objects.all()
    serializer_class = FootballPlayersAndCoachesUnderMeSerializer
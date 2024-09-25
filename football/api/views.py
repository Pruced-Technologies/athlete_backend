from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
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
from rest_framework.generics import ListAPIView, GenericAPIView
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
from django.db import transaction
from django.utils.crypto import get_random_string
import random
from django.contrib.sites.shortcuts import get_current_site
from .utils import Util
import jwt
from django.db.models import Q
# import datetime

from django_rest_passwordreset.signals import reset_password_token_created

# Create your views here.

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         # Add custom claims
#         token['first_name'] = user.first_name
#         token['last_name'] = user.last_name
#         token['username'] = user.username
#         token['sport_type'] = user.sport_type
#         token['is_verified'] = user.is_verified
#         # ...

#         # print(token)
#         # print(user.email)
#         # send_token_via_email(user.email,token)
#         return token


# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'football/api/register',
        'football/api/login',
        'football/api/token/refresh',
    ]

    return Response(routes)

# class RegisterView(generics.GenericAPIView):

#     serializer_class = RegisterSerializer
#     renderer_classes = (UserRenderer,)

#     def post(self, request):
#         user = request.data
#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         user_data = serializer.data
#         user = User.objects.get(email=user_data['email'])
#         token = RefreshToken.for_user(user).access_token
#         current_site = get_current_site(request).domain
#         relativeLink = reverse('email-verify')
#         absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
#         email_body = 'Hi '+user.username + \
#             ' Use the link below to verify your email \n' + absurl
#         data = {'email_body': email_body, 'to_email': user.email,
#                 'email_subject': 'Verify your email'}

#         Util.send_email(data)
#         return Response(user_data, status=status.HTTP_201_CREATED)

# class registerView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         verifation_code = serializer.validated_data['otp']
#         send_mail(
#             subject='Email Verification',
#             message=f'Your verification code is {verifation_code}',
#             from_email='athletescouting@gmail.com',
#             recipient_list=[serializer.validated_data['email']],
#             fail_silently=False,
#         )
#         # return Response(serializer.data)
#         return Response({"message": "Data saved successfully"}, status=200)

class registerView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = CustomUser.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)+"&email="+user.email
        email_body = 'Hi '+user.username + ', \n Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        Util.send_email(data)
        return Response({"message": "Data saved successfully. Please check your mail for verification your user's account.", "data":user_data}, status=200)


def getExpiredToken(request):
        emailId = request.GET.get('emailId')
        print(f'my email Id:',emailId)   
        try:
            # print(f'my token:',token)                                                                        
            # user_data = jwt.decode(token, settings.SECRET_KEY,algorithms=["HS256"])
            # print(f'my user data:',user_data)                                                                        
            user = CustomUser.objects.get(email=emailId)
            # print(user)
            token = RefreshToken.for_user(user).access_token
            current_site = get_current_site(request).domain
            relativeLink = reverse('email-verify')
            absurl = 'http://'+current_site+relativeLink+"?token="+str(token)+"&email="+user.email
            email_body = 'Hi '+user.username + ', \n Use the link below to verify your email \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Verify your email'}
            print(data)
            Util.send_email(data)
            # return Response({"message": "Data saved successfully. Please check your mail for verification your user's account.", "data":user_data}, status=200)
            return HttpResponse("Token send successfully. Please check your mail for verification your user's account.")
            # return render(request, 'token_response.html', {"message": "Data saved successfully. Please check your mail for verification your user's account."})
        except:
            return HttpResponse("User does not exist.")
        

class VerifyEmail(APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        emailId = request.GET.get('email')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY,algorithms=["HS256"])
            # payload.blacklist()
            # print(payload)
            user = CustomUser.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            # return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
            return render(request, 'football/my_template.html')
        except jwt.ExpiredSignatureError as identifier:
            # return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
            return render(request, 'football/my_template_session_expired.html', {'emailId':emailId})
        except jwt.exceptions.DecodeError as identifier:
            # return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)   
            return render(request, 'football/my_template_invalid_token.html')
        
class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    
    
    
# class UserAPIView(GenericAPIView):
#     serializer_class = UserSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)  

class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    # filter_backends = [filters.OrderingFilter]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] 
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    # filter_backends = [filters.OrderingFilter]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Access the related Author model
        # print(instance)
        # user = SportProfileType.objects.filter(user=instance.id)
        # print(user)
        # if len(user) > 0:
        #     print('Sport profile created already')
        #     if not instance.is_flag:
        #         instance.is_flag = True
        #         # instance.account_type = 'user'
        #         instance.save() 
        # else:
        #     print('Sport profile not created yet')
            
        return Response(serializer.data, status=status.HTTP_200_OK)

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
    
class AddAddressAPIViewSet(APIView):
    def post(self, request, *args, **kwargs):
        # value = request.data.get('permanent_user_id')
        print(request.data)
        # Check if 'id' is present in request data
        if 'permanent_user_id' in request.data:
            # Get the instance to update
            instance_id = request.data.get('permanent_user_id')  # Remove 'id' from data
            try:
                instance = Address.objects.get(permanent_user_id=instance_id)
                print(instance)
                instance.permanent_user_id = None
                instance.save()
                
                serializer = AddressSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=201)
                return Response(serializer.errors, status=400)
            except Address.DoesNotExist:
                serializer = AddressSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=201)
                return Response(serializer.errors, status=400)
        else:
            serializer = AddressSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)

                

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
    
class FootballCoachEndorsementRequestViewSet(viewsets.ModelViewSet):
    queryset = FootballCoachEndorsementRequest.objects.all()
    serializer_class = FootballCoachEndorsementRequestSerializer
    
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

class MyNetworkRequestAPIView(APIView):
    def post(self, request, *args, **kwargs):  
        serializer = MyNetworkRequestSerializer(data=request.data)
        if serializer.is_valid():
            user_instance = serializer.save()
            print(user_instance)
            user = CustomUser.objects.get(email=user_instance.from_user)
            network_request = [{
                'connect_to_user': user.id,
                'status': 'pending',
                'user_id': user_instance.to_user,
                'network_request_id': user_instance.id,
                'network_request_send_by': user.id,
            }, {
                'connect_to_user': user_instance.to_user,
                'status': 'pending',
                'user_id': user.id,
                'network_request_id': user_instance.id,
                'network_request_send_by': user.id
            }]
            print(network_request)
            network_connections_serializer = NetworkConnectionsSerializer(data=network_request, many=True)
            if network_connections_serializer.is_valid():
                network_connections_serializer.save()
                return Response({'message': 'data saved successfully'}, status=201)
        return Response(serializer.errors, status=400)
    
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
    
class FootballClubLicenseCreateModelAPIView(APIView):
    def post(self, request, *args, **kwargs):
        value = request.data.get('license_id')
        # Check if 'id' is present in request data
        if value != '':
            # If 'id' is present, it's an update operation
            # return self.update(request, *args, **kwargs)
            serializer = FootballClubVerificationDocumentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        else:
                data = request.data
        
                # Separate the data based on the models
                license_data = {key: data[key] for key in ['license_name']}
                club_data = {key: data[key] for key in ['license_id', 'document_type', 'document_name', 'document_file', 'club_id']}
                # And so on...

                # Serialize the data for each model
                license_serializer = SportLicenseSerializer(data=license_data)

                # Validate the data for each model
                if license_serializer.is_valid():
                    license_instance = license_serializer.save()
                        
                    # Extract 'id' from model1_instance
                    license_id = license_instance.id
                        
                    # Assign id to the appropriate field in Model2
                    club_data['license_id'] = license_id    
                    club_serializer = FootballClubVerificationDocumentSerializer(data=club_data)
                    if club_serializer.is_valid():
                        club_serializer.save()
                
                        # Return any relevant data or success message
                        return Response({"message": "Data saved successfully"}, status=201)
                    else:
                        errors = {}
                        errors['club_errors'] = club_serializer.errors
                            
                        return Response(errors, status=400)
                else:
                    # If any serializer data is invalid, return errors
                    errors = {}
                    if not license_serializer.is_valid():
                        errors['license_errors'] = license_serializer.errors
                
                    return Response(errors, status=400)

class FootballClubLicenseUpdateModelAPIView(APIView):
    def post(self, request, *args, **kwargs):
        value = request.data.get('license_id')
        # Check if 'id' is present in request data
        if value != '':
            # If 'id' is present, it's an update operation
            return self.update(request, *args, **kwargs)
        else:
                data = request.data
        
                # Separate the data based on the models
                license_data = {key: data[key] for key in ['license_name']}
                club_data = {key: data[key] for key in ['id', 'license_id', 'document_type', 'document_name', 'document_file', 'club_id']}
                # And so on...

                # Serialize the data for each model
                license_serializer = SportLicenseSerializer(data=license_data)

                # Validate the data for each model
                if license_serializer.is_valid():
                    license_instance = license_serializer.save()
                
                    # Extract 'id' from model1_instance
                    license_id = license_instance.id
                        
                    # Assign id to the appropriate field in Model2
                    club_data['license_id'] = license_id 
            
                    # Get the instance to update
                    instance_id = request.data.get('id')  # Remove 'id' from data
                    try:
                        instance = FootballClubVerificationDocument.objects.get(pk=instance_id)
                    except FootballClubVerificationDocument.DoesNotExist:
                        return Response({"error": "Instance does not exist"}, status=404)

                    # Update the instance
                    serializer = FootballClubVerificationDocumentSerializer(instance, data=club_data)
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

    def update(self, request, *args, **kwargs):
        # Get the instance to update
        instance_id = request.data.get('id')  # Remove 'id' from data
        try:
            instance = FootballClubVerificationDocument.objects.get(pk=instance_id)
        except FootballClubVerificationDocument.DoesNotExist:
            return Response({"error": "Instance does not exist"}, status=404)

        # Update the instance
        serializer = FootballClubVerificationDocumentSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
class FootballClubHistoryCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Assuming the request data contains a 'type' field indicating the model
        career_history = request.data
        flag = career_history.get('flag')

        if flag == 'createleague':
            data = career_history

            # Separate the data based on the models
            league_data = {key: data[key] for key in ['league_name']}
            club_data = {key: data[key] for key in ['from_year', 'to_year', 'league_id', 'league_name', 'games_played', 'games_won', 'games_lost', 'games_tied', 'points', 'position', 'tournament', 'achievement', 'club_id']}
            # And so on...

            # Serialize the data for each model
            league_serializer = LeagueSerializer(data=league_data)
            # And so on...

            # Validate the data for each model
            if league_serializer.is_valid():
                league_instance = league_serializer.save()
                
                # Extract 'id' from model1_instance
                league_id = league_instance.id
                
                # Assign id to the appropriate field in Model2
                club_data['league_id'] = league_id    
                club_serializer = FootballClubHistorySerializer(data=club_data)
                if club_serializer.is_valid():
                    club_serializer.save()
                    
                    return Response({"message": "Data saved successfully"}, status=201)
                else:
                    errors = {}
                    errors['club_errors'] = club_serializer.errors
                    
                    return Response(errors, status=400)
            else:
                # If any serializer data is invalid, return errors
                errors = {}
                if not league_serializer.is_valid():
                    errors['league_errors'] = league_serializer.errors
        
                return Response(errors, status=400)
        else:
            data = career_history
            # career_history = request.data.get('career_history')
            club_data = {key: data[key] for key in ['from_year', 'to_year', 'league_id', 'league_name', 'games_played', 'games_won', 'games_lost', 'games_tied', 'points', 'position', 'tournament', 'achievement', 'club_id']}
            club_serializer = FootballClubHistorySerializer(data=club_data)
            if club_serializer.is_valid():
                club_serializer.save()
                return Response({"message": "Data saved successfully"}, status=201)
        
            return Response(club_serializer.errors, status=400)
        
class FootballClubHistoryUpdateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Assuming the request data contains a 'type' field indicating the model
        career_history = request.data
        flag = career_history.get('flag')

        if flag == 'createleague':
            data = career_history

            # Separate the data based on the models
            league_data = {key: data[key] for key in ['league_name']}
            club_data = {key: data[key] for key in ['from_year', 'to_year', 'league_id', 'league_name', 'games_played', 'games_won', 'games_lost', 'games_tied', 'points', 'position', 'tournament', 'achievement']}
            # And so on...

            # Serialize the data for each model
            league_serializer = LeagueSerializer(data=league_data)

            # Validate the data for each model
            if league_serializer.is_valid():
                # Perform any additional processing or actions as needed
                # For example, save the data to the respective models
                
                league_instance = league_serializer.save()
                
                # Extract 'id' from model1_instance
                league_id = league_instance.id
                
                # Assign id to the appropriate field in Model2
                club_data['league_id'] = league_id  
    
                # Get the instance to update
                instance_id = data.get('id')  # Remove 'id' from data
                try:
                    instance = FootballClubHistory.objects.get(pk=instance_id)
                except FootballClubHistory.DoesNotExist:
                    return Response({"error": "Instance does not exist"}, status=404)

                # Update the instance
                club_serializer = FootballClubHistorySerializer(instance, data=club_data)
                if club_serializer.is_valid():
                    # player_career_history_instance = player_serializer.save()
                    club_serializer.save()
                                
                    return Response({"message": "Data saved successfully"}, status=201)
                return Response(club_serializer.errors, status=400)
            else:
                # If any serializer data is invalid, return errors
                errors = {}
                if not league_serializer.is_valid():
                    errors['league_errors'] = league_serializer.errors
        
                return Response(errors, status=400)
            
        else:
            data = career_history
            club_data = {key: data[key] for key in ['from_year', 'to_year', 'league_id', 'league_name', 'games_played', 'games_won', 'games_lost', 'games_tied', 'points', 'position', 'tournament', 'achievement']}
            # Get the instance to update
            instance_id = data.get('id')  # Remove 'id' from data
            try:
                instance = FootballClubHistory.objects.get(pk=instance_id)
            except FootballClubHistory.DoesNotExist:
                return Response({"error": "Instance does not exist"}, status=404)
            
            club_serializer = FootballClubHistorySerializer(instance, data=club_data)
            if club_serializer.is_valid():
                club_serializer.save()
                return Response({"message": "Data saved successfully"}, status=201)
        
            return Response(club_serializer.errors, status=400)
                
class FootballClubLicenseViewSet(viewsets.ModelViewSet):
    queryset = FootballClubVerificationDocument.objects.all()
    serializer_class = FootballClubVerificationDocumentSerializer

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
   
class AllUserFilter(filters.FilterSet):
    full_name = CharFilter(method='filter_by_full_name')
    
    class Meta:
        model = CustomUser
        fields = ['full_name']
        
    # def filter_by_full_name(self, queryset, name, value):
    #     return queryset.filter(Q(first_name__icontains=value) | Q(last_name__icontains=value) | Q(email__icontains=value) | Q(account_type__icontains='user') | Q(is_flag__icontains=True))
    
    def filter_by_full_name(self, queryset, name, value):
        # Filter where first_name is not null and apply the full_name filter logic
        return queryset.exclude(first_name__isnull=True).exclude(account_type='institute').exclude(is_superuser=True).exclude(is_flag=False).filter(
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(email__icontains=value)
        )
   
class AllUserSearchViewSet(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AllUserFilter


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
    user__email = CharFilter(field_name='user__email', lookup_expr='icontains')
    user__dob = filters.DateFromToRangeFilter(field_name='user__dob')
    # age = NumberFilter(method='filter_by_age')
    # user__min_age = NumberFilter(field_name='user__dob', lookup_expr='year__gte')
    # user__max_age = NumberFilter(field_name='user__dob', lookup_expr='year__lte')
    user__full_name = CharFilter(method='filter_by_full_name')

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
            'user__last_name',
            'user__email',
            'user__full_name'
        )
        
    # def filter_by_full_name(self, queryset, name, value):
    #     return queryset.filter(Q(user__first_name__icontains=value) | Q(user__last_name__icontains=value) | Q(user__email__icontains=value))
    
    def filter_by_full_name(self, queryset, name, value):
        # Filter where first_name is not null and apply the full_name filter logic
        return queryset.exclude(user__first_name__isnull=True).exclude(user__account_type='institute').exclude(user__is_superuser=True).exclude(user__is_flag=False).filter(
            Q(user__first_name__icontains=value) |
            Q(user__last_name__icontains=value) |
            Q(user__email__icontains=value)
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
    user__full_name = CharFilter(method='filter_by_full_name')

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
            'user__dob',
            'user__full_name'
        )
        
    # def filter_by_full_name(self, queryset, name, value):
    #     return queryset.filter(Q(user__first_name__icontains=value) | Q(user__last_name__icontains=value) | Q(user__email__icontains=value))
    
    def filter_by_full_name(self, queryset, name, value):
        # Filter where first_name is not null and apply the full_name filter logic
        return queryset.exclude(user__first_name__isnull=True).exclude(user__account_type='institute').exclude(user__is_superuser=True).exclude(user__is_flag=False).filter(
            Q(user__first_name__icontains=value) |
            Q(user__last_name__icontains=value) |
            Q(user__email__icontains=value)
        )
        
        
class CoachSearchViewSet(ListAPIView):
    queryset = FootballCoach.objects.all()
    serializer_class = GetFootballCoachSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CoachFilter

class AgentFilter(filters.FilterSet):
    user__first_name = CharFilter(field_name='user__first_name', lookup_expr='icontains')
    user__last_name = CharFilter(field_name='user__last_name', lookup_expr='icontains')
    user__sport_type = CharFilter(field_name='user__sport_type', lookup_expr='icontains')
    user__full_name = CharFilter(method='filter_by_full_name')
    
    class Meta:
        model = Agent
        fields = (
            'user__first_name',
            'user__last_name',
            'user__sport_type',
            'user__full_name'
        )
        # filter_overrides = {
        #     models.CharField: {
        #         'filter_class': filters.CharFilter,
        #         'extra': lambda f: {
        #             'lookup_expr': 'icontains',
        #         },
        #     },
        # }
        
    # def filter_by_full_name(self, queryset, name, value):
    #     return queryset.filter(Q(user__first_name__icontains=value) | Q(user__last_name__icontains=value) | Q(user__email__icontains=value))
    
    def filter_by_full_name(self, queryset, name, value):
        return queryset.exclude(user__first_name__isnull=True).exclude(user__account_type='institute').exclude(user__is_superuser=True).exclude(user__is_flag=False).filter(
            Q(user__first_name__icontains=value) |
            Q(user__last_name__icontains=value) |
            Q(user__email__icontains=value)
        )

class AgentSearchViewSet(ListAPIView):
    queryset = Agent.objects.all()
    serializer_class = GetAgentSerializer
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
        from_user=request.data['from']
        # email_body=request.data['message']
        absurl = settings.BASE_URL+'login'
        email_body = 'Hello sir/madam,\nYou have an invitation request from BSCOUTD sent by ' + from_user + '\nUse the link below to register\n' + absurl
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
    
class FootballPlayerEndorsementRequestViewSet(viewsets.ModelViewSet):
    queryset = FootballPlayerEndorsementRequest.objects.all()
    serializer_class = FootballPlayerEndorsementRequestSerializer
    
class GetFootballPlayerEndorsementRequestViewSet(viewsets.ModelViewSet):
    queryset = FootballPlayerEndorsementRequest.objects.all()
    serializer_class = GetPlayerEndorsementRequestSerializer

class GetFootballCoachEndorsementRequestViewSet(viewsets.ModelViewSet):
    queryset = FootballCoachEndorsementRequest.objects.all()
    serializer_class = GetCoachEndorsementRequestSerializer
    
class MultiModelCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Assuming the request data contains a 'type' field indicating the model
        career_history = request.data.get('career_history')
        data_type = career_history.get('flag')
        # print(data_type)

        if data_type == 'league':
            data = career_history
            
            # Separate the data based on the models
            league_data = {key: data[key] for key in ['sport_type', 'league_name', 'league_type']}
            player_data = {key: data[key] for key in ['club_id', 'club_name', 'from_year', 'to_year', 'games_played', 'club_goals', 'club_assists', 'club_passes', 'club_saved_goals', 'interceptions_per_game', 'takles_per_game', 'shots_per_game', 'key_passes_per_game', 'dribles_completed_per_game', 'clean_sheets_per_game', 'club_yellow_card', 'club_red_card', 'league_id', 'league_name', 'country_name', 'league_type', 'achievements', 'summary', 'players']}
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
                player_serializer = ClubSerializer(data=player_data)
                if player_serializer.is_valid():
                    player_career_history_instance = player_serializer.save()

                    endorsement_request = request.data.get('endorsement_request')
                    if(endorsement_request!=''):
                        print(endorsement_request) 
                        if isinstance(endorsement_request, list):
                            endorsement_request_serializer = FootballPlayerEndorsementRequestSerializer(data=endorsement_request, many=True)
                            if endorsement_request_serializer.is_valid():
                                for item_data in endorsement_request_serializer.validated_data:
                                    # print(item_data['to_endorser'])
                                    if item_data['to_endorser'] is None:  
                                        return Response({'error':'No user found with this email.'}, status=status.HTTP_400_BAD_REQUEST)
                                    else:
                                        item_data['player_career_history'] = player_career_history_instance
                                            
                                        # my_object = CustomUser.objects.get(email=item_data['to_endorser_email'])
                                        my_object = CustomUser.objects.get(email=item_data['to_endorser'])
                                            
                                        endorsee = CustomUser.objects.get(email=item_data['from_endorsee'])
                                            
                                        absurl = settings.BASE_URL+'endorsements/pending'
                                        email_body = 'Hi '+ my_object.first_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '.\nUse the link below to check the endorsement request\n' + absurl
                                        data = {'email_body': email_body, 'to_email': my_object.email,
                                                        'email_subject': 'Endorsement Request'}

                                        Util.send_email(data)
                                            
                                try:
                                    with transaction.atomic():
                                        FootballPlayerEndorsementRequest.objects.bulk_create([
                                            FootballPlayerEndorsementRequest(**item) for item in endorsement_request_serializer.validated_data
                                        ])
                                        # serializer.save()
                                            
                                    # return Response(endorsement_request_serializer.data, status=status.HTTP_200_OK)
                                            
                                    # return self.update(request, *args, **kwargs)
                                except Exception as e:
                                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                            else:
                                return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({"error": "Expected a list of items"}, status=status.HTTP_400_BAD_REQUEST)
                            
                    endorsement_request_to_club = request.data.get('endorsement_request_to_club')
                    if(endorsement_request_to_club != ''):
                        print(endorsement_request_to_club) 
                        endorsement_request_serializer = FootballPlayerEndorsementRequestSerializer(data=endorsement_request_to_club)
                        if endorsement_request_serializer.is_valid():
                            endorsement_request_serializer.validated_data['player_career_history'] = player_career_history_instance
                                
                            register_id = endorsement_request_to_club.get('reg_id')  
                            from_endorsee = endorsement_request_to_club.get('from_endorsee')  
                            try:          
                                my_object = CustomUser.objects.get(reg_id=register_id)
                                endorsement_request_serializer.validated_data['to_endorser'] = my_object 
                                    
                                endorsee = CustomUser.objects.get(id=from_endorsee)
                                    
                                absurl = settings.BASE_URL+'endorsements/pending'
                                email_body = 'Hi '+ my_object.club_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '\nUse the link below to check the endorsement request\n' + absurl
                                data = {'email_body': email_body, 'to_email': my_object.email, 'email_subject': 'Endorsement Request'}

                                Util.send_email(data)
                                                
                                endorsement_request_serializer.save() 
                                return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK) 
                            except CustomUser.DoesNotExist:  
                                return Response({'error':'Club does not exist'}, status=status.HTTP_401_UNAUTHORIZED)     
                        else:
                            return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
                            
                    return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response(player_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                # If any serializer data is invalid, return errors
                errors = {}
                if not league_serializer.is_valid():
                    errors['league_errors'] = league_serializer.errors
                
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            
        elif data_type == 'leaguenull':
            data = career_history
            
            # Separate the data based on the models
            # league_data = {key: data[key] for key in ['sport_type', 'league_name', 'league_type']}
            player_data = {key: data[key] for key in ['club_id', 'club_name', 'from_year', 'to_year', 'games_played', 'club_goals', 'club_assists', 'club_passes', 'club_saved_goals', 'interceptions_per_game', 'takles_per_game', 'shots_per_game', 'key_passes_per_game', 'dribles_completed_per_game', 'clean_sheets_per_game', 'club_yellow_card', 'club_red_card', 'country_name', 'league_type', 'achievements', 'summary', 'players']}
            # And so on...

            player_serializer = ClubSerializer(data=player_data)
            if player_serializer.is_valid():
                player_career_history_instance = player_serializer.save()

                endorsement_request = request.data.get('endorsement_request')
                if(endorsement_request!=''):
                    if isinstance(endorsement_request, list):
                        endorsement_request_serializer = FootballPlayerEndorsementRequestSerializer(data=endorsement_request, many=True)
                        if endorsement_request_serializer.is_valid():
                            for item_data in endorsement_request_serializer.validated_data:
                                # print(item_data['to_endorser'])
                                if item_data['to_endorser'] is None:  
                                    return Response({'error':'No user found with this email.'}, status=status.HTTP_400_BAD_REQUEST)
                                else:
                                    item_data['player_career_history'] = player_career_history_instance
                                            
                                    # my_object = CustomUser.objects.get(email=item_data['to_endorser_email'])
                                    my_object = CustomUser.objects.get(email=item_data['to_endorser'])
                                            
                                    endorsee = CustomUser.objects.get(email=item_data['from_endorsee'])
                                            
                                    absurl = settings.BASE_URL+'endorsements/pending'
                                    email_body = 'Hi '+ my_object.first_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '.\nUse the link below to check the endorsement request\n' + absurl
                                    data = {'email_body': email_body, 'to_email': my_object.email,
                                                        'email_subject': 'Endorsement Request'}

                                    Util.send_email(data)       
                            try:
                                with transaction.atomic():
                                    FootballPlayerEndorsementRequest.objects.bulk_create([
                                        FootballPlayerEndorsementRequest(**item) for item in endorsement_request_serializer.validated_data
                                    ])
                            except Exception as e:
                                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({"error": "Expected a list of items"}, status=status.HTTP_400_BAD_REQUEST) 
                                
                endorsement_request_to_club = request.data.get('endorsement_request_to_club')
                if(endorsement_request_to_club != ''):
                    print(endorsement_request_to_club) 
                    endorsement_request_serializer = FootballPlayerEndorsementRequestSerializer(data=endorsement_request_to_club)
                    if endorsement_request_serializer.is_valid():
                        endorsement_request_serializer.validated_data['player_career_history'] = player_career_history_instance
                                
                        register_id = endorsement_request_to_club.get('reg_id')  
                        from_endorsee = endorsement_request_to_club.get('from_endorsee')  
                        try:          
                            my_object = CustomUser.objects.get(reg_id=register_id)
                            endorsement_request_serializer.validated_data['to_endorser'] = my_object 
                                    
                            endorsee = CustomUser.objects.get(id=from_endorsee)
                                    
                            absurl = settings.BASE_URL+'endorsements/pending'
                            email_body = 'Hi '+ my_object.club_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '\nUse the link below to check the endorsement request\n' + absurl
                            data = {'email_body': email_body, 'to_email': my_object.email, 'email_subject': 'Endorsement Request'}

                            Util.send_email(data)
                                                
                            endorsement_request_serializer.save() 
                            return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK) 
                        except CustomUser.DoesNotExist:  
                            return Response({'error':'Club does not exist'}, status=status.HTTP_401_UNAUTHORIZED)     
                    else:
                        return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                                        
                return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK)
            else:
                errors = {}
                errors['player_errors'] = player_serializer.errors
                        
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            
        elif data_type == 'team':
            # Get the data sent through HTTP POST
            # career_history = request.data.get('career_history')
            data = career_history
            
            # if 'league_id' in data:
            #     # If 'id' is present, it's an update operation
            #     flag=1
            #     league_id = data.get('league_id')
            #     sport_type = data.get('sport_type')
            #     print(league_id)
            #     # league_data = {key: data[key] for key in ['sport_type', 'league_name', 'league_type']}
            #     my_object = League.objects.get(id=league_id)
            #     print(my_object.sport_type)
            #     substrings = my_object.sport_type.split(',')
            #     print(f"Substrings are {substrings}")
            #     for substring in substrings:
            #         print(f"Sport type: {sport_type} found in the list.")
            #         if(substring.lower() == sport_type.lower()):
            #             print(f"Substring: {substring} found in the list.")
            #             flag = 0
            #     if(flag == 1):
            #         my_object.sport_type = my_object.sport_type + "," + sport_type
            #         print(my_object.sport_type)
            #         my_object.save()

            # Separate the data based on the models
            team_data = {key: data[key] for key in ['club_name', 'reg_id', 'country_name', 'sport_type']}
            player_data = {key: data[key] for key in ['club_id', 'club_name', 'from_year', 'to_year', 'games_played', 'club_goals', 'club_assists', 'club_passes', 'club_saved_goals', 'interceptions_per_game', 'takles_per_game', 'shots_per_game', 'key_passes_per_game', 'dribles_completed_per_game', 'clean_sheets_per_game', 'club_yellow_card', 'club_red_card', 'league_id', 'league_name', 'country_name', 'league_type', 'achievements', 'summary', 'players']}
            # And so on...

            # Serialize the data for each model
            team_serializer = TeamSerializer(data=team_data)

            # Validate the data for each model
            if team_serializer.is_valid():
                team_instance = team_serializer.save()
                
                # Extract 'id' from model1_instance
                team_id = team_instance.reg_id
                
                # Assign id to the appropriate field in Model2
                player_data['club_id'] = team_id    
                player_serializer = ClubSerializer(data=player_data)
                if player_serializer.is_valid():
                    player_career_history_instance = player_serializer.save()
                    endorsement_request = request.data.get('endorsement_request')
                    if(endorsement_request!=''):
                        if isinstance(endorsement_request, list):
                            endorsement_request_serializer = FootballPlayerEndorsementRequestSerializer(data=endorsement_request, many=True)
                            if endorsement_request_serializer.is_valid():
                                for item_data in endorsement_request_serializer.validated_data:
                                    # print(item_data['to_endorser'])
                                    if item_data['to_endorser'] is None:  
                                        return Response({'error':'No user found with this email.'}, status=status.HTTP_400_BAD_REQUEST)
                                    else:
                                        item_data['player_career_history'] = player_career_history_instance
                                            
                                        # my_object = CustomUser.objects.get(email=item_data['to_endorser_email'])
                                        my_object = CustomUser.objects.get(email=item_data['to_endorser'])
                                            
                                        endorsee = CustomUser.objects.get(email=item_data['from_endorsee'])
                                        
                                        absurl = settings.BASE_URL+'endorsements/pending'
                                        email_body = 'Hi '+ my_object.first_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '.\nUse the link below to check the endorsement request\n' + absurl
                                        data = {'email_body': email_body, 'to_email': my_object.email,
                                                        'email_subject': 'Endorsement Request'}

                                        Util.send_email(data)
                                            
                                try:
                                    with transaction.atomic():
                                        FootballPlayerEndorsementRequest.objects.bulk_create([
                                            FootballPlayerEndorsementRequest(**item) for item in endorsement_request_serializer.validated_data
                                        ])
                                        # serializer.save()
                                            
                                    return Response(endorsement_request_serializer.data, status=status.HTTP_200_OK)
                                            
                                    # return self.update(request, *args, **kwargs)
                                except Exception as e:
                                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                            else:
                                return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({"error": "Expected a list of items"}, status=status.HTTP_400_BAD_REQUEST)  
                                  
                    # endorsement_request_to_club = request.data.get('endorsement_request_to_club')
                    # if(endorsement_request_to_club != ''):
                    #     print(endorsement_request_to_club) 
                    #     endorsement_request_serializer = FootballPlayerEndorsementRequestSerializer(data=endorsement_request_to_club)
                    #     if endorsement_request_serializer.is_valid():
                    #         endorsement_request_serializer.validated_data['player_career_history'] = player_career_history_instance
                            
                    #         register_id = endorsement_request_to_club.get('reg_id')  
                    #         from_endorsee = endorsement_request_to_club.get('from_endorsee')  
                    #         try:          
                    #             my_object = CustomUser.objects.get(reg_id=register_id)
                    #             endorsement_request_serializer.validated_data['to_endorser'] = my_object 
                                
                    #             endorsee = CustomUser.objects.get(id=from_endorsee)
                                
                    #             absurl = settings.BASE_URL+'endorsements/pending'
                    #             email_body = 'Hi '+ my_object.club_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '\nUse the link below to check the endorsement request\n' + absurl
                    #             data = {'email_body': email_body, 'to_email': my_object.email, 'email_subject': 'Endorsement Request'}

                    #             Util.send_email(data)
                                            
                    #             endorsement_request_serializer.save() 
                    #             return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK) 
                    #         except CustomUser.DoesNotExist:  
                    #             return Response({'error':'Club does not exist'}, status=status.HTTP_401_UNAUTHORIZED)     
                    #     else:
                    #         return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                                       
                    return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response(player_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                # If any serializer data is invalid, return errors
                errors = {}
                if not team_serializer.is_valid():
                    errors['team_errors'] = team_serializer.errors
               
                return Response(errors, status=400)
            
        elif data_type == 'teamleaguenull':
            # Get the data sent through HTTP POST
            # career_history = request.data.get('career_history')
            data = career_history
            # club_id = endorsement_request_to_club.get('club_id')
            
            # if 'league_id' in data:
            #     # If 'id' is present, it's an update operation
            #     flag=1
            #     league_id = data.get('league_id')
            #     sport_type = data.get('sport_type')
            #     print(league_id)
            #     # league_data = {key: data[key] for key in ['sport_type', 'league_name', 'league_type']}
            #     my_object = League.objects.get(id=league_id)
            #     print(my_object.sport_type)
            #     substrings = my_object.sport_type.split(',')
            #     print(f"Substrings are {substrings}")
            #     for substring in substrings:
            #         print(f"Sport type: {sport_type} found in the list.")
            #         if(substring.lower() == sport_type.lower()):
            #             print(f"Substring: {substring} found in the list.")
            #             flag = 0
            #     if(flag == 1):
            #         my_object.sport_type = my_object.sport_type + "," + sport_type
            #         print(my_object.sport_type)
            #         my_object.save()

            # Separate the data based on the models
            team_data = {key: data[key] for key in ['club_name', 'reg_id', 'country_name', 'sport_type']}
            player_data = {key: data[key] for key in ['club_id', 'club_name', 'from_year', 'to_year', 'games_played', 'club_goals', 'club_assists', 'club_passes', 'club_saved_goals', 'interceptions_per_game', 'takles_per_game', 'shots_per_game', 'key_passes_per_game', 'dribles_completed_per_game', 'clean_sheets_per_game', 'club_yellow_card', 'club_red_card', 'country_name', 'league_type', 'achievements', 'summary', 'players']}
            # And so on...

            # Serialize the data for each model
            team_serializer = TeamSerializer(data=team_data)

            # Validate the data for each model
            if team_serializer.is_valid():
                team_instance = team_serializer.save()
                    
                # Extract 'id' from model1_instance
                team_id = team_instance.reg_id
                    
                # Assign id to the appropriate field in Model2
                player_data['club_id'] = team_id    
                player_serializer = ClubSerializer(data=player_data)
                if player_serializer.is_valid():
                    player_career_history_instance = player_serializer.save()
                    endorsement_request = request.data.get('endorsement_request')
                    if(endorsement_request!=''):
                        if isinstance(endorsement_request, list):
                            endorsement_request_serializer = FootballPlayerEndorsementRequestSerializer(data=endorsement_request, many=True)
                            if endorsement_request_serializer.is_valid():
                                for item_data in endorsement_request_serializer.validated_data:
                                    # print(item_data['to_endorser'])
                                    if item_data['to_endorser'] is None:  
                                        return Response({'error':'No user found with this email.'}, status=status.HTTP_400_BAD_REQUEST)
                                    else:
                                        item_data['player_career_history'] = player_career_history_instance
                                                
                                        # my_object = CustomUser.objects.get(email=item_data['to_endorser_email'])
                                        my_object = CustomUser.objects.get(email=item_data['to_endorser'])
                                                
                                        endorsee = CustomUser.objects.get(email=item_data['from_endorsee'])
                                            
                                        absurl = settings.BASE_URL+'endorsements/pending'
                                        email_body = 'Hi '+ my_object.first_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '.\nUse the link below to check the endorsement request\n' + absurl
                                        data = {'email_body': email_body, 'to_email': my_object.email,
                                                            'email_subject': 'Endorsement Request'}

                                        Util.send_email(data)
                                                
                                try:
                                    with transaction.atomic():
                                        FootballPlayerEndorsementRequest.objects.bulk_create([
                                            FootballPlayerEndorsementRequest(**item) for item in endorsement_request_serializer.validated_data
                                        ])
                                        # serializer.save()
                                                
                                    return Response(endorsement_request_serializer.data, status=status.HTTP_200_OK)
                                                
                                    # return self.update(request, *args, **kwargs)
                                except Exception as e:
                                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                            else:    
                                return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({"error": "Expected a list of items"}, status=status.HTTP_400_BAD_REQUEST)   
                                    
                    # endorsement_request_to_club = request.data.get('endorsement_request_to_club')
                    # if(endorsement_request_to_club != ''):
                    #     print(endorsement_request_to_club) 
                    #     endorsement_request_serializer = FootballPlayerEndorsementRequestSerializer(data=endorsement_request_to_club)
                    #     if endorsement_request_serializer.is_valid():
                    #         endorsement_request_serializer.validated_data['player_career_history'] = player_career_history_instance
                                
                    #         register_id = endorsement_request_to_club.get('reg_id')  
                    #         from_endorsee = endorsement_request_to_club.get('from_endorsee')  
                    #         try:          
                    #             my_object = CustomUser.objects.get(reg_id=register_id)
                    #             endorsement_request_serializer.validated_data['to_endorser'] = my_object 
                                    
                    #             endorsee = CustomUser.objects.get(id=from_endorsee)
                                    
                    #             absurl = settings.BASE_URL+'endorsements/pending'
                    #             email_body = 'Hi '+ my_object.club_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '\nUse the link below to check the endorsement request\n' + absurl
                    #             data = {'email_body': email_body, 'to_email': my_object.email, 'email_subject': 'Endorsement Request'}

                    #             Util.send_email(data)
                                                
                    #             endorsement_request_serializer.save() 
                    #             return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK) 
                    #         except CustomUser.DoesNotExist:  
                    #             return Response({'error':'Club does not exist'}, status=status.HTTP_401_UNAUTHORIZED) 
                    #     else:
                    #         return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
                                            
                    return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response(player_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                # If any serializer data is invalid, return errors
                errors = {}
                if not team_serializer.is_valid():
                    errors['team_errors'] = team_serializer.errors
                
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif data_type == 'teamleague':
             # Get the data sent through HTTP POST
            # career_history = request.data.get('career_history')
            data = career_history

            # Separate the data based on the models
            league_data = {key: data[key] for key in ['sport_type', 'league_name', 'league_type']}
            team_data = {key: data[key] for key in ['club_name', 'reg_id', 'country_name', 'sport_type']}
            player_data = {key: data[key] for key in ['club_id', 'club_name', 'from_year', 'to_year', 'games_played', 'club_goals', 'club_assists', 'club_passes', 'club_saved_goals', 'interceptions_per_game', 'takles_per_game', 'shots_per_game', 'key_passes_per_game', 'dribles_completed_per_game', 'clean_sheets_per_game', 'club_yellow_card', 'club_red_card', 'league_id', 'league_name', 'country_name', 'league_type', 'achievements', 'summary', 'players']}

            # Serialize the data for each model
            league_serializer = LeagueSerializer(data=league_data)
            team_serializer = TeamSerializer(data=team_data)

            # Validate the data for each model
            if team_serializer.is_valid() and league_serializer.is_valid():
                team_instance = team_serializer.save()
                league_instance = league_serializer.save()
                
                # Extract 'id' from model1_instance
                team_id = team_instance.reg_id
                league_id = league_instance.id
                
                # Assign id to the appropriate field in Model2
                player_data['club_id'] = team_id    
                player_data['league_id'] = league_id    
                player_serializer = ClubSerializer(data=player_data)
                if player_serializer.is_valid():
                    player_career_history_instance = player_serializer.save()
                    endorsement_request = request.data.get('endorsement_request')
                    if(endorsement_request!=''):
                        if isinstance(endorsement_request, list):
                            endorsement_request_serializer = FootballPlayerEndorsementRequestSerializer(data=endorsement_request, many=True)
                            if endorsement_request_serializer.is_valid():
                                for item_data in endorsement_request_serializer.validated_data:
                                    # print(item_data['to_endorser'])
                                    if item_data['to_endorser'] is None:  
                                        return Response({'error':'No user found with this email.'}, status=status.HTTP_400_BAD_REQUEST)
                                    else:
                                        item_data['player_career_history'] = player_career_history_instance
                                            
                                        # my_object = CustomUser.objects.get(email=item_data['to_endorser_email'])
                                        my_object = CustomUser.objects.get(email=item_data['to_endorser'])
                                            
                                        endorsee = CustomUser.objects.get(email=item_data['from_endorsee'])
                                        
                                        absurl = settings.BASE_URL+'endorsements/pending'
                                        email_body = 'Hi '+ my_object.first_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '.\nUse the link below to check the endorsement request\n' + absurl
                                        data = {'email_body': email_body, 'to_email': my_object.email,
                                                        'email_subject': 'Endorsement Request'}

                                        Util.send_email(data)
                                            
                                try:
                                    with transaction.atomic():
                                        FootballPlayerEndorsementRequest.objects.bulk_create([
                                            FootballPlayerEndorsementRequest(**item) for item in endorsement_request_serializer.validated_data
                                        ])
                                        # serializer.save()
                                            
                                    return Response(endorsement_request_serializer.data, status=status.HTTP_200_OK)
                                            
                                    # return self.update(request, *args, **kwargs)
                                except Exception as e:
                                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                            else:    
                                return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({"error": "Expected a list of items"}, status=status.HTTP_400_BAD_REQUEST) 
                                   
                    # endorsement_request_to_club = request.data.get('endorsement_request_to_club')
                    # if(endorsement_request_to_club != ''):
                    #     print(endorsement_request_to_club) 
                    #     endorsement_request_serializer = FootballPlayerEndorsementRequestSerializer(data=endorsement_request_to_club)
                    #     if endorsement_request_serializer.is_valid():
                    #         endorsement_request_serializer.validated_data['player_career_history'] = player_career_history_instance
                            
                    #         register_id = endorsement_request_to_club.get('reg_id')  
                    #         from_endorsee = endorsement_request_to_club.get('from_endorsee')  
                    #         try:          
                    #             my_object = CustomUser.objects.get(reg_id=register_id)
                    #             endorsement_request_serializer.validated_data['to_endorser'] = my_object 
                                
                    #             endorsee = CustomUser.objects.get(id=from_endorsee)
                                
                    #             absurl = settings.BASE_URL+'endorsements/pending'
                    #             email_body = 'Hi '+ my_object.club_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '\nUse the link below to check the endorsement request\n' + absurl
                    #             data = {'email_body': email_body, 'to_email': my_object.email, 'email_subject': 'Endorsement Request'}

                    #             Util.send_email(data)
                                            
                    #             endorsement_request_serializer.save() 
                    #             return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK) 
                    #         except CustomUser.DoesNotExist:  
                    #             return Response({'error':'Club does not exist'}, status=status.HTTP_401_UNAUTHORIZED)   
                    #     else:
                    #         return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                                         
                    return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response(player_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                # If any serializer data is invalid, return errors
                errors = {}
                if not team_serializer.is_valid():
                    errors['team_errors'] = team_serializer.errors
                if not league_serializer.is_valid():
                    errors['league_errors'] = league_serializer.errors
               
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response({"error": "Invalid data type provided"}, status=status.HTTP_400_BAD_REQUEST)
        

class MultiModelCreateUpdateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # career_history = request.data.get('career_history')
        # Check if 'id' is present in request data
        # if 'league_id' in career_history:
        #     flag=1
        #     league_id = career_history.get('league_id')
        #     sport_type = career_history.get('sport_type')
        #     print(league_id)
        #     my_object = League.objects.get(id=league_id)
        #     print(my_object.sport_type)
        #     substrings = my_object.sport_type.split(',')
        #     print(f"Substrings are {substrings}")
        #     for substring in substrings:
        #         print(f"Sport type: {sport_type} found in the list.")
        #         if(substring.lower() == sport_type.lower()):
        #             print(f"Substring: {substring} found in the list.")
        #             flag = 0
        #     if(flag == 1):
        #         my_object.sport_type = my_object.sport_type + "," + sport_type
        #         print(my_object.sport_type)
        #         my_object.save()
        #     return self.create(request, *args, **kwargs)
        # else:
        #     return self.create(request, *args, **kwargs)

    # def create(self, request, *args, **kwargs):
        career_history = request.data.get('career_history')
        print(career_history)
        club_serializer = ClubSerializer(data=career_history)
        if club_serializer.is_valid():
            player_career_history_instance = club_serializer.save()
                
            endorsement_request = request.data.get('endorsement_request')
            if(endorsement_request != ''):
                print(endorsement_request)
                if isinstance(endorsement_request, list):
                    endorsement_request_serializer = FootballPlayerEndorsementRequestSerializer(data=endorsement_request, many=True)
                    if endorsement_request_serializer.is_valid():
                        for item_data in endorsement_request_serializer.validated_data:
                            if item_data['to_endorser'] is None:  
                                return Response({'error':'No user found with this email.'}, status=status.HTTP_400_BAD_REQUEST)
                            else:
                                item_data['player_career_history'] = player_career_history_instance
                                            
                                # my_object = CustomUser.objects.get(email=item_data['to_endorser_email'])
                                my_object = CustomUser.objects.get(email=item_data['to_endorser'])
                                    
                                endorsee = CustomUser.objects.get(email=item_data['from_endorsee'])
                                            
                                absurl = settings.BASE_URL+'endorsements/pending'
                                email_body = 'Hi '+ my_object.first_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '.\nUse the link below to check the endorsement request\n' + absurl
                                data = {'email_body': email_body, 'to_email': my_object.email,
                                        'email_subject': 'Endorsement Request'}

                                Util.send_email(data)              
                        try:
                            with transaction.atomic():
                                FootballPlayerEndorsementRequest.objects.bulk_create([
                                    FootballPlayerEndorsementRequest(**item) for item in endorsement_request_serializer.validated_data
                                ])
                                            
                            # return Response(endorsement_request_serializer.data, status=status.HTTP_200_OK)
                        except Exception as e:
                            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"error": "Expected a list of items"}, status=status.HTTP_400_BAD_REQUEST) 
                            
            endorsement_request_to_club = request.data.get('endorsement_request_to_club')
            if(endorsement_request_to_club != ''):
                print(endorsement_request_to_club) 
                endorsement_request_serializer = FootballPlayerEndorsementRequestSerializer(data=endorsement_request_to_club)
                if endorsement_request_serializer.is_valid():
                    endorsement_request_serializer.validated_data['player_career_history'] = player_career_history_instance
                        
                    register_id = endorsement_request_to_club.get('reg_id')  
                    from_endorsee = endorsement_request_to_club.get('from_endorsee')  
                    try:          
                        my_object = CustomUser.objects.get(reg_id=register_id)
                        endorsement_request_serializer.validated_data['to_endorser'] = my_object 
                            
                        endorsee = CustomUser.objects.get(id=from_endorsee)
                            
                        absurl = settings.BASE_URL+'endorsements/pending'
                        email_body = 'Hi '+ my_object.club_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '\nUse the link below to check the endorsement request\n' + absurl
                        data = {'email_body': email_body, 'to_email': my_object.email, 'email_subject': 'Endorsement Request'}

                        Util.send_email(data)
                                        
                        endorsement_request_serializer.save() 
                        return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK) 
                    except CustomUser.DoesNotExist:
                        return Response({'error':'Club not registered. You cannot send endorsement request.'}, status=status.HTTP_401_UNAUTHORIZED) 
                else:
                    return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
                                                
            return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK)
            
        return Response(club_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PlayerLeagueModelUpdateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # career_history = request.data.get('career_history')
        # value = career_history.get('league_id')
        # Check if 'id' is present in request data
        # if value != '':
        #     flag=1
        #     league_id = career_history.get('league_id')
        #     sport_type = career_history.get('sport_type')
        #     print(league_id)
        #     my_object = League.objects.get(id=league_id)
        #     print(my_object.sport_type)
        #     # Split the string into multiple substrings based on comma
        #     substrings = my_object.sport_type.split(',')
        #     print(f"Substrings are {substrings}")
        #     for substring in substrings:
        #         print(f"Sport type: {sport_type} found in the list.")
        #         if(substring.lower() == sport_type.lower()):
        #             print(f"Substring: {substring} found in the list.")
        #             flag = 0
        #     if(flag == 1):
        #         my_object.sport_type = my_object.sport_type + "," + sport_type
        #         print(my_object.sport_type)
        #         my_object.save()
        #     return self.update(request, *args, **kwargs)
        # else:
        #     return self.update(request, *args, **kwargs)

    # def update(self, request, *args, **kwargs):
        career_history = request.data.get('career_history')
        # Get the instance to update
        instance_id = career_history.get('id')  # Remove 'id' from data
        try:
            instance = Club.objects.get(pk=instance_id)
        except Club.DoesNotExist:
            return Response({"error": "Instance does not exist"}, status=404)

        # Update the instance
        club_serializer = ClubSerializer(instance, data=career_history)
        if club_serializer.is_valid():
            club_serializer.save()
            
            endorsement_request = request.data.get('endorsement_request')
            if(endorsement_request != ''):
                print(endorsement_request)
                if isinstance(endorsement_request, list):
                    endorsement_request_serializer = FootballPlayerEndorsementRequestSerializer(data=endorsement_request, many=True)
                    if endorsement_request_serializer.is_valid():
                        for item_data in endorsement_request_serializer.validated_data:
                            if item_data['to_endorser'] is None:  
                                return Response({'error':'No user found with this email.'}, status=status.HTTP_400_BAD_REQUEST)
                            else:         
                                my_object = CustomUser.objects.get(email=item_data['to_endorser'])
                                    
                                endorsee = CustomUser.objects.get(email=item_data['from_endorsee'])
                                            
                                absurl = settings.BASE_URL+'endorsements/pending'
                                email_body = 'Hi '+ my_object.first_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '.\nUse the link below to check the endorsement request\n' + absurl
                                data = {'email_body': email_body, 'to_email': my_object.email,
                                        'email_subject': 'Endorsement Request'}

                                Util.send_email(data)              
                        try:
                            with transaction.atomic():
                                FootballPlayerEndorsementRequest.objects.bulk_create([
                                    FootballPlayerEndorsementRequest(**item) for item in endorsement_request_serializer.validated_data
                                ])
                                            
                            # return Response(endorsement_request_serializer.data, status=status.HTTP_200_OK)
                        except Exception as e:
                            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"error": "Expected a list of items"}, status=status.HTTP_400_BAD_REQUEST) 
                            
            endorsement_request_to_club = request.data.get('endorsement_request_to_club')
            if(endorsement_request_to_club != ''):
                print(endorsement_request_to_club)   
                endorsement_request_serializer = FootballPlayerEndorsementRequestSerializer(data=endorsement_request_to_club)
                if endorsement_request_serializer.is_valid():
                    register_id = endorsement_request_to_club.get('reg_id')  
                    from_endorsee = endorsement_request_to_club.get('from_endorsee')  
                    try:          
                        my_object = CustomUser.objects.get(reg_id=register_id)
                        endorsement_request_serializer.validated_data['to_endorser'] = my_object 
                        
                        try:
                            FootballPlayerEndorsementRequest.objects.get(to_endorser=endorsement_request_serializer.validated_data['to_endorser'], type='Club', from_endorsee=from_endorsee)
                            return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK) 
                        
                        except FootballPlayerEndorsementRequest.DoesNotExist:
                            endorsee = CustomUser.objects.get(id=from_endorsee)
                                
                            absurl = settings.BASE_URL+'endorsements/pending'
                            email_body = 'Hi '+ my_object.club_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '\nUse the link below to check the endorsement request\n' + absurl
                            data = {'email_body': email_body, 'to_email': my_object.email, 'email_subject': 'Endorsement Request'}

                            Util.send_email(data)
                                            
                            endorsement_request_serializer.save() 
                            
                            return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK) 
                    
                    except CustomUser.DoesNotExist:
                        return Response({'error':'Club not registered. You cannot send endorsement request.'}, status=status.HTTP_401_UNAUTHORIZED) 
                else:
                    return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)          
                                
            return Response({"message": "Data saved successfully"}, status=status.HTTP_201_CREATED)
        
        return Response(club_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PlayerTeamLeagueModelUpdateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Assuming the request data contains a 'type' field indicating the model
        career_history = request.data.get('career_history')
        data_type = career_history.get('flag')
        # print(data_type)

        if data_type == 'league':
            data = career_history

            # Separate the data based on the models
            league_data = {key: data[key] for key in ['sport_type', 'league_name', 'league_type']}
            player_data = {key: data[key] for key in ['id', 'club_id', 'club_name', 'from_year', 'to_year', 'games_played', 'club_goals', 'club_assists', 'club_passes', 'club_saved_goals', 'interceptions_per_game', 'takles_per_game', 'shots_per_game', 'key_passes_per_game', 'dribles_completed_per_game', 'clean_sheets_per_game', 'club_yellow_card', 'club_red_card', 'league_id', 'league_name', 'country_name', 'league_type', 'achievements', 'summary']}
            # And so on...

            # Serialize the data for each model
            league_serializer = LeagueSerializer(data=league_data)

            # Validate the data for each model
            if league_serializer.is_valid():
                # Perform any additional processing or actions as needed
                # For example, save the data to the respective models
                
                league_instance = league_serializer.save()
                
                # Extract 'id' from model1_instance
                league_id = league_instance.id
                
                # Assign id to the appropriate field in Model2
                player_data['league_id'] = league_id  
    
                # Get the instance to update
                instance_id = data.get('id')  # Remove 'id' from data
                try:
                    instance = Club.objects.get(pk=instance_id)
                except Club.DoesNotExist:
                    return Response({"error": "Instance does not exist"}, status=404)

                # Update the instance
                player_serializer = ClubSerializer(instance, data=player_data)
                if player_serializer.is_valid():
                    # player_career_history_instance = player_serializer.save()
                    player_serializer.save()

                    endorsement_request = request.data.get('endorsement_request')
                    if(endorsement_request != ''):
                        print(endorsement_request)
                        if isinstance(endorsement_request, list):
                            endorsement_request_serializer = FootballPlayerEndorsementRequestSerializer(data=endorsement_request, many=True)
                            if endorsement_request_serializer.is_valid():
                                for item_data in endorsement_request_serializer.validated_data:
                                    if item_data['to_endorser'] is None:  
                                        return Response({'error':'No user found with this email.'}, status=status.HTTP_400_BAD_REQUEST)
                                    else:         
                                        my_object = CustomUser.objects.get(email=item_data['to_endorser'])
                                            
                                        endorsee = CustomUser.objects.get(email=item_data['from_endorsee'])
                                                    
                                        absurl = settings.BASE_URL+'endorsements/pending'
                                        email_body = 'Hi '+ my_object.first_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '.\nUse the link below to check the endorsement request\n' + absurl
                                        data = {'email_body': email_body, 'to_email': my_object.email,
                                                'email_subject': 'Endorsement Request'}

                                        Util.send_email(data)              
                                try:
                                    with transaction.atomic():
                                        FootballPlayerEndorsementRequest.objects.bulk_create([
                                            FootballPlayerEndorsementRequest(**item) for item in endorsement_request_serializer.validated_data
                                        ])
                                                    
                                    # return Response(endorsement_request_serializer.data, status=status.HTTP_200_OK)
                                except Exception as e:
                                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                            else:
                                return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({"error": "Expected a list of items"}, status=status.HTTP_400_BAD_REQUEST) 
                                    
                    endorsement_request_to_club = request.data.get('endorsement_request_to_club')
                    if(endorsement_request_to_club != ''):
                        print(endorsement_request_to_club)   
                        endorsement_request_serializer = FootballPlayerEndorsementRequestSerializer(data=endorsement_request_to_club)
                        if endorsement_request_serializer.is_valid():
                            register_id = endorsement_request_to_club.get('reg_id')  
                            from_endorsee = endorsement_request_to_club.get('from_endorsee')  
                            try:          
                                my_object = CustomUser.objects.get(reg_id=register_id)
                                endorsement_request_serializer.validated_data['to_endorser'] = my_object 
                                
                                try:
                                    FootballPlayerEndorsementRequest.objects.get(to_endorser=endorsement_request_serializer.validated_data['to_endorser'], type='Club', from_endorsee=from_endorsee)
                                    return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK) 
                                
                                except FootballPlayerEndorsementRequest.DoesNotExist:
                                    endorsee = CustomUser.objects.get(id=from_endorsee)
                                        
                                    absurl = settings.BASE_URL+'endorsements/pending'
                                    email_body = 'Hi '+ my_object.club_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '\nUse the link below to check the endorsement request\n' + absurl
                                    data = {'email_body': email_body, 'to_email': my_object.email, 'email_subject': 'Endorsement Request'}

                                    Util.send_email(data)
                                                    
                                    endorsement_request_serializer.save() 
                                    
                                    return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK) 
                            
                            except CustomUser.DoesNotExist:
                                return Response({'error':'Club not registered. You cannot send endorsement request.'}, status=status.HTTP_401_UNAUTHORIZED) 
                        else:
                            return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)          
                                        
                    return Response({"message": "Data saved successfully"}, status=status.HTTP_201_CREATED)
                else:
                    return Response(player_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                # If any serializer data is invalid, return errors
                errors = {}
                if not league_serializer.is_valid():
                    errors['league_errors'] = league_serializer.errors
        
                return Response(errors, status=400)
            
        if data_type == 'leaguenull':
            data = career_history

            # Separate the data based on the models
            # league_data = {key: data[key] for key in ['sport_type', 'league_name', 'league_type']}
            player_data = {key: data[key] for key in ['id', 'club_id', 'club_name', 'from_year', 'to_year', 'games_played', 'club_goals', 'club_assists', 'club_passes', 'club_saved_goals', 'interceptions_per_game', 'takles_per_game', 'shots_per_game', 'key_passes_per_game', 'dribles_completed_per_game', 'clean_sheets_per_game', 'club_yellow_card', 'club_red_card', 'country_name', 'league_type', 'achievements', 'summary']}
            # And so on...

            # Get the instance to update
            instance_id = data.get('id')  # Remove 'id' from data
            try:
                instance = Club.objects.get(pk=instance_id)
            except Club.DoesNotExist:
                return Response({"error": "Instance does not exist"}, status=404)

            # Update the instance
            player_serializer = ClubSerializer(instance, data=player_data)
            if player_serializer.is_valid():
                # player_career_history_instance = player_serializer.save()
                player_serializer.save()

                endorsement_request = request.data.get('endorsement_request')
                if(endorsement_request != ''):
                    print(endorsement_request)
                    if isinstance(endorsement_request, list):
                        endorsement_request_serializer = FootballPlayerEndorsementRequestSerializer(data=endorsement_request, many=True)
                        if endorsement_request_serializer.is_valid():
                            for item_data in endorsement_request_serializer.validated_data:
                                if item_data['to_endorser'] is None:  
                                    return Response({'error':'No user found with this email.'}, status=status.HTTP_400_BAD_REQUEST)
                                else:         
                                    my_object = CustomUser.objects.get(email=item_data['to_endorser'])
                                        
                                    endorsee = CustomUser.objects.get(email=item_data['from_endorsee'])
                                                
                                    absurl = settings.BASE_URL+'endorsements/pending'
                                    email_body = 'Hi '+ my_object.first_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '.\nUse the link below to check the endorsement request\n' + absurl
                                    data = {'email_body': email_body, 'to_email': my_object.email,
                                            'email_subject': 'Endorsement Request'}

                                    Util.send_email(data)              
                            try:
                                with transaction.atomic():
                                    FootballPlayerEndorsementRequest.objects.bulk_create([
                                        FootballPlayerEndorsementRequest(**item) for item in endorsement_request_serializer.validated_data
                                    ])
                                                
                                # return Response(endorsement_request_serializer.data, status=status.HTTP_200_OK)
                            except Exception as e:
                                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({"error": "Expected a list of items"}, status=status.HTTP_400_BAD_REQUEST) 
                                
                endorsement_request_to_club = request.data.get('endorsement_request_to_club')
                if(endorsement_request_to_club != ''):
                    print(endorsement_request_to_club)   
                    endorsement_request_serializer = FootballPlayerEndorsementRequestSerializer(data=endorsement_request_to_club)
                    if endorsement_request_serializer.is_valid():
                        register_id = endorsement_request_to_club.get('reg_id')  
                        from_endorsee = endorsement_request_to_club.get('from_endorsee')  
                        try:          
                            my_object = CustomUser.objects.get(reg_id=register_id)
                            endorsement_request_serializer.validated_data['to_endorser'] = my_object 
                            
                            try:
                                FootballPlayerEndorsementRequest.objects.get(to_endorser=endorsement_request_serializer.validated_data['to_endorser'], type='Club', from_endorsee=from_endorsee)
                                return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK) 
                            
                            except FootballPlayerEndorsementRequest.DoesNotExist:
                                endorsee = CustomUser.objects.get(id=from_endorsee)
                                    
                                absurl = settings.BASE_URL+'endorsements/pending'
                                email_body = 'Hi '+ my_object.club_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '\nUse the link below to check the endorsement request\n' + absurl
                                data = {'email_body': email_body, 'to_email': my_object.email, 'email_subject': 'Endorsement Request'}

                                Util.send_email(data)
                                                
                                endorsement_request_serializer.save() 
                                
                                return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK) 
                        
                        except CustomUser.DoesNotExist:
                            return Response({'error':'Club not registered. You cannot send endorsement request.'}, status=status.HTTP_401_UNAUTHORIZED) 
                    else:
                        return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)          
                                    
                return Response({"message": "Data saved successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response(player_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        elif data_type == 'team':
             # Get the data sent through HTTP POST
            data = career_history
            
            # if 'league_id' in data:
            #     # If 'id' is present, it's an update operation
            #     flag=1
            #     league_id = data.get('league_id')
            #     sport_type = data.get('sport_type')
            #     print(league_id)
            #     my_object = League.objects.get(id=league_id)
            #     print(my_object.sport_type)
            #     substrings = my_object.sport_type.split(',')
            #     print(f"Substrings are {substrings}")
            #     for substring in substrings:
            #         print(f"Sport type: {sport_type} found in the list.")
            #         if(substring.lower() == sport_type.lower()):
            #             print(f"Substring: {substring} found in the list.")
            #             flag = 0
            #     if(flag == 1):
            #         my_object.sport_type = my_object.sport_type + "," + sport_type
            #         print(my_object.sport_type)
            #         my_object.save()

            # Separate the data based on the models
            team_data = {key: data[key] for key in ['club_name', 'reg_id', 'country_name', 'sport_type']}
            player_data = {key: data[key] for key in ['id', 'club_id', 'club_name', 'from_year', 'to_year', 'games_played', 'club_goals', 'club_assists', 'club_passes', 'club_saved_goals', 'interceptions_per_game', 'takles_per_game', 'shots_per_game', 'key_passes_per_game', 'dribles_completed_per_game', 'clean_sheets_per_game', 'club_yellow_card', 'club_red_card', 'league_id', 'league_name', 'country_name', 'league_type', 'achievements', 'summary']}
            # And so on...

            # Serialize the data for each model
            team_serializer = TeamSerializer(data=team_data)

            # Validate the data for each model
            if team_serializer.is_valid():
                team_instance = team_serializer.save()
                
                # Extract 'id' from model1_instance
                team_id = team_instance.reg_id
                
                # Assign id to the appropriate field in Model2
                player_data['club_id'] = team_id   
                instance_id = data.get('id')  # Remove 'id' from data
                try:
                    instance = Club.objects.get(pk=instance_id)
                except Club.DoesNotExist:
                    return Response({"error": "Instance does not exist"}, status=404)

                # Update the instance
                club_serializer = ClubSerializer(instance, data=player_data)
                if club_serializer.is_valid():
                    # player_career_history_instance = club_serializer.save()
                    club_serializer.save()
                    
                    endorsement_request = request.data.get('endorsement_request')
                    if(endorsement_request != ''):
                        print(endorsement_request)
                        if isinstance(endorsement_request, list):
                            endorsement_request_serializer = FootballPlayerEndorsementRequestSerializer(data=endorsement_request, many=True)
                            if endorsement_request_serializer.is_valid():
                                for item_data in endorsement_request_serializer.validated_data:
                                    if item_data['to_endorser'] is None:  
                                        return Response({'error':'No user found with this email.'}, status=status.HTTP_400_BAD_REQUEST)
                                    else:         
                                        my_object = CustomUser.objects.get(email=item_data['to_endorser'])
                                            
                                        endorsee = CustomUser.objects.get(email=item_data['from_endorsee'])
                                                    
                                        absurl = settings.BASE_URL+'endorsements/pending'
                                        email_body = 'Hi '+ my_object.first_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '.\nUse the link below to check the endorsement request\n' + absurl
                                        data = {'email_body': email_body, 'to_email': my_object.email,
                                                'email_subject': 'Endorsement Request'}

                                        Util.send_email(data)              
                                try:
                                    with transaction.atomic():
                                        FootballPlayerEndorsementRequest.objects.bulk_create([
                                            FootballPlayerEndorsementRequest(**item) for item in endorsement_request_serializer.validated_data
                                        ])
                                                    
                                    # return Response(endorsement_request_serializer.data, status=status.HTTP_200_OK)
                                except Exception as e:
                                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                            else:
                                return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({"error": "Expected a list of items"}, status=status.HTTP_400_BAD_REQUEST)           
                                        
                    return Response({"message": "Data saved successfully"}, status=status.HTTP_201_CREATED)
                else:
                    return Response(club_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                # If any serializer data is invalid, return errors
                errors = {}
                if not team_serializer.is_valid():
                    errors['team_errors'] = team_serializer.errors
               
                return Response(errors, status=400)
            
        elif data_type == 'teamleaguenull':
             # Get the data sent through HTTP POST
            data = career_history
            
            # if 'league_id' in data:
            #     # If 'id' is present, it's an update operation
            #     flag=1
            #     league_id = data.get('league_id')
            #     sport_type = data.get('sport_type')
            #     print(league_id)
            #     my_object = League.objects.get(id=league_id)
            #     print(my_object.sport_type)
            #     substrings = my_object.sport_type.split(',')
            #     print(f"Substrings are {substrings}")
            #     for substring in substrings:
            #         print(f"Sport type: {sport_type} found in the list.")
            #         if(substring.lower() == sport_type.lower()):
            #             print(f"Substring: {substring} found in the list.")
            #             flag = 0
            #     if(flag == 1):
            #         my_object.sport_type = my_object.sport_type + "," + sport_type
            #         print(my_object.sport_type)
            #         my_object.save()

            # Separate the data based on the models
            team_data = {key: data[key] for key in ['club_name', 'reg_id', 'country_name', 'sport_type']}
            player_data = {key: data[key] for key in ['id', 'club_id', 'club_name', 'from_year', 'to_year', 'games_played', 'club_goals', 'club_assists', 'club_passes', 'club_saved_goals', 'interceptions_per_game', 'takles_per_game', 'shots_per_game', 'key_passes_per_game', 'dribles_completed_per_game', 'clean_sheets_per_game', 'club_yellow_card', 'club_red_card', 'country_name', 'league_type', 'achievements', 'summary']}
            # And so on...

            # Serialize the data for each model
            team_serializer = TeamSerializer(data=team_data)

            # Validate the data for each model
            if team_serializer.is_valid():
                team_instance = team_serializer.save()
                
                # Extract 'id' from model1_instance
                team_id = team_instance.reg_id
                
                # Assign id to the appropriate field in Model2
                player_data['club_id'] = team_id   
                instance_id = data.get('id')  # Remove 'id' from data
                try:
                    instance = Club.objects.get(pk=instance_id)
                except Club.DoesNotExist:
                    return Response({"error": "Instance does not exist"}, status=404)

                # Update the instance
                club_serializer = ClubSerializer(instance, data=player_data)
                if club_serializer.is_valid():
                    # player_career_history_instance = club_serializer.save()
                    club_serializer.save()
                    
                    endorsement_request = request.data.get('endorsement_request')
                    if(endorsement_request != ''):
                        endorsement_request_serializer = FootballPlayerEndorsementRequestSerializer(data=endorsement_request)
                        if endorsement_request_serializer.is_valid():
                            try:
                                my_object = CustomUser.objects.get(email=endorsement_request_serializer.validated_data['to_endorser_email'])
                                return Response({'Email Id already registered with other User'}, status=status.HTTP_400_BAD_REQUEST)
                            except CustomUser.DoesNotExist:
                                new_user = {'username': team_id, 'password': 'welCome@123', 'password2': 'welCome@123', 'email': endorsement_request_serializer.validated_data['to_endorser_email'], 'reg_id':  team_id, 'is_active': False, 'club_name': player_data['club_name'], 'account_type': 'institute'}
                                print(new_user)
                                user_serializer = UserSerializer(data=new_user)
                                if user_serializer.is_valid():
                                    user_instance = user_serializer.save()
                                    endorsement_request_serializer.validated_data['to_endorser'] = user_instance
                                    # endorsement_request_serializer.validated_data['player_career_history'] = player_career_history_instance
                                                    
                                    # send_mail(
                                    #     subject='Endorsement Request',
                                    #     message='Endorsement request from player for registration',
                                    #     from_email='athletescouting@gmail.com',
                                    #     recipient_list=[endorsement_request_serializer.validated_data['to_endorser_email']],
                                    #     fail_silently=False,
                                    # )
                                    
                                    absurl = settings.BASE_URL+'register?email=' + user_instance.email
                                    email_body = 'Hi '+ user_instance.club_name + ', you have a registration request from Bscoutd.' + '\n Use the link below to register \n' + absurl
                                    data = {'email_body': email_body, 'to_email': user_instance.email,
                                            'email_subject': 'Endorsement Request'}

                                    Util.send_email(data)
                                        
                                    endorsement_request_serializer.save()
                                else:
                                    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                    return Response({"message": "Data updated successfully"}, status=201)
                else:
                    return Response(club_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                # If any serializer data is invalid, return errors
                errors = {}
                if not team_serializer.is_valid():
                    errors['team_errors'] = team_serializer.errors
               
                return Response(errors, status=400)
        
        elif data_type == 'teamleague':
             # Get the data sent through HTTP POST
            data = career_history

            # Separate the data based on the models
            league_data = {key: data[key] for key in ['sport_type', 'league_name', 'league_type']}
            team_data = {key: data[key] for key in ['club_name', 'reg_id', 'country_name', 'sport_type']}
            player_data = {key: data[key] for key in ['id', 'club_id', 'club_name', 'from_year', 'to_year', 'games_played', 'club_goals', 'club_assists', 'club_passes', 'club_saved_goals', 'interceptions_per_game', 'takles_per_game', 'shots_per_game', 'key_passes_per_game', 'dribles_completed_per_game', 'clean_sheets_per_game', 'club_yellow_card', 'club_red_card', 'league_id', 'league_name', 'country_name', 'league_type', 'achievements', 'summary']}

            # Serialize the data for each model
            league_serializer = LeagueSerializer(data=league_data)
            team_serializer = TeamSerializer(data=team_data)

            # Validate the data for each model
            if team_serializer.is_valid() and league_serializer.is_valid():
                team_instance = team_serializer.save()
                league_instance = league_serializer.save()
                
                # Extract 'id' from model1_instance
                team_id = team_instance.reg_id
                league_id = league_instance.id
                
                # Assign id to the appropriate field in Model2
                player_data['club_id'] = team_id    
                player_data['league_id'] = league_id  
                
                instance_id = data.get('id')  # Remove 'id' from data
                try:
                    instance = Club.objects.get(pk=instance_id)
                except Club.DoesNotExist:
                    return Response({"error": "Instance does not exist"}, status=404)

                # Update the instance
                club_serializer = ClubSerializer(instance, data=player_data)
                if club_serializer.is_valid():
                    # player_career_history_instance = club_serializer.save()
                    club_serializer.save()
                    
                    endorsement_request = request.data.get('endorsement_request')
                    if(endorsement_request != ''):
                        print(endorsement_request)
                        if isinstance(endorsement_request, list):
                            endorsement_request_serializer = FootballPlayerEndorsementRequestSerializer(data=endorsement_request, many=True)
                            if endorsement_request_serializer.is_valid():
                                for item_data in endorsement_request_serializer.validated_data:
                                    if item_data['to_endorser'] is None:  
                                        return Response({'error':'No user found with this email.'}, status=status.HTTP_400_BAD_REQUEST)
                                    else:         
                                        my_object = CustomUser.objects.get(email=item_data['to_endorser'])
                                            
                                        endorsee = CustomUser.objects.get(email=item_data['from_endorsee'])
                                                    
                                        absurl = settings.BASE_URL+'endorsements/pending'
                                        email_body = 'Hi '+ my_object.first_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '.\nUse the link below to check the endorsement request\n' + absurl
                                        data = {'email_body': email_body, 'to_email': my_object.email,
                                                'email_subject': 'Endorsement Request'}

                                        Util.send_email(data)              
                                try:
                                    with transaction.atomic():
                                        FootballPlayerEndorsementRequest.objects.bulk_create([
                                            FootballPlayerEndorsementRequest(**item) for item in endorsement_request_serializer.validated_data
                                        ])
                                                    
                                    # return Response(endorsement_request_serializer.data, status=status.HTTP_200_OK)
                                except Exception as e:
                                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                            else:
                                return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({"error": "Expected a list of items"}, status=status.HTTP_400_BAD_REQUEST)           
                                        
                    return Response({"message": "Data saved successfully"}, status=status.HTTP_201_CREATED)
                else:
                    return Response(club_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
            if 'document_file' in request.data:
                data = request.data
        
                # Separate the data based on the models
                license_data = {key: data[key] for key in ['license_name']}
                coach_data = {key: data[key] for key in ['license_id', 'license_name', 'document_type', 'document_file', 'coach']}
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
            if 'document_file' in request.data:
                data = request.data
        
                # Separate the data based on the models
                license_data = {key: data[key] for key in ['license_name']}
                coach_data = {key: data[key] for key in ['id', 'license_id', 'license_name', 'document_type', 'document_file', 'coach']}
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
        
        
# Old requirement/enhancement made in endorsement request of coach

# class CoachCareerHistoryModelCreateAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         # Assuming the request data contains a 'type' field indicating the model
#         career_history = request.data.get('career_history')
#         data_type = career_history.get('flag')
#         # print(data_type)

#         if data_type == 'league':
#             data = career_history

#             # Separate the data based on the models
#             league_data = {key: data[key] for key in ['sport_type', 'league_name', 'league_type']}
#             coach_data = {key: data[key] for key in ['club_id', 'club_name', 'from_year', 'to_year', 'league_id', 'league_name', 'country_name', 'league_type', 'achievements', 'summary', 'coach_id']}
#             # And so on...

#             # Serialize the data for each model
#             league_serializer = LeagueSerializer(data=league_data)
#             # coach_serializer = FootballCoachCareerHistorySerializer(data=coach_data)
#             # And so on...

#             # Validate the data for each model
#             if league_serializer.is_valid():
#                 league_instance = league_serializer.save()
                
#                 # Extract 'id' from model1_instance
#                 league_id = league_instance.id
                
#                 # Assign id to the appropriate field in Model2
#                 coach_data['league_id'] = league_id    
#                 coach_serializer = FootballCoachCareerHistorySerializer(data=coach_data)
#                 if coach_serializer.is_valid():
#                     coach_career_history_instance = coach_serializer.save()
#                     endorsement_request = request.data.get('endorsement_request')
#                     if(endorsement_request!=''):
#                         print(endorsement_request) 
#                         endorsement_request_serializer = FootballCoachEndorsementRequestSerializer(data=endorsement_request)
#                         if endorsement_request_serializer.is_valid():
#                             register_id = endorsement_request.get('reg_id')
#                             endorsement_request_serializer.validated_data['coach_career_history'] = coach_career_history_instance
#                             try:     
#                                 my_object = CustomUser.objects.get(reg_id=register_id)
#                                 endorsement_request_serializer.validated_data['to_endorser'] = my_object 
                                    
#                                 # send_mail(
#                                 #     subject='Endorsement Request',
#                                 #     message='Endorsement request from coach',
#                                 #     from_email='athletescouting@gmail.com',
#                                 #     recipient_list=[my_object.email],
#                                 #     fail_silently=False,
#                                 # )
                                
#                                 absurl = settings.BASE_URL+'endorsements/pending'
#                                 email_body = 'Hi '+ my_object.club_name + ', you have endorsement request from coach.' + '\n Use the link below to check the endorsement request \n' + absurl
#                                 data = {'email_body': email_body, 'to_email': my_object.email,
#                                         'email_subject': 'Endorsement Request'}

#                                 Util.send_email(data)
                                
#                                 endorsement_request_serializer.save() 
#                             except CustomUser.DoesNotExist:
#                                 try:
#                                     my_object = CustomUser.objects.get(email=endorsement_request_serializer.validated_data['to_endorser_email'])
#                                     coach_career_history = FootballCoachCareerHistory.objects.get(id=coach_career_history_instance.id)
#                                     coach_career_history.delete()
#                                     return Response({'Email Id already registered with other User'}, status=status.HTTP_400_BAD_REQUEST)
#                                 except CustomUser.DoesNotExist:
#                                     new_user = {'username': register_id, 'password': 'welCome@123', 'password2': 'welCome@123', 'email': endorsement_request_serializer.validated_data['to_endorser_email'], 'is_active': False, 'reg_id': register_id, 'club_name': coach_data['club_name'], 'account_type': 'institute'}
#                                     print(new_user)
#                                     user_serializer = UserSerializer(data=new_user)
#                                     if user_serializer.is_valid():
#                                         user_instance = user_serializer.save()
#                                         endorsement_request_serializer.validated_data['to_endorser'] = user_instance
#                                         endorsement_request_serializer.validated_data['coach_career_history'] = coach_career_history_instance
                                                        
#                                         # send_mail(
#                                         #     subject='Endorsement Request',
#                                         #     message='Endorsement request from coach for registration',
#                                         #     from_email='athletescouting@gmail.com',
#                                         #     recipient_list=[endorsement_request_serializer.validated_data['to_endorser_email']],
#                                         #     fail_silently=False,
#                                         # )
                                        
#                                         absurl = settings.BASE_URL+'register?email=' + user_instance.email
#                                         email_body = 'Hi '+ user_instance.club_name + ', you have a registration request from Bscoutd.' + '\n Use the link below to register \n' + absurl
#                                         data = {'email_body': email_body, 'to_email': user_instance.email,
#                                                 'email_subject': 'Endorsement Request'}

#                                         Util.send_email(data)
                                
#                                         endorsement_request_serializer.save()
#                                     else:
#                                         return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
#                         else:
#                             return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)            
        
#                     # Return any relevant data or success message
#                     return Response({"message": "Data saved successfully"}, status=201)
#                 else:
#                     errors = {}
#                     errors['coach_errors'] = coach_serializer.errors
                    
#                     return Response(errors, status=400)
#             else:
#                 # If any serializer data is invalid, return errors
#                 errors = {}
#                 if not league_serializer.is_valid():
#                     errors['league_errors'] = league_serializer.errors
               
#                 return Response(errors, status=400)
            
#         if data_type == 'leaguenull':
#             data = career_history

#             # Separate the data based on the models
#             coach_data = {key: data[key] for key in ['club_id', 'club_name', 'from_year', 'to_year', 'country_name', 'league_type', 'achievements', 'summary', 'coach_id']}
#             # And so on...
  
#             coach_serializer = FootballCoachCareerHistorySerializer(data=coach_data)
#             if coach_serializer.is_valid():
#                 coach_career_history_instance = coach_serializer.save()
#                 endorsement_request = request.data.get('endorsement_request')
#                 if(endorsement_request!=''):
#                     print(endorsement_request) 
#                     endorsement_request_serializer = FootballCoachEndorsementRequestSerializer(data=endorsement_request)
#                     if endorsement_request_serializer.is_valid():
#                         register_id = endorsement_request.get('reg_id')
#                         endorsement_request_serializer.validated_data['coach_career_history'] = coach_career_history_instance
#                         try:     
#                             my_object = CustomUser.objects.get(reg_id=register_id)
#                             endorsement_request_serializer.validated_data['to_endorser'] = my_object 
                                    
#                                 # send_mail(
#                                 #     subject='Endorsement Request',
#                                 #     message='Endorsement request from coach',
#                                 #     from_email='athletescouting@gmail.com',
#                                 #     recipient_list=[my_object.email],
#                                 #     fail_silently=False,
#                                 # )
                                
#                             absurl = settings.BASE_URL+'endorsements/pending'
#                             email_body = 'Hi '+ my_object.club_name + ', you have endorsement request from coach.' + '\n Use the link below to check the endorsement request \n' + absurl
#                             data = {'email_body': email_body, 'to_email': my_object.email,
#                                         'email_subject': 'Endorsement Request'}

#                             Util.send_email(data)
                                
#                             endorsement_request_serializer.save() 
#                         except CustomUser.DoesNotExist:
#                             try:
#                                 my_object = CustomUser.objects.get(email=endorsement_request_serializer.validated_data['to_endorser_email'])
#                                 coach_career_history = FootballCoachCareerHistory.objects.get(id=coach_career_history_instance.id)
#                                 coach_career_history.delete()
#                                 return Response({'Email Id already registered with other User'}, status=status.HTTP_400_BAD_REQUEST)
#                             except CustomUser.DoesNotExist:
#                                 new_user = {'username': register_id, 'password': 'welCome@123', 'password2': 'welCome@123', 'email': endorsement_request_serializer.validated_data['to_endorser_email'], 'is_active': False, 'reg_id': register_id, 'club_name': coach_data['club_name'], 'account_type': 'institute'}
#                                 print(new_user)
#                                 user_serializer = UserSerializer(data=new_user)
#                                 if user_serializer.is_valid():
#                                     user_instance = user_serializer.save()
#                                     endorsement_request_serializer.validated_data['to_endorser'] = user_instance
#                                     endorsement_request_serializer.validated_data['coach_career_history'] = coach_career_history_instance
                                                        
#                                         # send_mail(
#                                         #     subject='Endorsement Request',
#                                         #     message='Endorsement request from coach for registration',
#                                         #     from_email='athletescouting@gmail.com',
#                                         #     recipient_list=[endorsement_request_serializer.validated_data['to_endorser_email']],
#                                         #     fail_silently=False,
#                                         # )
                                        
#                                     absurl = settings.BASE_URL+'register?email=' + user_instance.email
#                                     email_body = 'Hi '+ user_instance.club_name + ', you have a registration request from Bscoutd.' + '\n Use the link below to register \n' + absurl
#                                     data = {'email_body': email_body, 'to_email': user_instance.email,
#                                             'email_subject': 'Endorsement Request'}

#                                     Util.send_email(data)
                                
#                                     endorsement_request_serializer.save()
#                                 else:
#                                     return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
#                     else:
#                         return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)            
        
#                 # Return any relevant data or success message
#                 return Response({"message": "Data saved successfully"}, status=201)
#             else:
#                 errors = {}
#                 errors['coach_errors'] = coach_serializer.errors
                    
#                 return Response(errors, status=400)          
            
#         elif data_type == 'team':
#              # Get the data sent through HTTP POST
#             data = career_history
            
#             # if 'league_id' in data:
#             #     flag=1
#             #     league_id = data.get('league_id')
#             #     sport_type = data.get('sport_type')
#             #     print(league_id)
#             #     # league_data = {key: data[key] for key in ['sport_type', 'league_name', 'league_type']}
#             #     my_object = League.objects.get(id=league_id)
#             #     print(my_object.sport_type)
#             #     substrings = my_object.sport_type.split(',')
#             #     print(f"Substrings are {substrings}")
#             #     for substring in substrings:
#             #         print(f"Sport type: {sport_type} found in the list.")
#             #         if(substring.lower() == sport_type.lower()):
#             #             print(f"Substring: {substring} found in the list.")
#             #             flag = 0
#             #     if(flag == 1):
#             #         my_object.sport_type = my_object.sport_type + "," + sport_type
#             #         print(my_object.sport_type)
#             #         my_object.save()

#             # Separate the data based on the models
#             team_data = {key: data[key] for key in ['club_name', 'reg_id', 'country_name', 'sport_type']}
#             coach_data = {key: data[key] for key in ['club_id', 'club_name', 'from_year', 'to_year', 'league_id', 'league_name', 'country_name', 'league_type', 'achievements', 'summary', 'coach_id']}
#             # And so on...

#             # Serialize the data for each model
#             team_serializer = TeamSerializer(data=team_data)

#             # Validate the data for each model
#             if team_serializer.is_valid():
#                 team_instance = team_serializer.save()
                
#                 # Extract 'id' from model1_instance
#                 team_id = team_instance.reg_id
                
#                 # Assign id to the appropriate field in Model2
#                 coach_data['club_id'] = team_id    
#                 coach_serializer = FootballCoachCareerHistorySerializer(data=coach_data)
#                 if coach_serializer.is_valid():
#                     coach_career_history_instance = coach_serializer.save()
#                     endorsement_request = request.data.get('endorsement_request')
#                     if(endorsement_request != ''):
#                         endorsement_request_serializer = FootballCoachEndorsementRequestSerializer(data=endorsement_request)
#                         if endorsement_request_serializer.is_valid():
#                             try:
#                                 my_object = CustomUser.objects.get(email=endorsement_request_serializer.validated_data['to_endorser_email'])
#                                 coach_career_history = FootballCoachCareerHistory.objects.get(id=coach_career_history_instance.id)
#                                 coach_career_history.delete()
#                                 return Response({'Email Id already registered with other User'}, status=status.HTTP_400_BAD_REQUEST)
#                             except CustomUser.DoesNotExist:
#                                 new_user = {'username': team_id, 'password': 'welCome@123', 'password2': 'welCome@123', 'email': endorsement_request_serializer.validated_data['to_endorser_email'], 'reg_id':  team_id, 'is_active': False, 'club_name': coach_data['club_name'], 'account_type': 'institute'}
#                                 print(new_user)
#                                 user_serializer = UserSerializer(data=new_user)
#                                 if user_serializer.is_valid():
#                                     user_instance = user_serializer.save()
#                                     endorsement_request_serializer.validated_data['to_endorser'] = user_instance
#                                     endorsement_request_serializer.validated_data['coach_career_history'] = coach_career_history_instance
                                                    
#                                     # send_mail(
#                                     #     subject='Endorsement Request',
#                                     #     message='Endorsement request from coach for registration',
#                                     #     from_email='athletescouting@gmail.com',
#                                     #     recipient_list=[endorsement_request_serializer.validated_data['to_endorser_email']],
#                                     #     fail_silently=False,
#                                     # )
                                    
#                                     absurl = settings.BASE_URL+'register?email=' + user_instance.email
#                                     email_body = 'Hi '+ user_instance.club_name + ', you have a registration request from Bscoutd.' + '\n Use the link below to register \n' + absurl
#                                     data = {'email_body': email_body, 'to_email': user_instance.email,
#                                             'email_subject': 'Endorsement Request'}

#                                     Util.send_email(data)
                                
#                                     endorsement_request_serializer.save()
#                                 else:
#                                     return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#                         else:
#                             return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#                     # Return any relevant data or success message
#                     return Response({"message": "Data saved successfully"}, status=201)
#                 else:
#                     errors = {}
#                     errors['coach_errors'] = coach_serializer.errors
                    
#                     return Response(errors, status=400)
#             else:
#                 # If any serializer data is invalid, return errors
#                 errors = {}
#                 if not team_serializer.is_valid():
#                     errors['team_errors'] = team_serializer.errors
               
#                 return Response(errors, status=400)
            
#         elif data_type == 'teamleaguenull':
#              # Get the data sent through HTTP POST
#             data = career_history
            
#             # if 'league_id' in data:
#             #     flag=1
#             #     league_id = data.get('league_id')
#             #     sport_type = data.get('sport_type')
#             #     print(league_id)
#             #     # league_data = {key: data[key] for key in ['sport_type', 'league_name', 'league_type']}
#             #     my_object = League.objects.get(id=league_id)
#             #     print(my_object.sport_type)
#             #     substrings = my_object.sport_type.split(',')
#             #     print(f"Substrings are {substrings}")
#             #     for substring in substrings:
#             #         print(f"Sport type: {sport_type} found in the list.")
#             #         if(substring.lower() == sport_type.lower()):
#             #             print(f"Substring: {substring} found in the list.")
#             #             flag = 0
#             #     if(flag == 1):
#             #         my_object.sport_type = my_object.sport_type + "," + sport_type
#             #         print(my_object.sport_type)
#             #         my_object.save()

#             # Separate the data based on the models
#             team_data = {key: data[key] for key in ['club_name', 'reg_id', 'country_name', 'sport_type']}
#             coach_data = {key: data[key] for key in ['club_id', 'club_name', 'from_year', 'to_year', 'country_name', 'league_type', 'achievements', 'summary', 'coach_id']}
#             # And so on...

#             # Serialize the data for each model
#             team_serializer = TeamSerializer(data=team_data)

#             # Validate the data for each model
#             if team_serializer.is_valid():
#                 team_instance = team_serializer.save()
                
#                 # Extract 'id' from model1_instance
#                 team_id = team_instance.reg_id
                
#                 # Assign id to the appropriate field in Model2
#                 coach_data['club_id'] = team_id    
#                 coach_serializer = FootballCoachCareerHistorySerializer(data=coach_data)
#                 if coach_serializer.is_valid():
#                     coach_career_history_instance = coach_serializer.save()
#                     endorsement_request = request.data.get('endorsement_request')
#                     if(endorsement_request != ''):
#                         endorsement_request_serializer = FootballCoachEndorsementRequestSerializer(data=endorsement_request)
#                         if endorsement_request_serializer.is_valid():
#                             try:
#                                 my_object = CustomUser.objects.get(email=endorsement_request_serializer.validated_data['to_endorser_email'])
#                                 coach_career_history = FootballCoachCareerHistory.objects.get(id=coach_career_history_instance.id)
#                                 coach_career_history.delete()
#                                 return Response({'Email Id already registered with other User'}, status=status.HTTP_400_BAD_REQUEST)
#                             except CustomUser.DoesNotExist:
#                                 new_user = {'username': team_id, 'password': 'welCome@123', 'password2': 'welCome@123', 'email': endorsement_request_serializer.validated_data['to_endorser_email'], 'reg_id':  team_id, 'is_active': False, 'club_name': coach_data['club_name'], 'account_type': 'institute'}
#                                 print(new_user)
#                                 user_serializer = UserSerializer(data=new_user)
#                                 if user_serializer.is_valid():
#                                     user_instance = user_serializer.save()
#                                     endorsement_request_serializer.validated_data['to_endorser'] = user_instance
#                                     endorsement_request_serializer.validated_data['coach_career_history'] = coach_career_history_instance
                                                    
#                                     # send_mail(
#                                     #     subject='Endorsement Request',
#                                     #     message='Endorsement request from coach for registration',
#                                     #     from_email='athletescouting@gmail.com',
#                                     #     recipient_list=[endorsement_request_serializer.validated_data['to_endorser_email']],
#                                     #     fail_silently=False,
#                                     # )
                                    
#                                     absurl = settings.BASE_URL+'register?email=' + user_instance.email
#                                     email_body = 'Hi '+ user_instance.club_name + ', you have a registration request from Bscoutd.' + '\n Use the link below to register \n' + absurl
#                                     data = {'email_body': email_body, 'to_email': user_instance.email,
#                                             'email_subject': 'Endorsement Request'}

#                                     Util.send_email(data)
                                
#                                     endorsement_request_serializer.save()
#                                 else:
#                                     return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#                         else:
#                             return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#                     # Return any relevant data or success message
#                     return Response({"message": "Data saved successfully"}, status=201)
#                 else:
#                     errors = {}
#                     errors['coach_errors'] = coach_serializer.errors
                    
#                     return Response(errors, status=400)
#             else:
#                 # If any serializer data is invalid, return errors
#                 errors = {}
#                 if not team_serializer.is_valid():
#                     errors['team_errors'] = team_serializer.errors
               
#                 return Response(errors, status=400)
        
#         elif data_type == 'teamleague':
#              # Get the data sent through HTTP POST
#             data = career_history

#             # Separate the data based on the models
#             league_data = {key: data[key] for key in ['sport_type', 'league_name', 'league_type']}
#             team_data = {key: data[key] for key in ['club_name', 'reg_id', 'country_name', 'sport_type']}
#             coach_data = {key: data[key] for key in ['club_id', 'club_name', 'from_year', 'to_year', 'league_id', 'league_name', 'country_name', 'league_type', 'achievements', 'summary', 'coach_id']}

#             # Serialize the data for each model
#             league_serializer = LeagueSerializer(data=league_data)
#             team_serializer = TeamSerializer(data=team_data)

#             # Validate the data for each model
#             if team_serializer.is_valid() and league_serializer.is_valid():
#                 team_instance = team_serializer.save()
#                 league_instance = league_serializer.save()
                
#                 # Extract 'id' from model1_instance
#                 team_id = team_instance.reg_id
#                 league_id = league_instance.id
                
#                 # Assign id to the appropriate field in Model2
#                 coach_data['club_id'] = team_id    
#                 coach_data['league_id'] = league_id    
#                 coach_serializer = FootballCoachCareerHistorySerializer(data=coach_data)
#                 if coach_serializer.is_valid():
#                     coach_career_history_instance = coach_serializer.save()
#                     endorsement_request = request.data.get('endorsement_request')
#                     if(endorsement_request != ''):
#                         endorsement_request_serializer = FootballCoachEndorsementRequestSerializer(data=endorsement_request)
#                         if endorsement_request_serializer.is_valid():
#                             try:
#                                 my_object = CustomUser.objects.get(email=endorsement_request_serializer.validated_data['to_endorser_email'])
#                                 coach_career_history = FootballCoachCareerHistory.objects.get(id=coach_career_history_instance.id)
#                                 coach_career_history.delete()
#                                 return Response({'Email Id already registered with other User'}, status=status.HTTP_400_BAD_REQUEST)
#                             except CustomUser.DoesNotExist:
#                                 new_user = {'username': team_id, 'password': 'welCome@123', 'password2': 'welCome@123', 'email': endorsement_request_serializer.validated_data['to_endorser_email'], 'reg_id':  team_id, 'is_active': False, 'club_name': coach_data['club_name'], 'account_type': 'institute'}
#                                 print(new_user)
#                                 user_serializer = UserSerializer(data=new_user)
#                                 if user_serializer.is_valid():
#                                     user_instance = user_serializer.save()
#                                     endorsement_request_serializer.validated_data['to_endorser'] = user_instance
#                                     endorsement_request_serializer.validated_data['coach_career_history'] = coach_career_history_instance
                                                    
#                                     # send_mail(
#                                     #     subject='Endorsement Request',
#                                     #     message='Endorsement request from coach for registration',
#                                     #     from_email='athletescouting@gmail.com',
#                                     #     recipient_list=[endorsement_request_serializer.validated_data['to_endorser_email']],
#                                     #     fail_silently=False,
#                                     # )
                                    
#                                     absurl = settings.BASE_URL+'register?email=' + user_instance.email
#                                     email_body = 'Hi '+ user_instance.club_name + ', you have a registration request from Bscoutd.' + '\n Use the link below to register \n' + absurl
#                                     data = {'email_body': email_body, 'to_email': user_instance.email,
#                                             'email_subject': 'Endorsement Request'}

#                                     Util.send_email(data)
                                    
#                                     endorsement_request_serializer.save()
#                                 else:
#                                     return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#                         else:
#                             return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        
#                     # Return any relevant data or success message
#                     return Response({"message": "Data saved successfully"}, status=201)
#                 else:
#                     errors = {}
#                     errors['coach_errors'] = coach_serializer.errors
                    
#                     return Response(errors, status=400)
#             else:
#                 # If any serializer data is invalid, return errors
#                 errors = {}
#                 if not team_serializer.is_valid():
#                     errors['team_errors'] = team_serializer.errors
#                 if not league_serializer.is_valid():
#                     errors['league_errors'] = league_serializer.errors
               
#                 return Response(errors, status=400)
            
#         else:
#             return Response({"error": "Invalid data type provided"}, status=400)
        
# class CoachCareerHistoryLeagueModelCreateUpdateAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         # career_history = request.data.get('career_history')
        
#         # if 'league_id' in career_history:
#         #     flag=1
#         #     league_id = career_history.get('league_id')
#         #     sport_type = career_history.get('sport_type')
#         #     print(league_id)
#         #     my_object = League.objects.get(id=league_id)
#         #     print(my_object.sport_type)
#         #     substrings = my_object.sport_type.split(',')
#         #     print(f"Substrings are {substrings}")
#         #     for substring in substrings:
#         #         print(f"Sport type: {sport_type} found in the list.")
#         #         if(substring.lower() == sport_type.lower()):
#         #             print(f"Substring: {substring} found in the list.")
#         #             flag = 0
#         #     if(flag == 1):
#         #         my_object.sport_type = my_object.sport_type + "," + sport_type
#         #         print(my_object.sport_type)
#         #         my_object.save()
#         #     return self.create(request, *args, **kwargs)
#         # else:
#         #     return self.create(request, *args, **kwargs)

#     # def create(self, request, *args, **kwargs):
#         career_history = request.data.get('career_history')
#         coach_career_history_serializer = FootballCoachCareerHistorySerializer(data=career_history)
#         if coach_career_history_serializer.is_valid():
#             coach_career_history_instance = coach_career_history_serializer.save()
#             endorsement_request = request.data.get('endorsement_request')
#             if(endorsement_request != ''):
#                 print(endorsement_request) 
#                 endorsement_request_serializer = FootballCoachEndorsementRequestSerializer(data=endorsement_request)
#                 if endorsement_request_serializer.is_valid():
#                     register_id = endorsement_request.get('reg_id')
#                     endorsement_request_serializer.validated_data['coach_career_history'] = coach_career_history_instance
#                     try:             
#                         my_object = CustomUser.objects.get(reg_id=register_id)
#                         endorsement_request_serializer.validated_data['to_endorser'] = my_object 
                        
#                         absurl = settings.BASE_URL+'endorsements/pending'
#                         email_body = 'Hi '+ my_object.club_name + ', you have endorsement request from coach.' +'\n Use the link below to check the endorsement request \n' + absurl
#                         data = {'email_body': email_body, 'to_email': my_object.email,
#                                 'email_subject': 'Endorsement Request'}

#                         Util.send_email(data)
                                
#                         endorsement_request_serializer.save()   
#                     except CustomUser.DoesNotExist:
#                         try:
#                             my_object = CustomUser.objects.get(email=endorsement_request_serializer.validated_data['to_endorser_email'])
#                             coach_career_history = FootballCoachCareerHistory.objects.get(id=coach_career_history_instance.id)
#                             coach_career_history.delete()
#                             return Response({'Email Id already registered with other User'}, status=status.HTTP_400_BAD_REQUEST)
#                         except CustomUser.DoesNotExist:
#                             new_user = {'username': register_id, 'password': 'welCome@123', 'password2': 'welCome@123', 'email': endorsement_request_serializer.validated_data['to_endorser_email'], 'is_active': False, 'reg_id': register_id, 'club_name': career_history['club_name'], 'account_type': 'institute'}
#                             print(new_user)
#                             user_serializer = UserSerializer(data=new_user)
#                             if user_serializer.is_valid():
#                                 user_instance = user_serializer.save()
#                                 endorsement_request_serializer.validated_data['to_endorser'] = user_instance
#                                 endorsement_request_serializer.validated_data['coach_career_history'] = coach_career_history_instance
                                
#                                 absurl = settings.BASE_URL+'register?email=' + user_instance.email
#                                 email_body = 'Hi '+ user_instance.club_name + ', you have a registration request from Bscoutd.' + '\n Use the link below to register \n' + absurl
#                                 data = {'email_body': email_body, 'to_email': user_instance.email,
#                                         'email_subject': 'Endorsement Request'}

#                                 Util.send_email(data)
                                
#                                 endorsement_request_serializer.save()
#                             else:
#                                 return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)      
#                 else:
#                     return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)            
                                
#             return Response({"message": "Data saved successfully"}, status=201)
        
#         return Response(coach_career_history_serializer.errors, status=400)

# class CoachCareerHistoryAndLeagueModelUpdateAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#     #     career_history = request.data.get('career_history')
#     #     value = career_history.get('league_id')
        
#     #     if value != '':
#     #         flag=1
#     #         league_id = career_history.get('league_id')
#     #         sport_type = career_history.get('sport_type')
#     #         print(league_id)
#     #         my_object = League.objects.get(id=league_id)
#     #         print(my_object.sport_type)
#     #         # Split the string into multiple substrings based on comma
#     #         substrings = my_object.sport_type.split(',')
#     #         print(f"Substrings are {substrings}")
#     #         for substring in substrings:
#     #             print(f"Sport type: {sport_type} found in the list.")
#     #             if(substring.lower() == sport_type.lower()):
#     #                 print(f"Substring: {substring} found in the list.")
#     #                 flag = 0
#     #         if(flag == 1):
#     #             my_object.sport_type = my_object.sport_type + "," + sport_type
#     #             print(my_object.sport_type)
#     #             my_object.save()
#     #         return self.update(request, *args, **kwargs)
#     #     else:
#     #         return self.update(request, *args, **kwargs)

#     # def update(self, request, *args, **kwargs):
#         career_history = request.data.get('career_history')
#         # Get the instance to update
#         instance_id = career_history.get('id')  # Remove 'id' from data
#         try:
#             instance = FootballCoachCareerHistory.objects.get(pk=instance_id)
#         except FootballCoachCareerHistory.DoesNotExist:
#             return Response({"error": "Instance does not exist"}, status=404)

#         # Update the instance
#         coach_career_history_serializer = FootballCoachCareerHistorySerializer(instance, data=career_history)
#         if coach_career_history_serializer.is_valid():
#             coach_career_history_serializer.save()
            
#             endorsement_request = request.data.get('endorsement_request')
#             if(endorsement_request!=''):
#                 print(endorsement_request) 
#                 endorsement_request_serializer = FootballCoachEndorsementRequestSerializer(data=endorsement_request)
#                 if endorsement_request_serializer.is_valid():
#                     register_id = endorsement_request.get('reg_id')
#                     try:             
#                         my_object = CustomUser.objects.get(reg_id=register_id)
#                         endorsement_request_serializer.validated_data['to_endorser'] = my_object 
                                    
#                         # send_mail(
#                         #     subject='Endorsement Request',
#                         #     message='Endorsement request from coach',
#                         #     from_email='athletescouting@gmail.com',
#                         #     recipient_list=[my_object.email],
#                         #     fail_silently=False,
#                         # )
                        
#                         absurl = settings.BASE_URL+'endorsements/pending'
#                         email_body = 'Hi '+ my_object.club_name + ', you have endorsement request from coach.' + '\n Use the link below to check the endorsement request \n' + absurl
#                         data = {'email_body': email_body, 'to_email': my_object.email,
#                                 'email_subject': 'Endorsement Request'}

#                         Util.send_email(data)
                        
#                         endorsement_request_serializer.save()  
#                     except CustomUser.DoesNotExist:
#                         try:
#                             my_object = CustomUser.objects.get(email=endorsement_request_serializer.validated_data['to_endorser_email'])
#                             return Response({'Email Id already registered with other User'}, status=status.HTTP_400_BAD_REQUEST)
#                         except CustomUser.DoesNotExist:
#                             new_user = {'username': register_id, 'password': 'welCome@123', 'password2': 'welCome@123', 'email': endorsement_request_serializer.validated_data['to_endorser_email'], 'is_active': False, 'reg_id': register_id, 'club_name': career_history['club_name'], 'account_type': 'institute'}
#                             print(new_user)
#                             user_serializer = UserSerializer(data=new_user)
#                             if user_serializer.is_valid():
#                                 user_instance = user_serializer.save()
#                                 endorsement_request_serializer.validated_data['to_endorser'] = user_instance
                                                        
#                                 # send_mail(
#                                 #     subject='Endorsement Request',
#                                 #     message='Endorsement request from coach for registration',
#                                 #     from_email='athletescouting@gmail.com',
#                                 #     recipient_list=[endorsement_request_serializer.validated_data['to_endorser_email']],
#                                 #     fail_silently=False,
#                                 # )
                                
#                                 absurl = settings.BASE_URL+'register?email=' + user_instance.email
#                                 email_body = 'Hi '+ user_instance.club_name + ', you have a registration request from Bscoutd.' + '\n Use the link below to register \n' + absurl
#                                 data = {'email_body': email_body, 'to_email': user_instance.email,
#                                         'email_subject': 'Endorsement Request'}

#                                 Util.send_email(data)
                                
#                                 endorsement_request_serializer.save()
#                             else:
#                                 return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#                 else:
#                     return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)            
                                
#             return Response({"message": "Data saved successfully"}, status=201)
#         return Response(coach_career_history_serializer.errors, status=400)
    
# class CoachCareerHistoryTeamAndLeagueModelUpdateAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         # Assuming the request data contains a 'type' field indicating the model
#         career_history = request.data.get('career_history')
#         data_type = career_history.get('flag')

#         if data_type == 'league':
#             data = career_history

#             # Separate the data based on the models
#             league_data = {key: data[key] for key in ['sport_type', 'league_name', 'league_type']}
#             coach_data = {key: data[key] for key in ['id', 'club_id', 'club_name', 'from_year', 'to_year', 'league_id', 'league_name', 'country_name', 'league_type', 'achievements', 'summary']}
#             # And so on...

#             # Serialize the data for each model
#             league_serializer = LeagueSerializer(data=league_data)

#             # Validate the data for each model
#             if league_serializer.is_valid():
#                 league_instance = league_serializer.save()
                
#                 # Extract 'id' from model1_instance
#                 league_id = league_instance.id
                
#                 # Assign id to the appropriate field in Model2
#                 coach_data['league_id'] = league_id
    
#                 # Get the instance to update
#                 instance_id = data.get('id')  # Remove 'id' from data
#                 try:
#                     instance = FootballCoachCareerHistory.objects.get(pk=instance_id)
#                 except FootballCoachCareerHistory.DoesNotExist:
#                     return Response({"error": "Instance does not exist"}, status=404)

#                 # Update the instance
#                 coach_serializer = FootballCoachCareerHistorySerializer(instance, data=coach_data)
#                 if coach_serializer.is_valid():
#                     # player_career_history_instance = player_serializer.save()
#                     coach_serializer.save()

#                     endorsement_request = request.data.get('endorsement_request')
#                     if(endorsement_request != ''):
#                         print(endorsement_request) 
#                         endorsement_request_serializer = FootballPlayerEndorsementRequestSerializer(data=endorsement_request)
#                         if endorsement_request_serializer.is_valid():
#                             register_id = endorsement_request.get('reg_id')
#                             try:     
#                                 my_object = CustomUser.objects.get(reg_id=endorsement_request_serializer.validated_data['to_endorser'])
#                                 endorsement_request_serializer.validated_data['to_endorser'] = my_object 
                                    
#                                 # send_mail(
#                                 #     subject='Endorsement Request',
#                                 #     message='Endorsement request from coach',
#                                 #     from_email='athletescouting@gmail.com',
#                                 #     recipient_list=[my_object.email],
#                                 #     fail_silently=False,
#                                 # )
                                
#                                 absurl = settings.BASE_URL+'endorsements/pending'
#                                 email_body = 'Hi '+ my_object.club_name + ', you have endorsement request from coach.' + '\n Use the link below to check the endorsement request \n' + absurl
#                                 data = {'email_body': email_body, 'to_email': my_object.email,
#                                         'email_subject': 'Endorsement Request'}

#                                 Util.send_email(data)
                        
#                                 endorsement_request_serializer.save()  
#                             except CustomUser.DoesNotExist:
#                                 try:
#                                     my_object = CustomUser.objects.get(email=endorsement_request_serializer.validated_data['to_endorser_email'])
#                                     return Response({'Email Id already registered with other User'}, status=status.HTTP_400_BAD_REQUEST)
#                                 except CustomUser.DoesNotExist:
#                                     new_user = {'username': register_id, 'password': 'welCome@123', 'password2': 'welCome@123', 'email': endorsement_request_serializer.validated_data['to_endorser_email'], 'is_active': False, 'reg_id': register_id, 'club_name': coach_data['club_name'], 'account_type': 'institute'}
#                                     print(new_user)
#                                     user_serializer = UserSerializer(data=new_user)
#                                     if user_serializer.is_valid():
#                                         user_instance = user_serializer.save()
#                                         endorsement_request_serializer.validated_data['to_endorser'] = user_instance
                                                                
#                                         # send_mail(
#                                         #     subject='Endorsement Request',
#                                         #     message='Endorsement request from coach for registration',
#                                         #     from_email='athletescouting@gmail.com',
#                                         #     recipient_list=[endorsement_request_serializer.validated_data['to_endorser_email']],
#                                         #     fail_silently=False,
#                                         # )
                                        
#                                         absurl = settings.BASE_URL+'register?email=' + user_instance.email
#                                         email_body = 'Hi '+ user_instance.club_name + ', you have a registration request from Bscoutd.' + '\n Use the link below to register \n' + absurl
#                                         data = {'email_body': email_body, 'to_email': user_instance.email,
#                                                 'email_subject': 'Endorsement Request'}

#                                         Util.send_email(data)
                                
#                                         endorsement_request_serializer.save()
#                                     else:
#                                         return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
#                         else:
#                             return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)            
                                
#                     return Response({"message": "Data saved successfully"}, status=201)
                
#                 return Response(coach_serializer.errors, status=400)
#             else:
#                 # If any serializer data is invalid, return errors
#                 errors = {}
#                 if not league_serializer.is_valid():
#                     errors['league_errors'] = league_serializer.errors
        
#                 return Response(errors, status=400)
            
#         if data_type == 'leaguenull':
#             data = career_history

#             # Separate the data based on the models
#             coach_data = {key: data[key] for key in ['id', 'club_id', 'club_name', 'from_year', 'to_year', 'country_name', 'league_type', 'achievements', 'summary']}
#             # And so on...
    
#             # Get the instance to update
#             instance_id = data.get('id')  # Remove 'id' from data
#             try:
#                 instance = FootballCoachCareerHistory.objects.get(pk=instance_id)
#             except FootballCoachCareerHistory.DoesNotExist:
#                 return Response({"error": "Instance does not exist"}, status=404)

#             # Update the instance
#             coach_serializer = FootballCoachCareerHistorySerializer(instance, data=coach_data)
#             if coach_serializer.is_valid():
#                 # player_career_history_instance = player_serializer.save()
#                 coach_serializer.save()

#                 endorsement_request = request.data.get('endorsement_request')
#                 if(endorsement_request != ''):
#                     print(endorsement_request) 
#                     endorsement_request_serializer = FootballPlayerEndorsementRequestSerializer(data=endorsement_request)
#                     if endorsement_request_serializer.is_valid():
#                         register_id = endorsement_request.get('reg_id')
#                         try:     
#                             my_object = CustomUser.objects.get(reg_id=endorsement_request_serializer.validated_data['to_endorser'])
#                             endorsement_request_serializer.validated_data['to_endorser'] = my_object 
                                    
#                                 # send_mail(
#                                 #     subject='Endorsement Request',
#                                 #     message='Endorsement request from coach',
#                                 #     from_email='athletescouting@gmail.com',
#                                 #     recipient_list=[my_object.email],
#                                 #     fail_silently=False,
#                                 # )
                                
#                             absurl = settings.BASE_URL+'endorsements/pending'
#                             email_body = 'Hi '+ my_object.club_name + ', you have endorsement request from coach.' + '\n Use the link below to check the endorsement request \n' + absurl
#                             data = {'email_body': email_body, 'to_email': my_object.email,
#                                     'email_subject': 'Endorsement Request'}

#                             Util.send_email(data)
                        
#                             endorsement_request_serializer.save()  
#                         except CustomUser.DoesNotExist:
#                             try:
#                                 my_object = CustomUser.objects.get(email=endorsement_request_serializer.validated_data['to_endorser_email'])
#                                 return Response({'Email Id already registered with other User'}, status=status.HTTP_400_BAD_REQUEST)
#                             except CustomUser.DoesNotExist:
#                                 new_user = {'username': register_id, 'password': 'welCome@123', 'password2': 'welCome@123', 'email': endorsement_request_serializer.validated_data['to_endorser_email'], 'is_active': False, 'reg_id': register_id, 'club_name': coach_data['club_name'], 'account_type': 'institute'}
#                                 print(new_user)
#                                 user_serializer = UserSerializer(data=new_user)
#                                 if user_serializer.is_valid():
#                                     user_instance = user_serializer.save()
#                                     endorsement_request_serializer.validated_data['to_endorser'] = user_instance
                                                                
#                                         # send_mail(
#                                         #     subject='Endorsement Request',
#                                         #     message='Endorsement request from coach for registration',
#                                         #     from_email='athletescouting@gmail.com',
#                                         #     recipient_list=[endorsement_request_serializer.validated_data['to_endorser_email']],
#                                         #     fail_silently=False,
#                                         # )
                                        
#                                     absurl = settings.BASE_URL+'register?email=' + user_instance.email
#                                     email_body = 'Hi '+ user_instance.club_name + ', you have a registration request from Bscoutd.' + '\n Use the link below to register \n' + absurl
#                                     data = {'email_body': email_body, 'to_email': user_instance.email,
#                                             'email_subject': 'Endorsement Request'}

#                                     Util.send_email(data)
                                
#                                     endorsement_request_serializer.save()
#                                 else:
#                                     return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
#                     else:
#                         return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)            
                                
#                 return Response({"message": "Data saved successfully"}, status=201)
                
#             return Response(coach_serializer.errors, status=400)
            
#         elif data_type == 'team':
#              # Get the data sent through HTTP POST
#             data = career_history
            
#             # if 'league_id' in data:
#             #     flag=1
#             #     league_id = data.get('league_id')
#             #     sport_type = data.get('sport_type')
#             #     print(league_id)
#             #     my_object = League.objects.get(id=league_id)
#             #     print(my_object.sport_type)
#             #     substrings = my_object.sport_type.split(',')
#             #     print(f"Substrings are {substrings}")
#             #     for substring in substrings:
#             #         print(f"Sport type: {sport_type} found in the list.")
#             #         if(substring.lower() == sport_type.lower()):
#             #             print(f"Substring: {substring} found in the list.")
#             #             flag = 0
#             #     if(flag == 1):
#             #         my_object.sport_type = my_object.sport_type + "," + sport_type
#             #         print(my_object.sport_type)
#             #         my_object.save()

#             # Separate the data based on the models
#             team_data = {key: data[key] for key in ['club_name', 'reg_id', 'country_name', 'sport_type']}
#             coach_data = {key: data[key] for key in ['id', 'club_id', 'club_name', 'from_year', 'to_year', 'league_id', 'league_name', 'country_name', 'league_type', 'achievements', 'summary']}
#             # And so on...

#             # Serialize the data for each model
#             team_serializer = TeamSerializer(data=team_data)

#             # Validate the data for each model
#             if team_serializer.is_valid():
#                 team_instance = team_serializer.save()
                
#                 # Extract 'id' from model1_instance
#                 team_id = team_instance.reg_id
                
#                 # Assign id to the appropriate field in Model2
#                 coach_data['club_id'] = team_id   
#                 instance_id = data.get('id')  # Remove 'id' from data
#                 try:
#                     instance = FootballCoachCareerHistory.objects.get(pk=instance_id)
#                 except FootballCoachCareerHistory.DoesNotExist:
#                     return Response({"error": "Instance does not exist"}, status=404)

#                 # Update the instance
#                 coach_serializer = FootballCoachCareerHistorySerializer(instance, data=coach_data)
#                 if coach_serializer.is_valid():
#                     # player_career_history_instance = club_serializer.save()
#                     coach_serializer.save()
                    
#                     endorsement_request = request.data.get('endorsement_request')
#                     if(endorsement_request != ''):
#                         endorsement_request_serializer = FootballPlayerEndorsementRequestSerializer(data=endorsement_request)
#                         if endorsement_request_serializer.is_valid():
#                             try:
#                                 my_object = CustomUser.objects.get(email=endorsement_request_serializer.validated_data['to_endorser_email'])
#                                 return Response({'Email Id already registered with other User'}, status=status.HTTP_400_BAD_REQUEST)
#                             except CustomUser.DoesNotExist:
#                                 new_user = {'username': team_id, 'password': 'welCome@123', 'password2': 'welCome@123', 'email': endorsement_request_serializer.validated_data['to_endorser_email'], 'reg_id':  team_id, 'is_active': False, 'club_name': coach_data['club_name'], 'account_type': 'institute'}
#                                 print(new_user)
#                                 user_serializer = UserSerializer(data=new_user)
#                                 if user_serializer.is_valid():
#                                     user_instance = user_serializer.save()
#                                     endorsement_request_serializer.validated_data['to_endorser'] = user_instance
#                                     # endorsement_request_serializer.validated_data['player_career_history'] = player_career_history_instance
                                                    
#                                     # send_mail(
#                                     #     subject='Endorsement Request',
#                                     #     message='Endorsement request from coach for registration',
#                                     #     from_email='athletescouting@gmail.com',
#                                     #     recipient_list=[endorsement_request_serializer.validated_data['to_endorser_email']],
#                                     #     fail_silently=False,
#                                     # )
                                    
#                                     absurl = settings.BASE_URL+'register?email=' + user_instance.email
#                                     email_body = 'Hi '+ user_instance.club_name + ', you have a registration request from Bscoutd.' +'\n Use the link below to register \n' + absurl
#                                     data = {'email_body': email_body, 'to_email': user_instance.email,
#                                             'email_subject': 'Endorsement Request'}

#                                     Util.send_email(data)
                                
#                                     endorsement_request_serializer.save()
#                                 else:
#                                     return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#                         else:
#                             return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#                     # Return any relevant data or success message
#                     return Response({"message": "Data updated successfully"}, status=201)
#                 else:
#                     return Response(coach_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 # If any serializer data is invalid, return errors
#                 errors = {}
#                 if not team_serializer.is_valid():
#                     errors['team_errors'] = team_serializer.errors
               
#                 return Response(errors, status=400)
            
#         elif data_type == 'teamleaguenull':
#              # Get the data sent through HTTP POST
#             data = career_history
            
#             # if 'league_id' in data:
#             #     flag=1
#             #     league_id = data.get('league_id')
#             #     sport_type = data.get('sport_type')
#             #     print(league_id)
#             #     my_object = League.objects.get(id=league_id)
#             #     print(my_object.sport_type)
#             #     substrings = my_object.sport_type.split(',')
#             #     print(f"Substrings are {substrings}")
#             #     for substring in substrings:
#             #         print(f"Sport type: {sport_type} found in the list.")
#             #         if(substring.lower() == sport_type.lower()):
#             #             print(f"Substring: {substring} found in the list.")
#             #             flag = 0
#             #     if(flag == 1):
#             #         my_object.sport_type = my_object.sport_type + "," + sport_type
#             #         print(my_object.sport_type)
#             #         my_object.save()

#             # Separate the data based on the models
#             team_data = {key: data[key] for key in ['club_name', 'reg_id', 'country_name', 'sport_type']}
#             coach_data = {key: data[key] for key in ['id', 'club_id', 'club_name', 'from_year', 'to_year', 'country_name', 'league_type', 'achievements', 'summary']}
#             # And so on...

#             # Serialize the data for each model
#             team_serializer = TeamSerializer(data=team_data)

#             # Validate the data for each model
#             if team_serializer.is_valid():
#                 team_instance = team_serializer.save()
                
#                 # Extract 'id' from model1_instance
#                 team_id = team_instance.reg_id
                
#                 # Assign id to the appropriate field in Model2
#                 coach_data['club_id'] = team_id   
#                 instance_id = data.get('id')  # Remove 'id' from data
#                 try:
#                     instance = FootballCoachCareerHistory.objects.get(pk=instance_id)
#                 except FootballCoachCareerHistory.DoesNotExist:
#                     return Response({"error": "Instance does not exist"}, status=404)

#                 # Update the instance
#                 coach_serializer = FootballCoachCareerHistorySerializer(instance, data=coach_data)
#                 if coach_serializer.is_valid():
#                     # player_career_history_instance = club_serializer.save()
#                     coach_serializer.save()
                    
#                     endorsement_request = request.data.get('endorsement_request')
#                     if(endorsement_request != ''):
#                         endorsement_request_serializer = FootballPlayerEndorsementRequestSerializer(data=endorsement_request)
#                         if endorsement_request_serializer.is_valid():
#                             try:
#                                 my_object = CustomUser.objects.get(email=endorsement_request_serializer.validated_data['to_endorser_email'])
#                                 return Response({'Email Id already registered with other User'}, status=status.HTTP_400_BAD_REQUEST)
#                             except CustomUser.DoesNotExist:
#                                 new_user = {'username': team_id, 'password': 'welCome@123', 'password2': 'welCome@123', 'email': endorsement_request_serializer.validated_data['to_endorser_email'], 'reg_id':  team_id, 'is_active': False, 'club_name': coach_data['club_name'], 'account_type': 'institute'}
#                                 print(new_user)
#                                 user_serializer = UserSerializer(data=new_user)
#                                 if user_serializer.is_valid():
#                                     user_instance = user_serializer.save()
#                                     endorsement_request_serializer.validated_data['to_endorser'] = user_instance
#                                     # endorsement_request_serializer.validated_data['player_career_history'] = player_career_history_instance
                                                    
#                                     # send_mail(
#                                     #     subject='Endorsement Request',
#                                     #     message='Endorsement request from coach for registration',
#                                     #     from_email='athletescouting@gmail.com',
#                                     #     recipient_list=[endorsement_request_serializer.validated_data['to_endorser_email']],
#                                     #     fail_silently=False,
#                                     # )
                                    
#                                     absurl = settings.BASE_URL+'register?email=' + user_instance.email
#                                     email_body = 'Hi '+ user_instance.club_name + ', you have a registration request from Bscoutd.' +'\n Use the link below to register \n' + absurl
#                                     data = {'email_body': email_body, 'to_email': user_instance.email,
#                                             'email_subject': 'Endorsement Request'}

#                                     Util.send_email(data)
                                
#                                     endorsement_request_serializer.save()
#                                 else:
#                                     return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#                         else:
#                             return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#                     # Return any relevant data or success message
#                     return Response({"message": "Data updated successfully"}, status=201)
#                 else:
#                     return Response(coach_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 # If any serializer data is invalid, return errors
#                 errors = {}
#                 if not team_serializer.is_valid():
#                     errors['team_errors'] = team_serializer.errors
               
#                 return Response(errors, status=400)
        
#         elif data_type == 'teamleague':
#              # Get the data sent through HTTP POST
#             data = career_history

#             # Separate the data based on the models
#             league_data = {key: data[key] for key in ['sport_type', 'league_name', 'league_type']}
#             team_data = {key: data[key] for key in ['club_name', 'reg_id', 'country_name', 'sport_type']}
#             coach_data = {key: data[key] for key in ['id', 'club_id', 'club_name', 'from_year', 'to_year', 'league_id', 'league_name', 'country_name', 'league_type', 'achievements', 'summary']}

#             # Serialize the data for each model
#             league_serializer = LeagueSerializer(data=league_data)
#             team_serializer = TeamSerializer(data=team_data)

#             # Validate the data for each model
#             if team_serializer.is_valid() and league_serializer.is_valid():
#                 team_instance = team_serializer.save()
#                 league_instance = league_serializer.save()
                
#                 # Extract 'id' from model1_instance
#                 team_id = team_instance.reg_id
#                 league_id = league_instance.id
                
#                 # Assign id to the appropriate field in Model2
#                 coach_data['club_id'] = team_id    
#                 coach_data['league_id'] = league_id    
#                 instance_id = data.get('id')  # Remove 'id' from data
#                 try:
#                     instance = FootballCoachCareerHistory.objects.get(pk=instance_id)
#                 except FootballCoachCareerHistory.DoesNotExist:
#                     return Response({"error": "Instance does not exist"}, status=404)

#                 # Update the instance
#                 coach_serializer = FootballCoachCareerHistorySerializer(instance, data=coach_data)
#                 if coach_serializer.is_valid():
#                     # player_career_history_instance = club_serializer.save()
#                     coach_serializer.save()
                    
#                     endorsement_request = request.data.get('endorsement_request')
#                     if(endorsement_request != ''):
#                         endorsement_request_serializer = FootballPlayerEndorsementRequestSerializer(data=endorsement_request)
#                         if endorsement_request_serializer.is_valid():
#                             try:
#                                 my_object = CustomUser.objects.get(email=endorsement_request_serializer.validated_data['to_endorser_email'])
#                                 return Response({'Email Id already registered with other User'}, status=status.HTTP_400_BAD_REQUEST)
#                             except CustomUser.DoesNotExist:
#                                 new_user = {'username': team_id, 'password': 'welCome@123', 'password2': 'welCome@123', 'email': endorsement_request_serializer.validated_data['to_endorser_email'], 'reg_id':  team_id, 'is_active': False, 'club_name': coach_data['club_name'], 'account_type': 'institute'}
#                                 print(new_user)
#                                 user_serializer = UserSerializer(data=new_user)
#                                 if user_serializer.is_valid():
#                                     user_instance = user_serializer.save()
#                                     endorsement_request_serializer.validated_data['to_endorser'] = user_instance
#                                     # endorsement_request_serializer.validated_data['player_career_history'] = player_career_history_instance
                                                    
#                                     # send_mail(
#                                     #     subject='Endorsement Request',
#                                     #     message='Endorsement request from coach for registration',
#                                     #     from_email='athletescouting@gmail.com',
#                                     #     recipient_list=[endorsement_request_serializer.validated_data['to_endorser_email']],
#                                     #     fail_silently=False,
#                                     # )
                                    
#                                     absurl = settings.BASE_URL+'register?email=' + user_instance.email
#                                     email_body = 'Hi '+ user_instance.club_name + ', you have a registration request from Bscoutd.' +'\n Use the link below to register \n' + absurl
#                                     data = {'email_body': email_body, 'to_email': user_instance.email,
#                                             'email_subject': 'Endorsement Request'}

#                                     Util.send_email(data)
                                
#                                     endorsement_request_serializer.save()
#                                 else:
#                                     return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#                         else:
#                             return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#                     # Return any relevant data or success message
#                     return Response({"message": "Data updated successfully"}, status=201)
#                 else:
#                     return Response(coach_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 # If any serializer data is invalid, return errors
#                 errors = {}
#                 if not team_serializer.is_valid():
#                     errors['team_errors'] = team_serializer.errors
#                 if not league_serializer.is_valid():
#                     errors['league_errors'] = league_serializer.errors
               
#                 return Response(errors, status=400)
#         else:
#             return Response({"error": "Invalid data type provided"}, status=400)

# New requirement/enhancement made to endorsement request of coach
class CoachCareerHistoryLeagueModelCreateUpdateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        career_history = request.data.get('career_history')
        coach_career_history_serializer = FootballCoachCareerHistorySerializer(data=career_history)
        if coach_career_history_serializer.is_valid():
            coach_career_history_instance = coach_career_history_serializer.save()
            
            endorsement_request = request.data.get('endorsement_request')
            if(endorsement_request != ''):
                print(endorsement_request)
                if isinstance(endorsement_request, list):
                    endorsement_request_serializer = FootballCoachEndorsementRequestSerializer(data=endorsement_request, many=True)
                    if endorsement_request_serializer.is_valid():
                        for item_data in endorsement_request_serializer.validated_data:
                            if item_data['to_endorser'] is None:  
                                return Response({'error':'No user found with this email.'}, status=status.HTTP_400_BAD_REQUEST)
                            else:
                                item_data['coach_career_history'] = coach_career_history_instance
                                            
                                # my_object = CustomUser.objects.get(email=item_data['to_endorser_email'])
                                my_object = CustomUser.objects.get(email=item_data['to_endorser'])
                                    
                                endorsee = CustomUser.objects.get(email=item_data['from_endorsee'])
                                            
                                absurl = settings.BASE_URL+'endorsements/pending'
                                email_body = 'Hi '+ my_object.first_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '.\nUse the link below to check the endorsement request\n' + absurl
                                data = {'email_body': email_body, 'to_email': my_object.email,
                                        'email_subject': 'Endorsement Request'}

                                Util.send_email(data)              
                        try:
                            with transaction.atomic():
                                FootballCoachEndorsementRequest.objects.bulk_create([
                                    FootballCoachEndorsementRequest(**item) for item in endorsement_request_serializer.validated_data
                                ])
                                            
                            # return Response(endorsement_request_serializer.data, status=status.HTTP_200_OK)
                        except Exception as e:
                            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"error": "Expected a list of items"}, status=status.HTTP_400_BAD_REQUEST) 
                            
            endorsement_request_to_club = request.data.get('endorsement_request_to_club')
            if(endorsement_request_to_club != ''):
                print(endorsement_request_to_club) 
                endorsement_request_serializer = FootballCoachEndorsementRequestSerializer(data=endorsement_request_to_club)
                if endorsement_request_serializer.is_valid():
                    endorsement_request_serializer.validated_data['coach_career_history'] = coach_career_history_instance
                        
                    register_id = endorsement_request_to_club.get('reg_id')  
                    from_endorsee = endorsement_request_to_club.get('from_endorsee')  
                    try:          
                        my_object = CustomUser.objects.get(reg_id=register_id)
                        endorsement_request_serializer.validated_data['to_endorser'] = my_object 
                            
                        endorsee = CustomUser.objects.get(id=from_endorsee)
                            
                        absurl = settings.BASE_URL+'endorsements/pending'
                        email_body = 'Hi '+ my_object.club_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '\nUse the link below to check the endorsement request\n' + absurl
                        data = {'email_body': email_body, 'to_email': my_object.email, 'email_subject': 'Endorsement Request'}

                        Util.send_email(data)
                                        
                        endorsement_request_serializer.save() 
                        return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK) 
                    except CustomUser.DoesNotExist:
                        return Response({'error':'Club not registered. You cannot send endorsement request.'}, status=status.HTTP_401_UNAUTHORIZED) 
                else:
                    return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)            
                                
            return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK)
        
        return Response(coach_career_history_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CoachCareerHistoryModelCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Assuming the request data contains a 'type' field indicating the model
        career_history = request.data.get('career_history')
        data_type = career_history.get('flag')
        # print(data_type)

        if data_type == 'league':
            data = career_history

            # Separate the data based on the models
            league_data = {key: data[key] for key in ['sport_type', 'league_name', 'league_type']}
            coach_data = {key: data[key] for key in ['club_id', 'club_name', 'from_year', 'to_year', 'league_id', 'league_name', 'country_name', 'league_type', 'achievements', 'summary', 'coach_id']}
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
                    coach_career_history_instance = coach_serializer.save()
                    endorsement_request = request.data.get('endorsement_request')
                    if(endorsement_request != ''):
                        print(endorsement_request)
                        if isinstance(endorsement_request, list):
                            endorsement_request_serializer = FootballCoachEndorsementRequestSerializer(data=endorsement_request, many=True)
                            if endorsement_request_serializer.is_valid():
                                for item_data in endorsement_request_serializer.validated_data:
                                    if item_data['to_endorser'] is None:  
                                        return Response({'error':'No user found with this email.'}, status=status.HTTP_400_BAD_REQUEST)
                                    else:
                                        item_data['coach_career_history'] = coach_career_history_instance
                                                    
                                        # my_object = CustomUser.objects.get(email=item_data['to_endorser_email'])
                                        my_object = CustomUser.objects.get(email=item_data['to_endorser'])
                                            
                                        endorsee = CustomUser.objects.get(email=item_data['from_endorsee'])
                                                    
                                        absurl = settings.BASE_URL+'endorsements/pending'
                                        email_body = 'Hi '+ my_object.first_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '.\nUse the link below to check the endorsement request\n' + absurl
                                        data = {'email_body': email_body, 'to_email': my_object.email,
                                                'email_subject': 'Endorsement Request'}

                                        Util.send_email(data)              
                                try:
                                    with transaction.atomic():
                                        FootballCoachEndorsementRequest.objects.bulk_create([
                                            FootballCoachEndorsementRequest(**item) for item in endorsement_request_serializer.validated_data
                                        ])
                                                    
                                    # return Response(endorsement_request_serializer.data, status=status.HTTP_200_OK)
                                except Exception as e:
                                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                            else:
                                return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({"error": "Expected a list of items"}, status=status.HTTP_400_BAD_REQUEST) 
                                    
                    endorsement_request_to_club = request.data.get('endorsement_request_to_club')
                    if(endorsement_request_to_club != ''):
                        print(endorsement_request_to_club) 
                        endorsement_request_serializer = FootballCoachEndorsementRequestSerializer(data=endorsement_request_to_club)
                        if endorsement_request_serializer.is_valid():
                            endorsement_request_serializer.validated_data['coach_career_history'] = coach_career_history_instance
                                
                            register_id = endorsement_request_to_club.get('reg_id')  
                            from_endorsee = endorsement_request_to_club.get('from_endorsee')  
                            try:          
                                my_object = CustomUser.objects.get(reg_id=register_id)
                                endorsement_request_serializer.validated_data['to_endorser'] = my_object 
                                    
                                endorsee = CustomUser.objects.get(id=from_endorsee)
                                    
                                absurl = settings.BASE_URL+'endorsements/pending'
                                email_body = 'Hi '+ my_object.club_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '\nUse the link below to check the endorsement request\n' + absurl
                                data = {'email_body': email_body, 'to_email': my_object.email, 'email_subject': 'Endorsement Request'}

                                Util.send_email(data)
                                                
                                endorsement_request_serializer.save() 
                                return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK) 
                            except CustomUser.DoesNotExist:
                                return Response({'error':'Club not registered. You cannot send endorsement request.'}, status=status.HTTP_401_UNAUTHORIZED) 
                        else:
                            return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)             
        
                    # Return any relevant data or success message
                    return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK)
                else:
                    errors = {}
                    errors['coach_errors'] = coach_serializer.errors
                    
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                # If any serializer data is invalid, return errors
                errors = {}
                if not league_serializer.is_valid():
                    errors['league_errors'] = league_serializer.errors
               
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            
        if data_type == 'leaguenull':
            data = career_history

            # Separate the data based on the models
            coach_data = {key: data[key] for key in ['club_id', 'club_name', 'from_year', 'to_year', 'country_name', 'league_type', 'achievements', 'summary', 'coach_id']}
            # And so on...
  
            coach_serializer = FootballCoachCareerHistorySerializer(data=coach_data)
            if coach_serializer.is_valid():
                coach_career_history_instance = coach_serializer.save()
                endorsement_request = request.data.get('endorsement_request')
                if(endorsement_request != ''):
                    print(endorsement_request)
                    if isinstance(endorsement_request, list):
                        endorsement_request_serializer = FootballCoachEndorsementRequestSerializer(data=endorsement_request, many=True)
                        if endorsement_request_serializer.is_valid():
                            for item_data in endorsement_request_serializer.validated_data:
                                if item_data['to_endorser'] is None:  
                                    return Response({'error':'No user found with this email.'}, status=status.HTTP_400_BAD_REQUEST)
                                else:
                                    item_data['coach_career_history'] = coach_career_history_instance
                                                
                                    # my_object = CustomUser.objects.get(email=item_data['to_endorser_email'])
                                    my_object = CustomUser.objects.get(email=item_data['to_endorser'])
                                        
                                    endorsee = CustomUser.objects.get(email=item_data['from_endorsee'])
                                                
                                    absurl = settings.BASE_URL+'endorsements/pending'
                                    email_body = 'Hi '+ my_object.first_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '.\nUse the link below to check the endorsement request\n' + absurl
                                    data = {'email_body': email_body, 'to_email': my_object.email,
                                            'email_subject': 'Endorsement Request'}

                                    Util.send_email(data)              
                            try:
                                with transaction.atomic():
                                    FootballCoachEndorsementRequest.objects.bulk_create([
                                        FootballCoachEndorsementRequest(**item) for item in endorsement_request_serializer.validated_data
                                    ])
                                                
                                # return Response(endorsement_request_serializer.data, status=status.HTTP_200_OK)
                            except Exception as e:
                                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({"error": "Expected a list of items"}, status=status.HTTP_400_BAD_REQUEST) 
                                
                endorsement_request_to_club = request.data.get('endorsement_request_to_club')
                if(endorsement_request_to_club != ''):
                    print(endorsement_request_to_club) 
                    endorsement_request_serializer = FootballCoachEndorsementRequestSerializer(data=endorsement_request_to_club)
                    if endorsement_request_serializer.is_valid():
                        endorsement_request_serializer.validated_data['coach_career_history'] = coach_career_history_instance
                            
                        register_id = endorsement_request_to_club.get('reg_id')  
                        from_endorsee = endorsement_request_to_club.get('from_endorsee')  
                        try:          
                            my_object = CustomUser.objects.get(reg_id=register_id)
                            endorsement_request_serializer.validated_data['to_endorser'] = my_object 
                                
                            endorsee = CustomUser.objects.get(id=from_endorsee)
                                
                            absurl = settings.BASE_URL+'endorsements/pending'
                            email_body = 'Hi '+ my_object.club_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '\nUse the link below to check the endorsement request\n' + absurl
                            data = {'email_body': email_body, 'to_email': my_object.email, 'email_subject': 'Endorsement Request'}

                            Util.send_email(data)
                                            
                            endorsement_request_serializer.save() 
                            return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK) 
                        except CustomUser.DoesNotExist:
                            return Response({'error':'Club not registered. You cannot send endorsement request.'}, status=status.HTTP_401_UNAUTHORIZED) 
                    else:
                        return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)            
        
                # Return any relevant data or success message
                return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK)
            else:
                errors = {}
                errors['coach_errors'] = coach_serializer.errors
                    
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)          
            
        elif data_type == 'team':
             # Get the data sent through HTTP POST
            data = career_history

            # Separate the data based on the models
            team_data = {key: data[key] for key in ['club_name', 'reg_id', 'country_name', 'sport_type']}
            coach_data = {key: data[key] for key in ['club_id', 'club_name', 'from_year', 'to_year', 'league_id', 'league_name', 'country_name', 'league_type', 'achievements', 'summary', 'coach_id']}
            # And so on...

            # Serialize the data for each model
            team_serializer = TeamSerializer(data=team_data)

            # Validate the data for each model
            if team_serializer.is_valid():
                team_instance = team_serializer.save()
                
                # Extract 'id' from model1_instance
                team_id = team_instance.reg_id
                
                # Assign id to the appropriate field in Model2
                coach_data['club_id'] = team_id    
                coach_serializer = FootballCoachCareerHistorySerializer(data=coach_data)
                if coach_serializer.is_valid():
                    coach_career_history_instance = coach_serializer.save()
                    endorsement_request = request.data.get('endorsement_request')
                    if(endorsement_request != ''):
                        print(endorsement_request)
                        if isinstance(endorsement_request, list):
                            endorsement_request_serializer = FootballCoachEndorsementRequestSerializer(data=endorsement_request, many=True)
                            if endorsement_request_serializer.is_valid():
                                for item_data in endorsement_request_serializer.validated_data:
                                    if item_data['to_endorser'] is None:  
                                        return Response({'error':'No user found with this email.'}, status=status.HTTP_400_BAD_REQUEST)
                                    else:
                                        item_data['coach_career_history'] = coach_career_history_instance
                                                    
                                        # my_object = CustomUser.objects.get(email=item_data['to_endorser_email'])
                                        my_object = CustomUser.objects.get(email=item_data['to_endorser'])
                                            
                                        endorsee = CustomUser.objects.get(email=item_data['from_endorsee'])
                                                    
                                        absurl = settings.BASE_URL+'endorsements/pending'
                                        email_body = 'Hi '+ my_object.first_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '.\nUse the link below to check the endorsement request\n' + absurl
                                        data = {'email_body': email_body, 'to_email': my_object.email,
                                                'email_subject': 'Endorsement Request'}

                                        Util.send_email(data)              
                                try:
                                    with transaction.atomic():
                                        FootballCoachEndorsementRequest.objects.bulk_create([
                                            FootballCoachEndorsementRequest(**item) for item in endorsement_request_serializer.validated_data
                                        ])
                                                    
                                    # return Response(endorsement_request_serializer.data, status=status.HTTP_200_OK)
                                except Exception as e:
                                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                            else:
                                return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({"error": "Expected a list of items"}, status=status.HTTP_400_BAD_REQUEST) 
        
                    # Return any relevant data or success message
                    return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK)
                else:
                    errors = {}
                    errors['coach_errors'] = coach_serializer.errors
                    
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                # If any serializer data is invalid, return errors
                errors = {}
                if not team_serializer.is_valid():
                    errors['team_errors'] = team_serializer.errors
               
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            
        elif data_type == 'teamleaguenull':
             # Get the data sent through HTTP POST
            data = career_history

            # Separate the data based on the models
            team_data = {key: data[key] for key in ['club_name', 'reg_id', 'country_name', 'sport_type']}
            coach_data = {key: data[key] for key in ['club_id', 'club_name', 'from_year', 'to_year', 'country_name', 'league_type', 'achievements', 'summary', 'coach_id']}
            # And so on...

            # Serialize the data for each model
            team_serializer = TeamSerializer(data=team_data)

            # Validate the data for each model
            if team_serializer.is_valid():
                team_instance = team_serializer.save()
                
                # Extract 'id' from model1_instance
                team_id = team_instance.reg_id
                
                # Assign id to the appropriate field in Model2
                coach_data['club_id'] = team_id    
                coach_serializer = FootballCoachCareerHistorySerializer(data=coach_data)
                if coach_serializer.is_valid():
                    coach_career_history_instance = coach_serializer.save()
                    endorsement_request = request.data.get('endorsement_request')
                    if(endorsement_request != ''):
                        print(endorsement_request)
                        if isinstance(endorsement_request, list):
                            endorsement_request_serializer = FootballCoachEndorsementRequestSerializer(data=endorsement_request, many=True)
                            if endorsement_request_serializer.is_valid():
                                for item_data in endorsement_request_serializer.validated_data:
                                    if item_data['to_endorser'] is None:  
                                        return Response({'error':'No user found with this email.'}, status=status.HTTP_400_BAD_REQUEST)
                                    else:
                                        item_data['coach_career_history'] = coach_career_history_instance
                                                    
                                        # my_object = CustomUser.objects.get(email=item_data['to_endorser_email'])
                                        my_object = CustomUser.objects.get(email=item_data['to_endorser'])
                                            
                                        endorsee = CustomUser.objects.get(email=item_data['from_endorsee'])
                                                    
                                        absurl = settings.BASE_URL+'endorsements/pending'
                                        email_body = 'Hi '+ my_object.first_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '.\nUse the link below to check the endorsement request\n' + absurl
                                        data = {'email_body': email_body, 'to_email': my_object.email,
                                                'email_subject': 'Endorsement Request'}

                                        Util.send_email(data)              
                                try:
                                    with transaction.atomic():
                                        FootballCoachEndorsementRequest.objects.bulk_create([
                                            FootballCoachEndorsementRequest(**item) for item in endorsement_request_serializer.validated_data
                                        ])
                                                    
                                    # return Response(endorsement_request_serializer.data, status=status.HTTP_200_OK)
                                except Exception as e:
                                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                            else:
                                return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({"error": "Expected a list of items"}, status=status.HTTP_400_BAD_REQUEST) 
        
                    # Return any relevant data or success message
                    return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK)
                else:
                    errors = {}
                    errors['coach_errors'] = coach_serializer.errors
                    
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                # If any serializer data is invalid, return errors
                errors = {}
                if not team_serializer.is_valid():
                    errors['team_errors'] = team_serializer.errors
               
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif data_type == 'teamleague':
             # Get the data sent through HTTP POST
            data = career_history

            # Separate the data based on the models
            league_data = {key: data[key] for key in ['sport_type', 'league_name', 'league_type']}
            team_data = {key: data[key] for key in ['club_name', 'reg_id', 'country_name', 'sport_type']}
            coach_data = {key: data[key] for key in ['club_id', 'club_name', 'from_year', 'to_year', 'league_id', 'league_name', 'country_name', 'league_type', 'achievements', 'summary', 'coach_id']}

            # Serialize the data for each model
            league_serializer = LeagueSerializer(data=league_data)
            team_serializer = TeamSerializer(data=team_data)

            # Validate the data for each model
            if team_serializer.is_valid() and league_serializer.is_valid():
                team_instance = team_serializer.save()
                league_instance = league_serializer.save()
                
                # Extract 'id' from model1_instance
                team_id = team_instance.reg_id
                league_id = league_instance.id
                
                # Assign id to the appropriate field in Model2
                coach_data['club_id'] = team_id    
                coach_data['league_id'] = league_id    
                coach_serializer = FootballCoachCareerHistorySerializer(data=coach_data)
                if coach_serializer.is_valid():
                    coach_career_history_instance = coach_serializer.save()
                    endorsement_request = request.data.get('endorsement_request')
                    if(endorsement_request != ''):
                        print(endorsement_request)
                        if isinstance(endorsement_request, list):
                            endorsement_request_serializer = FootballCoachEndorsementRequestSerializer(data=endorsement_request, many=True)
                            if endorsement_request_serializer.is_valid():
                                for item_data in endorsement_request_serializer.validated_data:
                                    if item_data['to_endorser'] is None:  
                                        return Response({'error':'No user found with this email.'}, status=status.HTTP_400_BAD_REQUEST)
                                    else:
                                        item_data['coach_career_history'] = coach_career_history_instance
                                                    
                                        # my_object = CustomUser.objects.get(email=item_data['to_endorser_email'])
                                        my_object = CustomUser.objects.get(email=item_data['to_endorser'])
                                            
                                        endorsee = CustomUser.objects.get(email=item_data['from_endorsee'])
                                                    
                                        absurl = settings.BASE_URL+'endorsements/pending'
                                        email_body = 'Hi '+ my_object.first_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '.\nUse the link below to check the endorsement request\n' + absurl
                                        data = {'email_body': email_body, 'to_email': my_object.email,
                                                'email_subject': 'Endorsement Request'}

                                        Util.send_email(data)              
                                try:
                                    with transaction.atomic():
                                        FootballCoachEndorsementRequest.objects.bulk_create([
                                            FootballCoachEndorsementRequest(**item) for item in endorsement_request_serializer.validated_data
                                        ])
                                                    
                                    # return Response(endorsement_request_serializer.data, status=status.HTTP_200_OK)
                                except Exception as e:
                                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                            else:
                                return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({"error": "Expected a list of items"}, status=status.HTTP_400_BAD_REQUEST) 
                        
                    # Return any relevant data or success message
                    return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK)
                else:
                    errors = {}
                    errors['coach_errors'] = coach_serializer.errors
                    
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                # If any serializer data is invalid, return errors
                errors = {}
                if not team_serializer.is_valid():
                    errors['team_errors'] = team_serializer.errors
                if not league_serializer.is_valid():
                    errors['league_errors'] = league_serializer.errors
               
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response({"error": "Invalid data type provided"}, status=status.HTTP_400_BAD_REQUEST)

class CoachCareerHistoryAndLeagueModelUpdateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        career_history = request.data.get('career_history')
        # Get the instance to update
        instance_id = career_history.get('id')  # Remove 'id' from data
        try:
            instance = FootballCoachCareerHistory.objects.get(pk=instance_id)
        except FootballCoachCareerHistory.DoesNotExist:
            return Response({"error": "Instance does not exist"}, status=404)

        # Update the instance
        coach_career_history_serializer = FootballCoachCareerHistorySerializer(instance, data=career_history)
        if coach_career_history_serializer.is_valid():
            coach_career_history_serializer.save()
            
            endorsement_request = request.data.get('endorsement_request')
            if(endorsement_request != ''):
                print(endorsement_request)
                if isinstance(endorsement_request, list):
                    endorsement_request_serializer = FootballCoachEndorsementRequestSerializer(data=endorsement_request, many=True)
                    if endorsement_request_serializer.is_valid():
                        for item_data in endorsement_request_serializer.validated_data:
                            if item_data['to_endorser'] is None:  
                                return Response({'error':'No user found with this email.'}, status=status.HTTP_400_BAD_REQUEST)
                            else:         
                                my_object = CustomUser.objects.get(email=item_data['to_endorser'])
                                    
                                endorsee = CustomUser.objects.get(email=item_data['from_endorsee'])
                                            
                                absurl = settings.BASE_URL+'endorsements/pending'
                                email_body = 'Hi '+ my_object.first_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '.\nUse the link below to check the endorsement request\n' + absurl
                                data = {'email_body': email_body, 'to_email': my_object.email,
                                        'email_subject': 'Endorsement Request'}

                                Util.send_email(data)              
                        try:
                            with transaction.atomic():
                                FootballCoachEndorsementRequest.objects.bulk_create([
                                    FootballCoachEndorsementRequest(**item) for item in endorsement_request_serializer.validated_data
                                ])
                                            
                            # return Response(endorsement_request_serializer.data, status=status.HTTP_200_OK)
                        except Exception as e:
                            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"error": "Expected a list of items"}, status=status.HTTP_400_BAD_REQUEST) 
                            
            endorsement_request_to_club = request.data.get('endorsement_request_to_club')
            if(endorsement_request_to_club != ''):
                print(endorsement_request_to_club)   
                endorsement_request_serializer = FootballCoachEndorsementRequestSerializer(data=endorsement_request_to_club)
                if endorsement_request_serializer.is_valid():
                    register_id = endorsement_request_to_club.get('reg_id')  
                    from_endorsee = endorsement_request_to_club.get('from_endorsee')  
                    try:          
                        my_object = CustomUser.objects.get(reg_id=register_id)
                        endorsement_request_serializer.validated_data['to_endorser'] = my_object 
                        
                        try:
                            FootballCoachEndorsementRequest.objects.get(to_endorser=endorsement_request_serializer.validated_data['to_endorser'], type='Club', from_endorsee=from_endorsee)
                            return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK) 
                        
                        except FootballCoachEndorsementRequest.DoesNotExist:
                            endorsee = CustomUser.objects.get(id=from_endorsee)
                                
                            absurl = settings.BASE_URL+'endorsements/pending'
                            email_body = 'Hi '+ my_object.club_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '\nUse the link below to check the endorsement request\n' + absurl
                            data = {'email_body': email_body, 'to_email': my_object.email, 'email_subject': 'Endorsement Request'}

                            Util.send_email(data)
                                            
                            endorsement_request_serializer.save() 
                            
                            return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK) 
                    
                    except CustomUser.DoesNotExist:
                        return Response({'error':'Club not registered. You cannot send endorsement request.'}, status=status.HTTP_401_UNAUTHORIZED) 
                else:
                    return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)          
                                
            return Response({"message": "Data saved successfully"}, status=status.HTTP_201_CREATED)            

        return Response(coach_career_history_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CoachCareerHistoryTeamAndLeagueModelUpdateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Assuming the request data contains a 'type' field indicating the model
        career_history = request.data.get('career_history')
        data_type = career_history.get('flag')

        if data_type == 'league':
            data = career_history

            # Separate the data based on the models
            league_data = {key: data[key] for key in ['sport_type', 'league_name', 'league_type']}
            coach_data = {key: data[key] for key in ['id', 'club_id', 'club_name', 'from_year', 'to_year', 'league_id', 'league_name', 'country_name', 'league_type', 'achievements', 'summary']}
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
                    return Response({"error": "Instance does not exist"}, status=status.HTTP_404_NOT_FOUND)

                # Update the instance
                coach_serializer = FootballCoachCareerHistorySerializer(instance, data=coach_data)
                if coach_serializer.is_valid():
                    # player_career_history_instance = player_serializer.save()
                    coach_serializer.save()

                    endorsement_request = request.data.get('endorsement_request')
                    if(endorsement_request != ''):
                        print(endorsement_request)
                        if isinstance(endorsement_request, list):
                            endorsement_request_serializer = FootballCoachEndorsementRequestSerializer(data=endorsement_request, many=True)
                            if endorsement_request_serializer.is_valid():
                                for item_data in endorsement_request_serializer.validated_data:
                                    if item_data['to_endorser'] is None:  
                                        return Response({'error':'No user found with this email.'}, status=status.HTTP_400_BAD_REQUEST)
                                    else:         
                                        my_object = CustomUser.objects.get(email=item_data['to_endorser'])
                                            
                                        endorsee = CustomUser.objects.get(email=item_data['from_endorsee'])
                                                    
                                        absurl = settings.BASE_URL+'endorsements/pending'
                                        email_body = 'Hi '+ my_object.first_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '.\nUse the link below to check the endorsement request\n' + absurl
                                        data = {'email_body': email_body, 'to_email': my_object.email,
                                                'email_subject': 'Endorsement Request'}

                                        Util.send_email(data)              
                                try:
                                    with transaction.atomic():
                                        FootballCoachEndorsementRequest.objects.bulk_create([
                                            FootballCoachEndorsementRequest(**item) for item in endorsement_request_serializer.validated_data
                                        ])
                                                    
                                    # return Response(endorsement_request_serializer.data, status=status.HTTP_200_OK)
                                except Exception as e:
                                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                            else:
                                return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({"error": "Expected a list of items"}, status=status.HTTP_400_BAD_REQUEST) 
                                    
                    endorsement_request_to_club = request.data.get('endorsement_request_to_club')
                    if(endorsement_request_to_club != ''):
                        print(endorsement_request_to_club)   
                        endorsement_request_serializer = FootballCoachEndorsementRequestSerializer(data=endorsement_request_to_club)
                        if endorsement_request_serializer.is_valid():
                            register_id = endorsement_request_to_club.get('reg_id')  
                            from_endorsee = endorsement_request_to_club.get('from_endorsee')  
                            try:          
                                my_object = CustomUser.objects.get(reg_id=register_id)
                                endorsement_request_serializer.validated_data['to_endorser'] = my_object 
                                
                                try:
                                    FootballCoachEndorsementRequest.objects.get(to_endorser=endorsement_request_serializer.validated_data['to_endorser'], type='Club', from_endorsee=from_endorsee)
                                    return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK) 
                                
                                except FootballCoachEndorsementRequest.DoesNotExist:
                                    endorsee = CustomUser.objects.get(id=from_endorsee)
                                        
                                    absurl = settings.BASE_URL+'endorsements/pending'
                                    email_body = 'Hi '+ my_object.club_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '\nUse the link below to check the endorsement request\n' + absurl
                                    data = {'email_body': email_body, 'to_email': my_object.email, 'email_subject': 'Endorsement Request'}

                                    Util.send_email(data)
                                                    
                                    endorsement_request_serializer.save() 
                                    
                                    return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK) 
                            
                            except CustomUser.DoesNotExist:
                                return Response({'error':'Club not registered. You cannot send endorsement request.'}, status=status.HTTP_401_UNAUTHORIZED) 
                        else:
                            return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)            
                                
                    return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK)
                
                return Response(coach_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                # If any serializer data is invalid, return errors
                errors = {}
                if not league_serializer.is_valid():
                    errors['league_errors'] = league_serializer.errors
        
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            
        if data_type == 'leaguenull':
            data = career_history

            # Separate the data based on the models
            coach_data = {key: data[key] for key in ['id', 'club_id', 'club_name', 'from_year', 'to_year', 'country_name', 'league_type', 'achievements', 'summary']}
            # And so on...
    
            # Get the instance to update
            instance_id = data.get('id')  # Remove 'id' from data
            try:
                instance = FootballCoachCareerHistory.objects.get(pk=instance_id)
            except FootballCoachCareerHistory.DoesNotExist:
                return Response({"error": "Instance does not exist"}, status=status.HTTP_404_NOT_FOUND)

            # Update the instance
            coach_serializer = FootballCoachCareerHistorySerializer(instance, data=coach_data)
            if coach_serializer.is_valid():
                # player_career_history_instance = player_serializer.save()
                coach_serializer.save()

                endorsement_request = request.data.get('endorsement_request')
                if(endorsement_request != ''):
                    print(endorsement_request)
                    if isinstance(endorsement_request, list):
                        endorsement_request_serializer = FootballCoachEndorsementRequestSerializer(data=endorsement_request, many=True)
                        if endorsement_request_serializer.is_valid():
                            for item_data in endorsement_request_serializer.validated_data:
                                if item_data['to_endorser'] is None:  
                                    return Response({'error':'No user found with this email.'}, status=status.HTTP_400_BAD_REQUEST)
                                else:         
                                    my_object = CustomUser.objects.get(email=item_data['to_endorser'])
                                        
                                    endorsee = CustomUser.objects.get(email=item_data['from_endorsee'])
                                                
                                    absurl = settings.BASE_URL+'endorsements/pending'
                                    email_body = 'Hi '+ my_object.first_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '.\nUse the link below to check the endorsement request\n' + absurl
                                    data = {'email_body': email_body, 'to_email': my_object.email,
                                            'email_subject': 'Endorsement Request'}

                                    Util.send_email(data)              
                            try:
                                with transaction.atomic():
                                    FootballCoachEndorsementRequest.objects.bulk_create([
                                        FootballCoachEndorsementRequest(**item) for item in endorsement_request_serializer.validated_data
                                    ])
                                                
                                # return Response(endorsement_request_serializer.data, status=status.HTTP_200_OK)
                            except Exception as e:
                                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({"error": "Expected a list of items"}, status=status.HTTP_400_BAD_REQUEST) 
                                
                endorsement_request_to_club = request.data.get('endorsement_request_to_club')
                if(endorsement_request_to_club != ''):
                    print(endorsement_request_to_club)   
                    endorsement_request_serializer = FootballCoachEndorsementRequestSerializer(data=endorsement_request_to_club)
                    if endorsement_request_serializer.is_valid():
                        register_id = endorsement_request_to_club.get('reg_id')  
                        from_endorsee = endorsement_request_to_club.get('from_endorsee')  
                        try:          
                            my_object = CustomUser.objects.get(reg_id=register_id)
                            endorsement_request_serializer.validated_data['to_endorser'] = my_object 
                            
                            try:
                                FootballCoachEndorsementRequest.objects.get(to_endorser=endorsement_request_serializer.validated_data['to_endorser'], type='Club', from_endorsee=from_endorsee)
                                return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK) 
                            
                            except FootballCoachEndorsementRequest.DoesNotExist:
                                endorsee = CustomUser.objects.get(id=from_endorsee)
                                    
                                absurl = settings.BASE_URL+'endorsements/pending'
                                email_body = 'Hi '+ my_object.club_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '\nUse the link below to check the endorsement request\n' + absurl
                                data = {'email_body': email_body, 'to_email': my_object.email, 'email_subject': 'Endorsement Request'}

                                Util.send_email(data)
                                                
                                endorsement_request_serializer.save() 
                                
                                return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK) 
                        
                        except CustomUser.DoesNotExist:
                            return Response({'error':'Club not registered. You cannot send endorsement request.'}, status=status.HTTP_401_UNAUTHORIZED) 
                    else:
                        return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)           
                                
                return Response({"message": "Data saved successfully"}, status=status.HTTP_200_OK)
                
            return Response(coach_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        elif data_type == 'team':
             # Get the data sent through HTTP POST
            data = career_history

            # Separate the data based on the models
            team_data = {key: data[key] for key in ['club_name', 'reg_id', 'country_name', 'sport_type']}
            coach_data = {key: data[key] for key in ['id', 'club_id', 'club_name', 'from_year', 'to_year', 'league_id', 'league_name', 'country_name', 'league_type', 'achievements', 'summary']}
            # And so on...

            # Serialize the data for each model
            team_serializer = TeamSerializer(data=team_data)

            # Validate the data for each model
            if team_serializer.is_valid():
                team_instance = team_serializer.save()
                
                # Extract 'id' from model1_instance
                team_id = team_instance.reg_id
                
                # Assign id to the appropriate field in Model2
                coach_data['club_id'] = team_id   
                instance_id = data.get('id')  # Remove 'id' from data
                try:
                    instance = FootballCoachCareerHistory.objects.get(pk=instance_id)
                except FootballCoachCareerHistory.DoesNotExist:
                    return Response({"error": "Instance does not exist"}, status=status.HTTP_404_NOT_FOUND)

                # Update the instance
                coach_serializer = FootballCoachCareerHistorySerializer(instance, data=coach_data)
                if coach_serializer.is_valid():
                    # player_career_history_instance = club_serializer.save()
                    coach_serializer.save()
                    
                    endorsement_request = request.data.get('endorsement_request')
                    if(endorsement_request != ''):
                        print(endorsement_request)
                        if isinstance(endorsement_request, list):
                            endorsement_request_serializer = FootballCoachEndorsementRequestSerializer(data=endorsement_request, many=True)
                            if endorsement_request_serializer.is_valid():
                                for item_data in endorsement_request_serializer.validated_data:
                                    if item_data['to_endorser'] is None:  
                                        return Response({'error':'No user found with this email.'}, status=status.HTTP_400_BAD_REQUEST)
                                    else:         
                                        my_object = CustomUser.objects.get(email=item_data['to_endorser'])
                                            
                                        endorsee = CustomUser.objects.get(email=item_data['from_endorsee'])
                                                    
                                        absurl = settings.BASE_URL+'endorsements/pending'
                                        email_body = 'Hi '+ my_object.first_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '.\nUse the link below to check the endorsement request\n' + absurl
                                        data = {'email_body': email_body, 'to_email': my_object.email,
                                                'email_subject': 'Endorsement Request'}

                                        Util.send_email(data)              
                                try:
                                    with transaction.atomic():
                                        FootballCoachEndorsementRequest.objects.bulk_create([
                                            FootballCoachEndorsementRequest(**item) for item in endorsement_request_serializer.validated_data
                                        ])
                                                    
                                    # return Response(endorsement_request_serializer.data, status=status.HTTP_200_OK)
                                except Exception as e:
                                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                            else:
                                return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({"error": "Expected a list of items"}, status=status.HTTP_400_BAD_REQUEST)
                        
                    # Return any relevant data or success message
                    return Response({"message": "Data updated successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response(coach_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                # If any serializer data is invalid, return errors
                errors = {}
                if not team_serializer.is_valid():
                    errors['team_errors'] = team_serializer.errors
               
                return Response(errors, status=400)
            
        elif data_type == 'teamleaguenull':
             # Get the data sent through HTTP POST
            data = career_history

            # Separate the data based on the models
            team_data = {key: data[key] for key in ['club_name', 'reg_id', 'country_name', 'sport_type']}
            coach_data = {key: data[key] for key in ['id', 'club_id', 'club_name', 'from_year', 'to_year', 'country_name', 'league_type', 'achievements', 'summary']}
            # And so on...

            # Serialize the data for each model
            team_serializer = TeamSerializer(data=team_data)

            # Validate the data for each model
            if team_serializer.is_valid():
                team_instance = team_serializer.save()
                
                # Extract 'id' from model1_instance
                team_id = team_instance.reg_id
                
                # Assign id to the appropriate field in Model2
                coach_data['club_id'] = team_id   
                instance_id = data.get('id')  # Remove 'id' from data
                try:
                    instance = FootballCoachCareerHistory.objects.get(pk=instance_id)
                except FootballCoachCareerHistory.DoesNotExist:
                    return Response({"error": "Instance does not exist"}, status=status.HTTP_404_NOT_FOUND)

                # Update the instance
                coach_serializer = FootballCoachCareerHistorySerializer(instance, data=coach_data)
                if coach_serializer.is_valid():
                    # player_career_history_instance = club_serializer.save()
                    coach_serializer.save()
                    
                    endorsement_request = request.data.get('endorsement_request')
                    if(endorsement_request != ''):
                        print(endorsement_request)
                        if isinstance(endorsement_request, list):
                            endorsement_request_serializer = FootballCoachEndorsementRequestSerializer(data=endorsement_request, many=True)
                            if endorsement_request_serializer.is_valid():
                                for item_data in endorsement_request_serializer.validated_data:
                                    if item_data['to_endorser'] is None:  
                                        return Response({'error':'No user found with this email.'}, status=status.HTTP_400_BAD_REQUEST)
                                    else:         
                                        my_object = CustomUser.objects.get(email=item_data['to_endorser'])
                                            
                                        endorsee = CustomUser.objects.get(email=item_data['from_endorsee'])
                                                    
                                        absurl = settings.BASE_URL+'endorsements/pending'
                                        email_body = 'Hi '+ my_object.first_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '.\nUse the link below to check the endorsement request\n' + absurl
                                        data = {'email_body': email_body, 'to_email': my_object.email,
                                                'email_subject': 'Endorsement Request'}

                                        Util.send_email(data)              
                                try:
                                    with transaction.atomic():
                                        FootballCoachEndorsementRequest.objects.bulk_create([
                                            FootballCoachEndorsementRequest(**item) for item in endorsement_request_serializer.validated_data
                                        ])
                                                    
                                    # return Response(endorsement_request_serializer.data, status=status.HTTP_200_OK)
                                except Exception as e:
                                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                            else:
                                return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({"error": "Expected a list of items"}, status=status.HTTP_400_BAD_REQUEST)
                        
                    # Return any relevant data or success message
                    return Response({"message": "Data updated successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response(coach_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                # If any serializer data is invalid, return errors
                errors = {}
                if not team_serializer.is_valid():
                    errors['team_errors'] = team_serializer.errors
               
                return Response(errors, status=400)
        
        elif data_type == 'teamleague':
             # Get the data sent through HTTP POST
            data = career_history

            # Separate the data based on the models
            league_data = {key: data[key] for key in ['sport_type', 'league_name', 'league_type']}
            team_data = {key: data[key] for key in ['club_name', 'reg_id', 'country_name', 'sport_type']}
            coach_data = {key: data[key] for key in ['id', 'club_id', 'club_name', 'from_year', 'to_year', 'league_id', 'league_name', 'country_name', 'league_type', 'achievements', 'summary']}

            # Serialize the data for each model
            league_serializer = LeagueSerializer(data=league_data)
            team_serializer = TeamSerializer(data=team_data)

            # Validate the data for each model
            if team_serializer.is_valid() and league_serializer.is_valid():
                team_instance = team_serializer.save()
                league_instance = league_serializer.save()
                
                # Extract 'id' from model1_instance
                team_id = team_instance.reg_id
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
                coach_serializer = FootballCoachCareerHistorySerializer(instance, data=coach_data)
                if coach_serializer.is_valid():
                    # player_career_history_instance = club_serializer.save()
                    coach_serializer.save()
                    
                    endorsement_request = request.data.get('endorsement_request')
                    if(endorsement_request != ''):
                        print(endorsement_request)
                        if isinstance(endorsement_request, list):
                            endorsement_request_serializer = FootballCoachEndorsementRequestSerializer(data=endorsement_request, many=True)
                            if endorsement_request_serializer.is_valid():
                                for item_data in endorsement_request_serializer.validated_data:
                                    if item_data['to_endorser'] is None:  
                                        return Response({'error':'No user found with this email.'}, status=status.HTTP_400_BAD_REQUEST)
                                    else:         
                                        my_object = CustomUser.objects.get(email=item_data['to_endorser'])
                                            
                                        endorsee = CustomUser.objects.get(email=item_data['from_endorsee'])
                                                    
                                        absurl = settings.BASE_URL+'endorsements/pending'
                                        email_body = 'Hi '+ my_object.first_name + ', you have endorsement request from ' + endorsee.first_name + ' ' + endorsee.last_name + '.\nUse the link below to check the endorsement request\n' + absurl
                                        data = {'email_body': email_body, 'to_email': my_object.email,
                                                'email_subject': 'Endorsement Request'}

                                        Util.send_email(data)              
                                try:
                                    with transaction.atomic():
                                        FootballCoachEndorsementRequest.objects.bulk_create([
                                            FootballCoachEndorsementRequest(**item) for item in endorsement_request_serializer.validated_data
                                        ])
                                                    
                                    # return Response(endorsement_request_serializer.data, status=status.HTTP_200_OK)
                                except Exception as e:
                                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                            else:
                                return Response(endorsement_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({"error": "Expected a list of items"}, status=status.HTTP_400_BAD_REQUEST)
                        
                    # Return any relevant data or success message
                    return Response({"message": "Data updated successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response(coach_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                # If any serializer data is invalid, return errors
                errors = {}
                if not team_serializer.is_valid():
                    errors['team_errors'] = team_serializer.errors
                if not league_serializer.is_valid():
                    errors['league_errors'] = league_serializer.errors
               
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid data type provided"}, status=status.HTTP_400_BAD_REQUEST)
        

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
            if 'document_file' in request.data:
                data = request.data
        
                # Separate the data based on the models
                license_data = {key: data[key] for key in ['license_name']}
                agent_data = {key: data[key] for key in ['license_id', 'license_name', 'document_type', 'document_file', 'agent']}
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
            if 'document_file' in request.data:
                data = request.data
        
                # Separate the data based on the models
                license_data = {key: data[key] for key in ['license_name']}
                agent_data = {key: data[key] for key in ['id', 'license_id', 'license_name', 'document_type', 'document_file', 'agent']}
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
    
class GetPlayersCoachesEndorsementUnderAgentViewSet(viewsets.ModelViewSet):
    queryset = FootballPlayersAndCoachesUnderMe.objects.all()
    serializer_class = GetFootballPlayersAndCoachesUnderMeSerializer
    
    
class PlayersCoachesEndorsementUnderAgentViewSet(viewsets.ModelViewSet):
    queryset = FootballAgentEndorsementRequest.objects.all()
    serializer_class = FootballAgentEndorsementRequestSerializer
    
    @action(detail=True, methods=['get'])
    def request_list(self, request, pk=None):
    #    users = self.get_object() # retrieve an object by pk provided
       users = FootballAgentEndorsementRequest.objects.filter(to_endorser = pk).order_by('-id')
    #    user_list = MyNetworkRequest.objects.filter(id=users).distinct()
       user_list_json = GetAgentEndorsementRequestSerializer(users, many=True)
       return Response(user_list_json.data)
   

class GetFootballPlayersCoachesEndorsementUnderAgentViewSet(viewsets.ModelViewSet):
    queryset = FootballAgentEndorsementRequest.objects.all()
    serializer_class = GetAgentEndorsementRequestSerializer
    
    
class AgentCareerHisrtoryAPIView(APIView):
    def post(self, request):
        # print(request.data)
        # players_coaches_under_me=request.data.get('players_and_coaches_under_me')
        # print(players_coaches_under_me)
        # serializer = FootballPlayersAndCoachesUnderMeSerializer(data=players_coaches_under_me)
        # if serializer.is_valid():
        #     print(serializer.data)
        #     # serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer = AgentCareerHistorySerializer(data=request.data)
        if serializer.is_valid():
            # print(serializer.data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AgentCareerHistoryUpdateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        players_and_coaches_under_me = request.data.get('players_and_coaches_under_me')
        # print(players_and_coaches_under_me)
        # Check if 'id' is present in request data
        if players_and_coaches_under_me == '':
            # If 'id' is not present, it's an update operation
            return self.update(request, *args, **kwargs)
        else:
            # If 'id' is present, it's a create operation      
            print(players_and_coaches_under_me)    
            # serializer = BulkCreateAgentPlayersCoachesUnderMeSerializer(data=players_and_coaches_under_me, many=True)

            # # Validate the data for each model
            # if serializer.is_valid():
            #     serializer.save()
            #     # return self.update(request, *args, **kwargs)
            #     return Response(serializer.data, status=status.HTTP_201_CREATED)
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
            
            if isinstance(players_and_coaches_under_me, list):
                serializer = FootballPlayersAndCoachesUnderMeSerializer(data=players_and_coaches_under_me, many=True)
                if serializer.is_valid():
                    try:
                        with transaction.atomic():
                            FootballPlayersAndCoachesUnderMe.objects.bulk_create([
                                FootballPlayersAndCoachesUnderMe(**item) for item in serializer.validated_data
                            ])
                        # return Response(serializer.data, status=status.HTTP_201_CREATED)
                        return self.update(request, *args, **kwargs)
                    except Exception as e:
                        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Expected a list of items"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        # Get the instance to update
        instance_id = request.data.get('id')  # Remove 'id' from data
        try:
            instance = AgentCareerHistory.objects.get(pk=instance_id)
        except AgentCareerHistory.DoesNotExist:
            return Response({"error": "Instance does not exist"}, status=404)
        
        agent_career_history_data = {key: request.data[key] for key in ['id', 'from_year', 'to_year', 'company', 'contact_no', 'email', 'address_lane', 'zip', 'state', 'country', 'achievements', 'summary']}
        # print(agent_career_history_data)
        
        # Update the instance
        serializer = AgentCareerHistoryUpdateSerializer(instance, data=agent_career_history_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    

class AgentCreatePlayersAndCoachesEndorsementAPIView(APIView):
    def post(self, request, *args, **kwargs):
        players_coaches_under_me = request.data.get('players_coaches_under_me')
        players_coaches_under_me_serializer = FootballPlayersAndCoachesUnderMeSerializer(data=players_coaches_under_me)
        if players_coaches_under_me_serializer.is_valid():
            player_coaches_under_me_instance = players_coaches_under_me_serializer.save()
            endorsement_request = request.data.get('endorsement_request')
            # return Response(players_coaches_under_me_serializer.data, status=status.HTTP_201_CREATED)
            if isinstance(endorsement_request, list):
                serializer = FootballAgentEndorsementRequestSerializer(data=endorsement_request, many=True)
                if serializer.is_valid():
                    for item_data in serializer.validated_data:
                        # print(item_data['to_endorser'])
                        if item_data['to_endorser'] is None:
                            # random_str = generate_random_string(10)
                            # random_contact_numbers = ''.join(['9'] + [str(random.randint(2, 9)) for _ in range(1, 10)])
                            new_user = {'username': get_random_string(7), 'password': 'welCome@123', 'password2': 'welCome@123', 'email': item_data['to_endorser_email'], 'is_active': False}
                            print(new_user)
                            user_serializer = UserSerializer(data=new_user)
                            if user_serializer.is_valid():
                                user_instance = user_serializer.save()
                
                                item_data['to_endorser'] = user_instance
                                item_data['agent_players_coaches_under_me'] = player_coaches_under_me_instance
                                
                                # send_mail(
                                #     subject='Endorsement Request',
                                #     message='Endorsement request from agent for registration',
                                #     from_email='athletescouting@gmail.com',
                                #     recipient_list=[item_data['to_endorser_email']],
                                #     fail_silently=False,
                                # )
                                
                                absurl = settings.BASE_URL+'register?email=' + user_instance.email
                                email_body = 'Hi '+ user_instance.username + ', you have a registration request from Bscoutd.' +'\n Use the link below to register \n' + absurl
                                data = {'email_body': email_body, 'to_email': user_instance.email,
                                            'email_subject': 'Endorsement Request'}

                                Util.send_email(data)
                            else:
                                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            item_data['agent_players_coaches_under_me'] = player_coaches_under_me_instance
                            
                            my_object = CustomUser.objects.get(email=item_data['to_endorser_email'])
                            
                            # send_mail(
                            #     subject='Endorsement Request',
                            #     message='Endorsement Request from Agent',
                            #     from_email='athletescouting@gmail.com',
                            #     recipient_list=[item_data['to_endorser_email']],
                            #     fail_silently=False,
                            # )
                            
                            absurl = settings.BASE_URL+'endorsements/pending'
                            email_body = 'Hi '+my_object.username + ', you have endorsement request from agent.' + '\n Use the link below to check the endorsement request \n' + absurl
                            data = {'email_body': email_body, 'to_email': my_object.email,
                                        'email_subject': 'Endorsement Request'}

                            Util.send_email(data)
                            
                    try:
                        with transaction.atomic():
                            FootballAgentEndorsementRequest.objects.bulk_create([
                                FootballAgentEndorsementRequest(**item) for item in serializer.validated_data
                            ])
                            # serializer.save()
                            
                        return Response(serializer.data, status=200)
                            
                        # return self.update(request, *args, **kwargs)
                    except Exception as e:
                        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Expected a list of items"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(players_coaches_under_me_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AgentPlayerAndCoachesEndorsementUpdateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        endorsement_request = request.data.get('endorsement_request')
        # print(players_and_coaches_under_me)
        # Check if 'id' is present in request data
        if endorsement_request == '':
            # If 'id' is not present, it's an update operation
            return self.update(request, *args, **kwargs)
        else:
            # If 'id' is present, it's a create operation      
            print(endorsement_request)    
            
            if isinstance(endorsement_request, list):
                serializer = FootballAgentEndorsementRequestSerializer(data=endorsement_request, many=True)
                if serializer.is_valid():
                    for item_data in serializer.validated_data:
                        # print(item_data['to_endorser'])
                        if item_data['to_endorser'] is None:
                            # random_str = generate_random_string(10)
                            # random_contact_numbers = ''.join(['9'] + [str(random.randint(2, 9)) for _ in range(1, 10)])
                            new_user = {'username': get_random_string(7), 'password': 'welCome@123', 'password2': 'welCome@123', 'email': item_data['to_endorser_email'], 'is_active': False}
                            print(new_user)
                            user_serializer = UserSerializer(data=new_user)
                            if user_serializer.is_valid():
                                user_instance = user_serializer.save()
                                
                                item_data['to_endorser'] = user_instance
                                
                                # send_mail(
                                #     subject='Endorsement Request',
                                #     message='Endorsement request from agent for registration',
                                #     from_email='athletescouting@gmail.com',
                                #     recipient_list=[item_data['to_endorser_email']],
                                #     fail_silently=False,
                                # )
                                
                                absurl = settings.BASE_URL+'register?email=' + user_instance.email
                                email_body = 'Hi '+ user_instance.username + ', you have a registration request from Bscoutd.' +'\n Use the link below to register \n' + absurl
                                data = {'email_body': email_body, 'to_email': user_instance.email,
                                            'email_subject': 'Endorsement Request'}

                                Util.send_email(data)
                            else:
                                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            # send_mail(
                            #     subject='Endorsement Request',
                            #     message='Endorsement Request from Agent',
                            #     from_email='athletescouting@gmail.com',
                            #     recipient_list=[item_data['to_endorser_email']],
                            #     fail_silently=False,
                            # )
                            
                            my_object = CustomUser.objects.get(email=item_data['to_endorser_email'])
                            
                            absurl = settings.BASE_URL+'endorsements/pending'
                            email_body = 'Hi '+my_object.username + ', you have endorsement request from agent.' + '\n Use the link below to check the endorsement request \n' + absurl
                            data = {'email_body': email_body, 'to_email': my_object.email,
                                        'email_subject': 'Endorsement Request'}

                            Util.send_email(data)
                            
                    try:
                        with transaction.atomic():
                            FootballAgentEndorsementRequest.objects.bulk_create([
                                FootballAgentEndorsementRequest(**item) for item in serializer.validated_data
                            ])
                            # serializer.save()
                            
                        return Response(serializer.data, status=200)
                            
                        # return self.update(request, *args, **kwargs)
                    except Exception as e:
                        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Expected a list of items"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        # Get the instance to update
        instance_id = request.data.get('id')  # Remove 'id' from data
        try:
            instance = FootballPlayersAndCoachesUnderMe.objects.get(pk=instance_id)
        except FootballPlayersAndCoachesUnderMe.DoesNotExist:
            return Response({"error": "Instance does not exist"}, status=404)
        
        agent_players_coaches_under_me_data = {key: request.data[key] for key in ['id', 'type', 'user_id', 'name', 'is_notable']}
        # print(agent_career_history_data)
        
        # Update the instance
        serializer = FootballPlayersAndCoachesUnderMeSerializer(instance, data=agent_players_coaches_under_me_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

class ChangeSportProfileTypeAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Get the instance to update
        data = request.data
        instance_id = data.get('user')
        type = data.get('profile_type')
        try:
            instance = SportProfileType.objects.get(user=instance_id, profile_type=type)
            serializer = SportProfileTypeSerializer(instance, data=data)
            if serializer.is_valid():
                try:
                    player_object = SportProfileType.objects.get(user=instance_id, profile_type='Player')
                    player_object.status = 'Not Current'
                    player_object.save()
                except SportProfileType.DoesNotExist:
                    pass
                try:
                    coach_object = SportProfileType.objects.get(user=instance_id, profile_type='Coach')
                    coach_object.status = 'Not Current'
                    coach_object.save()
                except SportProfileType.DoesNotExist:
                    pass
                try:
                    agent_object = SportProfileType.objects.get(user=instance_id, profile_type='Agent')
                    agent_object.status = 'Not Current'
                    agent_object.save()
                except SportProfileType.DoesNotExist:
                    pass
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        except SportProfileType.DoesNotExist:
            return Response(serializer.errors, status=400)

# class SportProfileTypeStatusChangeCreateAndUpdateAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         # Get the instance to update
#         data = request.data
#         instance_id = data.get('user')
#         type = data.get('profile_type')
#         try:
#             instance = SportProfileType.objects.get(user=instance_id, profile_type=type)
#             serializer = SportProfileTypeSerializer(instance, data=data)
#             if serializer.is_valid():
#                 player_object = SportProfileType.objects.get(user=instance_id, profile_type='Player')
#                 player_object.status = 'Not Current'
#                 player_object.save()
#                 coach_object = SportProfileType.objects.get(user=instance_id, profile_type='Coach')
#                 coach_object.status = 'Not Current'
#                 coach_object.save()
#                 agent_object = SportProfileType.objects.get(user=instance_id, profile_type='Agent')
#                 agent_object.status = 'Not Current'
#                 agent_object.save()
#                 serializer.save()
#                 return Response(serializer.data, status=200)
#             return Response(serializer.errors, status=400)
#         except SportProfileType.DoesNotExist:
#             # If 'user_id' is not present, it's a create operation
#             serializer = SportProfileTypeSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 user_instance = CustomUser.objects.get(id=instance_id)
#                 if not user_instance.is_flag and user_instance.first_name is not None and user_instance.last_name is not None and user_instance.contact_no is not None and user_instance.dob is not None:
#                     user_instance.is_flag = True
#                     user_instance.save() 
#                 if type == 'Player':
#                     try:
#                         instance_player = Player.objects.get(user=instance_id)
#                         player_data = {key: data[key] for key in ['user']}
#                         serializer_player = PlayerSerializer(data=player_data)
#                         if serializer_player.is_valid():
#                             serializer_player.save()
#                             return Response({{"message": "Data saved successfully"}}, status=200)
#                         else:
#                             return Response(serializer_player.errors, status=400)
#                     except Player.DoesNotExist:
#                         return Response(serializer.data, status=200)
                    
#                 elif type == 'Coach':
#                     try:
#                         instance_coach = FootballCoach.objects.get(user=instance_id)
#                         coach_data = {key: data[key] for key in ['user']}
#                         serializer_coach = FootballCoachSerializer(data=coach_data)
#                         if serializer_coach.is_valid():
#                             serializer_coach.save()
#                             return Response({{"message": "Data saved successfully"}}, status=200)
#                         else:
#                             return Response(serializer_coach.errors, status=400)
#                     except FootballCoach.DoesNotExist:
#                         return Response(serializer.data, status=200)
                    
#                 elif type == 'Agent':
#                     try:
#                         instance_agent = Agent.objects.get(user=instance_id)
#                         agent_data = {key: data[key] for key in ['user']}
#                         serializer_agent = AgentSerializer(data=agent_data)
#                         if serializer_agent.is_valid():
#                             serializer_agent.save()
#                             return Response({{"message": "Data saved successfully"}}, status=200)
#                         else:
#                             return Response(serializer_agent.errors, status=400)
#                     except Agent.DoesNotExist:
#                         return Response(serializer.data, status=200)     
                        
#             return Response(serializer.errors, status=400)
        
class SportProfileTypeCreateAndUpdateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Get the instance to update
        data = request.data
        instance_id = data.get('user')
        type = data.get('profile_type')
        # player_object = SportProfileType.objects.get(user=instance_id, profile_type='Player')
        # player_object.status = 'Not Current'
        # player_object.save()
        # coach_object = SportProfileType.objects.get(user=instance_id, profile_type='Coach')
        # coach_object.status = 'Not Current'
        # coach_object.save()
        # agent_object = SportProfileType.objects.get(user=instance_id, profile_type='Agent')
        # agent_object.status = 'Not Current'
        # agent_object.save()
        try:
            instance = SportProfileType.objects.get(user=instance_id, profile_type=type)
            serializer = SportProfileTypeSerializer(instance, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        except SportProfileType.DoesNotExist:
            # If 'user_id' is not present, it's a create operation
            serializer = SportProfileTypeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                user_instance = CustomUser.objects.get(id=instance_id)
                if type != 'Institution':
                    user_instance.account_type = 'user'
                    # if not user_instance.is_flag and user_instance.first_name is not None and user_instance.last_name is not None and user_instance.contact_no is not None and user_instance.dob is not None:
                    if not user_instance.is_flag:
                        user_instance.is_flag = True
                    user_instance.save() 
                    if type == 'Player':
                        player_data = {key: data[key] for key in ['user']}
                        try:
                            instance_player = Player.objects.get(user=instance_id)
                            # player_data = {key: data[key] for key in ['user']}
                            serializer_player = PlayerSerializer(instance_player, data=player_data)
                            if serializer_player.is_valid():
                                serializer_player.save()
                                return Response({"message": "Data updated successfully"}, status=200)
                            return Response(serializer_player.errors, status=400)
                        except Player.DoesNotExist:
                            # player_data = {key: data[key] for key in ['user']}
                            serializer_player = PlayerSerializer(data=player_data)
                            if serializer_player.is_valid():
                                serializer_player.save()
                                return Response({"message": "Data saved successfully"}, status=200)
                            return Response(serializer_player.errors, status=400)
                        
                    elif type == 'Coach':
                        coach_data = {key: data[key] for key in ['user']}
                        try:
                            instance_coach = FootballCoach.objects.get(user=instance_id)
                            # coach_data = {key: data[key] for key in ['user']}
                            serializer_coach = FootballCoachSerializer(instance_coach, data=coach_data)
                            if serializer_coach.is_valid():
                                serializer_coach.save()
                                return Response({"message": "Data updated successfully"}, status=200)
                            return Response(serializer_coach.errors, status=400)
                        except FootballCoach.DoesNotExist:
                            serializer_coach = FootballCoachSerializer(data=coach_data)
                            if serializer_coach.is_valid():
                                serializer_coach.save()
                                return Response({"message": "Data saved successfully"}, status=200)
                            return Response(serializer_coach.errors, status=400)
                        
                    elif type == 'Agent':
                        agent_data = {key: data[key] for key in ['user']}
                        try:
                            instance_agent = Agent.objects.get(user=instance_id)
                            # agent_data = {key: data[key] for key in ['user']}
                            serializer_agent = AgentSerializer(instance_agent, data=agent_data)
                            if serializer_agent.is_valid():
                                serializer_agent.save()
                                return Response({"message": "Data updated successfully"}, status=200)
                            return Response(serializer_agent.errors, status=400)
                        except Agent.DoesNotExist:
                            serializer_agent = AgentSerializer(data=agent_data)
                            if serializer_agent.is_valid():
                                serializer_agent.save()
                                return Response({"message": "Data saved successfully"}, status=200)
                            return Response(serializer_agent.errors, status=400) 
                else:
                    user_instance.account_type = 'institute'
                    # if not user_instance.is_flag and user_instance.club_name is not None and user_instance.contact_no is not None and user_instance.dob is not None:
                    #     user_instance.is_flag = True
                    # to be removed
                    try:
                       Team.objects.get(reg_id=user_instance.reg_id)
                    except Team.DoesNotExist:
                        register_id = str(uuid.uuid4())[:36]
                        # Manually construct the data you want to save
                        team_data = {
                            'club_name': user_instance.club_name,  # Replace with actual values or variables
                            'reg_id': register_id,
                            # ... other fields ...
                        }
                        user_instance.reg_id=register_id
                        # print(team_data)
                        team_serializer = TeamSerializer(data=team_data)
                        
                        if team_serializer.is_valid():
                            team_serializer.save()
                    
                    user_instance.save()
                    club_data = {key: data[key] for key in ['user']}
                    try:
                        instance_club = FootballClub.objects.get(user=instance_id)
                        # club_data = {key: data[key] for key in ['user']}
                        serializer_club = FootballClubSerializer(instance_club, data=club_data)
                        if serializer_club.is_valid():
                            serializer_club.save()
                            return Response({"message": "Data updated successfully"}, status=201)
                        return Response(serializer_club.errors, status=400)
                    except FootballClub.DoesNotExist:
                        # club_data = {key: data[key] for key in ['user']}
                        serializer_club = FootballClubSerializer(data=club_data)
                        if serializer_club.is_valid():
                            serializer_club.save()
                            return Response({"message": "Data saved successfully"}, status=200)        
                        return Response(serializer_club.errors, status=400)         
            return Response(serializer.errors, status=400)

        
# added by Pijush
#User = get_user_model()  # Get the User model dynamically

class OpportunityViewSet(viewsets.ModelViewSet):
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer
#    permission_classes = [IsAuthenticated]

class OpportunityApplicationsViewSet(viewsets.ModelViewSet):
    queryset = OpportunityApplications.objects.all()
    serializer_class = OpportunityApplicationsSerializer

class HelpViewSet(viewsets.ModelViewSet):
    queryset = Help.objects.all()
    serializer_class = HelpSerializer

class HelpSupportViewSet(viewsets.ModelViewSet):
    queryset = HelpSupports.objects.all()
    serializer_class = HelpSupportsSerializer

class WellnessScoreViewSet(viewsets.ModelViewSet):
    queryset = WellnessScore.objects.all()
    serializer_class = WellnessScoreSerializer
    
class ConditioningLogViewSet(viewsets.ModelViewSet):
    queryset = ConditioningLog.objects.all()
    serializer_class = ConditioningLogSerializer
# end of Added by Pijush

# changes made by me

class GetInstitutionViewSet(APIView):
    def get(self, request, slug):
        try:
            CustomUser.objects.get(reg_id=slug)
            return Response(status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
# class GetPlayerEndorsementRequest(viewsets.ModelViewSet):
#     queryset = FootballPlayerEndorsementRequest.objects.all()
#     serializer_class = FootballPlayerEndorsementRequestSerializer
    
#     @action(detail=True, methods=['get'])
#     def request_list(self, request, pk=None):
#     #    users = self.get_object() # retrieve an object by pk provided
#        users = FootballPlayerEndorsementRequest.objects.filter(to_endorser = pk)
#     #    user_list = MyNetworkRequest.objects.filter(id=users).distinct()
#        user_list_json = FootballPlayerEndorsementRequestSerializer(users, many=True)
#        return Response(user_list_json.data)

class GetPlayerEndorsementRequest(APIView):
    def get(self, request):
        # Extract the filter value from the query parameters
        user_id = request.GET.get('user_id')  # or any other field you want to filter by
        
        # Filter the data based on the extracted value
        filtered_data = FootballPlayerEndorsementRequest.objects.filter(to_endorser=user_id)
        
        # Serialize the filtered data
        serializer = GetPlayerEndorsementRequestSerializer(filtered_data, many=True)
        
        # Return the serialized data as a response
        return Response(serializer.data)
    
class GetCoachEndorsementRequest(APIView):
    def get(self, request):
        # Extract the filter value from the query parameters
        user_id = request.GET.get('user_id')  # or any other field you want to filter by
        
        # Filter the data based on the extracted value
        filtered_data = FootballCoachEndorsementRequest.objects.filter(to_endorser=user_id)
        
        # Serialize the filtered data
        serializer = GetCoachEndorsementRequestSerializer(filtered_data, many=True)
        
        # Return the serialized data as a response
        return Response(serializer.data)
        
class DeleteAllUsersView(APIView):
    def delete(self, request):
        CustomUser.objects.all().delete()
        Address.objects.all().delete()
        return Response({"message": "All users deleted"}, status=status.HTTP_204_NO_CONTENT)
    
class CreateInstituteProfileView(APIView):
    def post(self, request):
        data = request.data
        emailId = data.get('email')
        pwd = data.get('password')
        try:
            user = CustomUser.objects.get(email=emailId)
            if user.check_password('welCome@123'):
                try:
                    validators.validate_password(pwd)
                    user.set_password(pwd)
                    user.is_active = True
                    user.save()
                    token = RefreshToken.for_user(user).access_token
                    current_site = get_current_site(request).domain
                    relativeLink = reverse('email-verify')
                    absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
                    email_body = 'Hi '+user.club_name + ',\n Use the link below to verify your email \n' + absurl
                    data = {'email_body': email_body, 'to_email': user.email,
                            'email_subject': 'Verify your email'}

                    Util.send_email(data)
                    return Response({"message": "Data saved successfully. Please check your mail for verification your user's account."}, status=status.HTTP_200_OK)
                except ValidationError as exc:
                    raise serializers.ValidationError({'password': exc.messages})
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_401_UNAUTHORIZED)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

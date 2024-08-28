from rest_framework import serializers
from football.models import *
import django.contrib.auth.password_validation as validators
from django.core.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = CustomUser
        fields = ['token']
        
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=3, read_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = CustomUser.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = CustomUser.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)

        if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }

        return super().validate(attrs)

class SportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        ordering = ['-id']
        model = Type
        fields = ("id", "sport_type")

class TeamSerializer(serializers.ModelSerializer):
    # sport_type = SportTypeSerializer(many=True, read_only=True)
    
    class Meta:
        ordering = ['-id']
        model = Team
        # fields = ("id", "team_name", "reg_id", "country_name", "sport_type", "league_id")
        fields = ("id", "club_name", "reg_id", "country_name", "sport_type")
        
class LeagueSerializer(serializers.ModelSerializer):
    # teams = TeamSerializer(many=True, read_only=True)

    class Meta:
        ordering = ['-id']
        model = League
        fields = "__all__"
        
class CountrySerializer(serializers.ModelSerializer):
    # leagues = LeagueSerializer(many=True, read_only=True)
    class Meta:
        ordering = ['-id']
        model = Country
        fields = ("id", "country_name")

class NetworkConnectionsSerializer(serializers.ModelSerializer):
    # connect_to_user = ConnectUserSerializer()

    class Meta:
        ordering = ['-id']
        model = NetworkConnected
        fields = ("id", "connect_to_user", "status", "user_id", "network_request_id")
        extra_kwargs = {'user_id': {'required': False}}

class ProfilePhotoSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = ProfilePhoto
        fields = ("id", "photo", "user_id")
        extra_kwargs = {'user_id': {'required': False}}

# class PersonalAchievementsSerializer(serializers.ModelSerializer):

#     class Meta:
#         ordering = ['-id']
#         model = PersonalAchievements
#         fields = ("id", "achievement_name", "period", "profile_type", "user_id")
#         extra_kwargs = {'user_id': {'required': False}}
        
class SportProfileTypeSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = SportProfileType
        fields = '__all__'
        extra_kwargs = {'user_id': {'required': False}}

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = Address
        fields = ("id", "address_lane", "landmark", "city", "pin", "state", "country", "address_type", "is_active", "permanent_user_id", "present_user_id")
        extra_kwargs = {'permanent_user_id': {'required': False}, 'present_user_id': {'required': False}}

class PlayerVideoClipSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = PlayerVideoClip
        fields = ("id", "title", "profile_type", "clip_url", "user_id")
        extra_kwargs = {'user_id': {'required': False}}

class ProfileDescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = ProfileDescription
        fields = ("id", "title","description", "profile_type","user_id")
        extra_kwargs = {'user_id': {'required': False}}

class CustomUserSerializer(serializers.ModelSerializer):
    sport_profile_type = SportProfileTypeSerializer(many=True, read_only=True)
    # personal_achievements = PersonalAchievementsSerializer(many=True, read_only=True)
    profile_description = ProfileDescriptionSerializer(many=True, read_only=True)
    connected_users = NetworkConnectionsSerializer(many=True, read_only=True)
    age = serializers.SerializerMethodField()

    class Meta(object):
        model = CustomUser 
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'sport_profile_type' : {'required': False},
            'profile_description' : {'required': False}
        }
        
    def get_age(self, obj):
        return obj.calculate_age()
    
# class GetPlayerEndorsementSerializer(serializers.ModelSerializer):
#     player_career_history = PlayerCareerHistorySerializer()

#     class Meta:
#         ordering = ['-id']
#         model = FootballPlayerEndorsementRequest
#         fields = "__all__"
    
class GetFootballPlayerEndorsementRequestSerializer(serializers.ModelSerializer):
    to_endorser = CustomUserSerializer()
    from_endorsee = CustomUserSerializer()

    class Meta:
        ordering = ['-id']
        model = FootballPlayerEndorsementRequest
        fields = "__all__"
    
class FootballPlayerEndorsementRequestSerializer(serializers.ModelSerializer):
    # reg_id = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        ordering = ['-id']
        model = FootballPlayerEndorsementRequest
        fields = "__all__"

class ClubSerializer(serializers.ModelSerializer):
    endorsement_request = GetFootballPlayerEndorsementRequestSerializer(many=True, read_only=True)

    class Meta:
        ordering = ['-id']
        model = Club
        fields = '__all__'
        extra_kwargs = {'players': {'required': False}}
        
class PlayerCareerHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Club
        fields = '__all__'
  
# class GetPlayerEndorsementSerializer(serializers.ModelSerializer):
#     player_career_history = PlayerCareerHistorySerializer()

#     class Meta:
#         ordering = ['-id']
#         model = FootballPlayerEndorsementRequest
#         fields = "__all__"    
          
class GetPlayerEndorsementRequestSerializer(serializers.ModelSerializer):
    from_endorsee = CustomUserSerializer()
    player_career_history = PlayerCareerHistorySerializer()
    
    class Meta:
        model = FootballPlayerEndorsementRequest
        fields = "__all__"

# class AcheivementsSerializer(serializers.ModelSerializer):

#     class Meta:
#         ordering = ['-id']
#         model = Acheivements
#         fields = ("id", "acheivement_name", "period", "player_id", "coach_id", "club_id")
#         extra_kwargs = {'player_id': {'required': False}, 'coach_id': {'required': False}, 'club_id':  {'required': False}}

class FootballClubOfficeBearerSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = FootballClubOfficeBearer
        fields = "__all__"
        extra_kwargs = {'club_id': {'required': False}}

class FootballClubHistorySerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = FootballClubHistory
        fields = "__all__"
        extra_kwargs = {'club_id': {'required': False}}
        
class FootballClubVerificationDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = FootballClubVerificationDocument
        fields = "__all__"
        extra_kwargs = {'club_id': {'required': False}}

class FootballClubSerializer(serializers.ModelSerializer):
    # user = ClubUserSerializer()
    office_bearer = FootballClubOfficeBearerSerializer(many=True, read_only=True)
    club_history = FootballClubHistorySerializer(many=True, read_only=True)
    verification_document = FootballClubVerificationDocumentSerializer(many=True, read_only=True)
    # club_acheivements = AcheivementsSerializer(many=True, read_only=True)
    # player_current_club_inside = PlayerSerializer(many=True, read_only=True)
    # coach_current_club_inside = FootballCoachSerializer(many=True, read_only=True)

    class Meta:
        ordering = ['-id']
        model = FootballClub
        fields = "__all__"
        extra_kwargs = {'office_bearer': {'required': False}, 'club_history': {'required': False}, 'verification_document': {'required': False}}

class GetFootballClubSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    office_bearer = FootballClubOfficeBearerSerializer(many=True, read_only=True)
    club_history = FootballClubHistorySerializer(many=True, read_only=True)
    # club_acheivements = AcheivementsSerializer(many=True, read_only=True)
    # player_current_club_inside = PlayerSerializer(many=True, read_only=True)
    # coach_current_club_inside = FootballCoachSerializer(many=True, read_only=True)

    class Meta:
        ordering = ['-id']
        model = FootballClub
        fields = "__all__"
        extra_kwargs = {'office_bearer': {'required': False}, 'club_history': {'required': False}}
        
class AgentLicenseSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = AgentLicense
        fields = '__all__'
        extra_kwargs = {'agent': {'required': False}}
        
class AgentCareerHistoryUpdateSerializer(serializers.ModelSerializer):
    # players_and_coaches_under_me = FootballPlayersAndCoachesUnderMeSerializer(many=True)

    class Meta:
        # ordering = ['-id']
        model = AgentCareerHistory
        fields = '__all__'
        # extra_kwargs = {'players_and_coaches_under_me': {'required': False}}
        
class FootballAgentEndorsementRequestSerializer(serializers.ModelSerializer):

    class Meta:
        # ordering = ['-id']
        model = FootballAgentEndorsementRequest
        fields = "__all__"
        extra_kwargs = {'agent_players_coaches_under_me': {'required': False}}
               
class GetFootballAgentEndorsementRequestSerializer(serializers.ModelSerializer):
    to_endorser = CustomUserSerializer()
    from_endorsee = CustomUserSerializer()
    class Meta:
        # ordering = ['-id']
        model = FootballAgentEndorsementRequest
        fields = "__all__"
        extra_kwargs = {'agent_players_coaches_under_me': {'required': False}}
      
        
class FootballPlayersAndCoachesUnderAgentSerializer(serializers.ModelSerializer):
    agent_career_history = AgentCareerHistoryUpdateSerializer()
    class Meta:
        # ordering = ['-id']
        model = FootballPlayersAndCoachesUnderMe
        fields = "__all__"
        # extra_kwargs = {'endorsement_request': {'required': False}}
        
class GetAgentEndorsementRequestSerializer(serializers.ModelSerializer):
    from_endorsee = CustomUserSerializer()
    agent_players_coaches_under_me = FootballPlayersAndCoachesUnderAgentSerializer()
    class Meta:
        # ordering = ['-id']
        model = FootballAgentEndorsementRequest
        fields = "__all__"
        # extra_kwargs = {'agent_players_coaches_under_me': {'required': False}}
        
class FootballPlayersAndCoachesUnderMeSerializer(serializers.ModelSerializer):
    endorsement_request = FootballAgentEndorsementRequestSerializer(many=True, read_only=True)
    class Meta:
        # ordering = ['-id']
        model = FootballPlayersAndCoachesUnderMe
        fields = "__all__"
        extra_kwargs = {'endorsement_request': {'required': False}}
        
class GetFootballPlayersAndCoachesUnderMeSerializer(serializers.ModelSerializer):
    endorsement_request = GetFootballAgentEndorsementRequestSerializer(many=True, read_only=True)
    class Meta:
        # ordering = ['-id']
        model = FootballPlayersAndCoachesUnderMe
        fields = "__all__"
        extra_kwargs = {'endorsement_request': {'required': False}}
        
# class BulkAgentPlayersCoachesUnderMeSerializer(serializers.ListSerializer):
#     def create(self, validated_data):
#         players_coaches_under_me = [FootballPlayersAndCoachesUnderMe(**item) for item in validated_data]
#         return FootballPlayersAndCoachesUnderMe.objects.bulk_create(players_coaches_under_me)

# class BulkCreateAgentPlayersCoachesUnderMeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FootballPlayersAndCoachesUnderMe
#         fields = '__all__'
#         list_serializer_class = BulkAgentPlayersCoachesUnderMeSerializer
        
class AgentCareerHistorySerializer(serializers.ModelSerializer):
    players_and_coaches_under_me = FootballPlayersAndCoachesUnderMeSerializer(many=True)

    class Meta:
        # ordering = ['-id']
        model = AgentCareerHistory
        fields = '__all__'
        # extra_kwargs = {'players_and_coaches_under_me': {'required': False}}
        
    def create(self, validated_data):
        players_and_coaches_under_me_data = validated_data.pop('players_and_coaches_under_me')
        agent_career_history = AgentCareerHistory.objects.create(**validated_data)
        for players_and_coaches_data in players_and_coaches_under_me_data:
            FootballPlayersAndCoachesUnderMe.objects.create(agent_career_history=agent_career_history, **players_and_coaches_data)
        return agent_career_history


class AgentSerializer(serializers.ModelSerializer):
    my_license = AgentLicenseSerializer(many=True, read_only=True)
    career_history = AgentCareerHistorySerializer(many=True, read_only=True)
    # players_and_coaches_under_me = FootballPlayersAndCoachesUnderMeSerializer(many=True, read_only=True)

    class Meta:
        ordering = ['-id']
        model = Agent
        fields = "__all__"
        extra_kwargs = {'my_license': {'required': False}, 'career_history': {'required': False}}

class GetAgentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    my_license = AgentLicenseSerializer(many=True, read_only=True)
    career_history = AgentCareerHistorySerializer(many=True, read_only=True)
    # players_and_coaches_under_me = FootballPlayersAndCoachesUnderMeSerializer(many=True, read_only=True)
    
    class Meta:
        ordering = ['-id']
        model = Agent
        fields = "__all__"
        extra_kwargs = {'my_license': {'required': False}, 'career_history': {'required': False}}

# class AgentOutsideSerializer(serializers.ModelSerializer):

#     class Meta:
#         ordering = ['-id']
#         model = AgentOutside
#         fields = ("id", "agent_name", "contact", "player_id")
#         extra_kwargs = {'player_id': {'required': False}}

# class GetReferenceSerializer(serializers.ModelSerializer):
#     reffered_user = CustomUserSerializer()
#     class Meta:
#         ordering = ['-id']
#         model = Reference
#         fields = ("id", "reffered_user", "player_id")
#         extra_kwargs = {'player_id': {'required': False}}

# class ReferenceSerializer(serializers.ModelSerializer):

#     class Meta:
#         ordering = ['-id']
#         model = Reference
#         fields = ("id", "reffered_user", "player_id")
#         extra_kwargs = {'player_id': {'required': False}}

# class ReferenceOutsideSerializer(serializers.ModelSerializer):

#     class Meta:
#         ordering = ['-id']
#         model = ReferenceOutside
#         fields = ("id", "reference_name", "contact", "player_id")
#         extra_kwargs = {'player_id': {'required': False}}

class PlayerSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    club = ClubSerializer(many=True, read_only=True)
    # current_club_inside = FootballClubSerializer()
    # video_clip = PlayerVideoClipSerializer(many=True, read_only=True)
    # carreer_history = PlayerCareerHistorySerializer(many=True, read_only=True)
    # player_acheivements = AcheivementsSerializer(many=True, read_only=True)
    # player_current_club_inside = FootballClubSerializer(many=True, read_only=True)
    # agent_inside = GetAgentInsideSerializer(many=True, read_only=True)
    # agent_outside = AgentOutsideSerializer(many=True, read_only=True)
    # reference_users_inside = GetReferenceSerializer(many=True, read_only=True)
    # reference_users_outside = ReferenceOutsideSerializer(many=True, read_only=True)

    class Meta:
        ordering = ['-id']
        model = Player
        fields = "__all__"
        extra_kwargs = {'club': {'required': False}}

class GetPlayerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    club = ClubSerializer(many=True, read_only=True)
    # current_club_inside = FootballClubSerializer()
    # video_clip = PlayerVideoClipSerializer(many=True, read_only=True)
    # carreer_history = PlayerCareerHistorySerializer(many=True, read_only=True)
    # player_acheivements = AcheivementsSerializer(many=True, read_only=True)
    # player_current_club_inside = FootballClubSerializer(many=True, read_only=True)
    # agent_inside = GetAgentInsideSerializer(many=True, read_only=True)
    # agent_outside = AgentOutsideSerializer(many=True, read_only=True)
    # reference_users_inside = GetReferenceSerializer(many=True, read_only=True)
    # reference_users_outside = ReferenceOutsideSerializer(many=True, read_only=True)

    class Meta:
        ordering = ['-id']
        model = Player
        fields = "__all__"
        extra_kwargs = {'club': {'required': False}}

class FootballTournamentsSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = FootballTournaments
        fields = ("id", "tournaments_name", "no_of_times", "coach_career_history_id","coach_id")
        extra_kwargs = {'coach_career_history_id': {'required': False}, 'coach_id': {'required': False}}
        
class GetFootballCoachEndorsementRequestSerializer(serializers.ModelSerializer):
    to_endorser = CustomUserSerializer()
    from_endorsee = CustomUserSerializer()

    class Meta:
        ordering = ['-id']
        model = FootballCoachEndorsementRequest
        fields = "__all__"
        
class FootballCoachEndorsementRequestSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = FootballCoachEndorsementRequest
        fields = "__all__"

class FootballCoachCareerHistorySerializer(serializers.ModelSerializer):
    endorsement_request = GetFootballCoachEndorsementRequestSerializer(many=True, read_only=True)

    class Meta:
        ordering = ['-id']
        model = FootballCoachCareerHistory
        fields = '__all__'
        extra_kwargs = {'coach_id': {'required': False}}
        
class CoachCareerHistorySerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = FootballCoachCareerHistory
        fields = '__all__'
        
class GetCoachEndorsementRequestSerializer(serializers.ModelSerializer):
    from_endorsee = CustomUserSerializer()
    coach_career_history = CoachCareerHistorySerializer()
    
    class Meta:
        model = FootballCoachEndorsementRequest
        fields = "__all__"
        
class CoachLicenseSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = CoachLicense
        fields = '__all__'
        extra_kwargs = {'coach': {'required': False}}

class FootballCoachSerializer(serializers.ModelSerializer):
    carreer_history = FootballCoachCareerHistorySerializer(many=True, read_only=True)
    # tournaments_name_won_as_coach = FootballTournamentsSerializer(many=True, read_only=True)
    # coach_acheivements = AcheivementsSerializer(many=True, read_only=True)
    my_license = CoachLicenseSerializer(many=True, read_only=True)
    # current_club_inside = FootballClubSerializer()

    class Meta:
        ordering = ['-id']
        model = FootballCoach
        fields = '__all__'
        extra_kwargs = {'carreer_history': {'required': False}, 'my_license': {'required': False}}

class GetFootballCoachSerializer(serializers.ModelSerializer):
    user= CustomUserSerializer()
    carreer_history = FootballCoachCareerHistorySerializer(many=True, read_only=True)
    # tournaments_name_won_as_coach = FootballTournamentsSerializer(many=True, read_only=True)
    # coach_acheivements = AcheivementsSerializer(many=True, read_only=True)
    my_license = CoachLicenseSerializer(many=True, read_only=True)
    # current_club_inside = FootballClubSerializer()

    class Meta:
        ordering = ['-id']
        model = FootballCoach
        fields = '__all__'
        extra_kwargs = {'carreer_history': {'required': False}, 'my_license': {'required': False}}

class ConnectUserSerializer(serializers.ModelSerializer):
    profile_image = ProfilePhotoSerializer(many=True, read_only=True)
    sport_profile_type = SportProfileTypeSerializer(many=True, read_only=True)
    # personal_achievements = PersonalAchievementsSerializer(many=True, read_only=True)
    permanent_address = AddressSerializer(many=True, read_only=True)
    present_address = AddressSerializer(many=True, read_only=True)
    video_clip = PlayerVideoClipSerializer(many=True, read_only=True)
    profile_description = ProfileDescriptionSerializer(many=True, read_only=True)
    player = PlayerSerializer(many=True, read_only=True)
    coach = FootballCoachSerializer(many=True, read_only=True)
    club = FootballClubSerializer(many=True, read_only=True)
    agent = AgentSerializer(many=True, read_only=True)
    # connected_users = NetworkConnectedSerializer(many=True, read_only=True)

    class Meta(object):
        model = CustomUser 
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'sport_profile_type' : {'required': False},
            'permanent_address' : {'required': False},
            'present_address' : {'required': False},
            'video_clip': {'required': False},
            'profile_desc': {'required': False},
            'player': {'required': False},
            'coach': {'required': False},
            'club': {'required': False},
            'agent': {'required': False},
        }

class NetworkConnectedSerializer(serializers.ModelSerializer):
    connect_to_user = ConnectUserSerializer()

    class Meta:
        ordering = ['-id']
        model = NetworkConnected
        fields = ("id", "connect_to_user", "status", "user_id", "network_request_id")
        extra_kwargs = {
            'user_id': {'required': False},
            'network_request_id': {'required': False},
        }

    # def create(self, validated_data):
    #     order_items_data = validated_data.pop('order_items')
    #     order = place_order.objects.create(**validated_data)
    #     for order_data in order_items_data:
    #         place_order_item.objects.create(order_item=order, **order_data)
    #     return order

# class NetworkConnectionsSerializer(serializers.ModelSerializer):
#     # connect_to_user = ConnectUserSerializer()

#     class Meta:
#         ordering = ['-id']
#         model = NetworkConnected
#         fields = ("id", "connect_to_user", "status", "user_id")
#         extra_kwargs = {'user_id': {'required': False}}

class UserSerializer(serializers.ModelSerializer):
    profile_image = ProfilePhotoSerializer(many=True, read_only=True)
    sport_profile_type = SportProfileTypeSerializer(many=True, read_only=True)
    # personal_achievements = PersonalAchievementsSerializer(many=True, read_only=True)
    permanent_address = AddressSerializer(many=True, read_only=True)
    present_address = AddressSerializer(many=True, read_only=True)
    video_clip = PlayerVideoClipSerializer(many=True, read_only=True)
    profile_description = ProfileDescriptionSerializer(many=True, read_only=True)
    player = PlayerSerializer(many=True, read_only=True)
    coach = FootballCoachSerializer(many=True, read_only=True)
    connected_users = NetworkConnectedSerializer(many=True, read_only=True)
    club = FootballClubSerializer(many=True, read_only=True)
    # reference_users_inside = ReferenceSerializer(many=True, read_only=True)
    # reference_users_outside = ReferenceOutsideSerializer(many=True, read_only=True)
    agent = AgentSerializer(many=True, read_only=True)
    # agent_outside = AgentOutsideSerializer(many=True, read_only=True)
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    age = serializers.SerializerMethodField()

    class Meta(object):
        model = CustomUser 
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'sport_profile_type' : {'required': False},
            'permanent_address' : {'required': False},
            'present_address' : {'required': False},
            'video_clip': {'required': False},
            'profile_desc': {'required': False},
            'player': {'required': False},
            'coach': {'required': False},
            'agent': {'required': False},
            'connected_users': {'required': False},
            'club': {'required': False},
            'age': {'required': False}
        }
        
    def get_age(self, obj):
        return obj.calculate_age()
        
    # Validating Password and Confirm Password while Registration
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs

    # def validate_password(self, data):
    #     validators.validate_password(password=data, user=CustomUser)
    #     return data
        
    def validate_password(self, value):
        try:
            validators.validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError({'password': exc.messages})
        return value

    # def create(self, validated_data):
    #     password = validated_data.pop('password', None)
    #     instance = self.Meta.model(**validated_data)
    #     if password is not None:
    #         instance.set_password(password)
    #     instance.save()
    #     return instance
    
    def create(self, validate_data):
        return CustomUser.objects.create_user(**validate_data)
    
class GetMyNetworkRequestSerializer(serializers.ModelSerializer):
    from_user = UserSerializer()

    class Meta:
        ordering = ['-id']
        model = MyNetworkRequest
        fields = ("id", "from_user", "to_user", "status")

class MyNetworkRequestSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = MyNetworkRequest
        fields = ("id", "from_user", "to_user", "status")

class GetVerifyRequestSerializer(serializers.ModelSerializer):
    from_user = UserSerializer()
    club_id = ClubSerializer()
    coach_club_id = FootballCoachCareerHistorySerializer()

    class Meta:
        ordering = ['-id']
        model = VerifyRequest
        fields = ("id", "from_user", "to_user", "status","profile_type","club_id","coach_club_id")
        extra_kwargs = {'club_id': {'required': False},'coach_club_id': {'required': False}}

class VerifyRequestSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = VerifyRequest
        fields = ("id", "from_user", "to_user", "status","profile_type","club_id","coach_club_id")
        extra_kwargs = {'club_id': {'required': False},'coach_club_id': {'required': False}}

class PostLikesSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = PostLikes
        fields = ("id", "user", "posted", "post_id")

class GetPostLikesSerializer(serializers.ModelSerializer):
    user=UserSerializer()

    class Meta:
        ordering = ['-id']
        model = PostLikes
        fields = ("id", "user", "posted", "post_id")

class PostCommentsSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = PostComments
        fields = ("id", "user", "comment", "posted", "post_id")

class GetPostCommentsSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = PostComments
        fields = ("id", "user", "comment", "posted", "post_id")
        ordering = ['-posted']
        lookup_field = 'post_id'

class PostItemSerializer(serializers.ModelSerializer):
    comments = GetPostCommentsSerializer(many=True, read_only=True)

    class Meta:
        ordering = ['-id']
        model = PostItem
        fields = ("id", "user", "picture", "description", "posted", "likes", "comments", "video_link", "type", "post_type")

class GetPostItemSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    comments = GetPostCommentsSerializer(many=True, read_only=True)
    likes = GetPostLikesSerializer(many=True, read_only=True)

    class Meta:
        ordering = ['-id']
        model = PostItem
        fields = ("id", "user", "picture", "description", "posted", "likes", "comments", "video_link", "type", "post_type")

class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = News
        fields = '__all__'

class GetNewsSerializer(serializers.ModelSerializer):
    user=CustomUserSerializer()

    class Meta:
        ordering = ['-id']
        model = News
        fields = '__all__'
        
class CreateInstituteProfileSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    new_password = serializers.CharField(required=True)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
class SportLicenseSerializer(serializers.ModelSerializer):
    class Meta:
        ordering = ['-id']
        model = SportLicense
        fields = ("id", "license_name")

        #added by Pijush
class OpportunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Opportunity
        fields = ['oppid', 'opportunity_type', 'description', 'valid_until','user']
        extra_kwargs = {'valid_until': {'required': False}}
class OpportunityApplicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpportunityApplications
        fields = ['opapplicationID', 'actedBy','saved','applied','appliedOn', 'comment','opportunityID']
        extra_kwargs = {'comment': {'required': False}}

class HelpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Help
        fields = ['helpid','typeOfHelp', 'description', 'createdBy']

class HelpSupportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpSupports
        fields = ['helpSupportID','helpID','helpProvidedBy', 'helpComments','helpProvidedBy']
        extra_kwargs = {'helpComments': {'required': False}}


class WellnessScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = WellnessScore
        fields = ['wellnessid','createdBy','mood','canManage','canHandlePressure','sleepHours', 'energyLevel', 'haveSupport', 'feelConnected', 'knowResourcesForSupport', 'needSupport', 'created_at', 'updated_at']

class ConditioningLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConditioningLog
        fields = '__all__'        
#end of added by Pijush 
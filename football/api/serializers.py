from rest_framework import serializers
from football.models import Address, CustomUser, Club, Player, ProfilePhoto, PlayerVideoClip, PlayerCareerHistory, SportProfileType, FootballCoachCareerHistory, FootballCoach, FootballTournaments, Acheivements,ProfileDescription, MyNetworkRequest, NetworkConnected, FootballClub, FootballClubHistory, FootballClubOfficeBearer, Reference, ReferenceOutside, Agent, AgentOutside, VerifyRequest, PostComments, PostItem, PostLikes, News
import django.contrib.auth.password_validation as validators
from django.core.exceptions import ValidationError

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

class SportProfileTypeSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = SportProfileType
        fields = ("id", "profile_type", "is_active", "user_id")
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
    profile_description = ProfileDescriptionSerializer(many=True, read_only=True)
    connected_users = NetworkConnectionsSerializer(many=True, read_only=True)

    class Meta(object):
        model = CustomUser 
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'sport_profile_type' : {'required': False},
            'profile_description' : {'required': False}
        }

class ClubSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = Club
        fields = ("id", "club_id", "club_name", "period", "games_played", "club_goals", "club_assists", "club_passes", "club_saved_goals", "interceptions_per_game", "takles_per_game", "shots_per_game", "key_passes_per_game", "dribles_completed_per_game", "clean_sheets_per_game", "club_yellow_card", "club_red_card", "players", "league","type", "status","remarks")
        extra_kwargs = {'players': {'required': False}}
    
class PlayerCareerHistorySerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = PlayerCareerHistory
        fields = ("id", "debut_date", "last_date", "league_name", "club_name", "player_id")
        extra_kwargs = {'player_id': {'required': False}}

class AcheivementsSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = Acheivements
        fields = ("id", "acheivement_name", "period", "player_id", "coach_id", "club_id")
        extra_kwargs = {'player_id': {'required': False}, 'coach_id': {'required': False}, 'club_id':  {'required': False}}

class FootballClubOfficeBearerSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = FootballClubOfficeBearer
        fields = ("id", "position", "name", "club_id")
        extra_kwargs = {'club_id': {'required': False}}

class FootballClubHistorySerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = FootballClubHistory
        fields = ("id", "period", "league_name", "games_played", "games_won", "games_lost", "games_tied", "points", "position", "club_id")
        extra_kwargs = {'club_id': {'required': False}}

class FootballClubSerializer(serializers.ModelSerializer):
    # user = ClubUserSerializer()
    office_bearer = FootballClubOfficeBearerSerializer(many=True, read_only=True)
    club_history = FootballClubHistorySerializer(many=True, read_only=True)
    club_acheivements = AcheivementsSerializer(many=True, read_only=True)
    # player_current_club_inside = PlayerSerializer(many=True, read_only=True)
    # coach_current_club_inside = FootballCoachSerializer(many=True, read_only=True)

    class Meta:
        ordering = ['-id']
        model = FootballClub
        fields = ("id", "user","office_bearer","club_history","club_acheivements")
        extra_kwargs = {'office_bearer': {'required': False}, 'club_history': {'required': False}, 'club_acheivements': {'required': False}}

class GetFootballClubSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    office_bearer = FootballClubOfficeBearerSerializer(many=True, read_only=True)
    club_history = FootballClubHistorySerializer(many=True, read_only=True)
    club_acheivements = AcheivementsSerializer(many=True, read_only=True)
    # player_current_club_inside = PlayerSerializer(many=True, read_only=True)
    # coach_current_club_inside = FootballCoachSerializer(many=True, read_only=True)

    class Meta:
        ordering = ['-id']
        model = FootballClub
        fields = ("id", "user","office_bearer","club_history","club_acheivements")
        extra_kwargs = {'office_bearer': {'required': False}, 'club_history': {'required': False}, 'club_acheivements': {'required': False}}

class AgentInsideSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = Agent
        fields = ("id", "user", "player_id")
        extra_kwargs = {'player_id': {'required': False}}

class GetAgentInsideSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        ordering = ['-id']
        model = Agent
        fields = ("id", "user", "player_id")
        extra_kwargs = {'player_id': {'required': False}}

class AgentOutsideSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = AgentOutside
        fields = ("id", "agent_name", "contact", "player_id")
        extra_kwargs = {'player_id': {'required': False}}

class GetReferenceSerializer(serializers.ModelSerializer):
    reffered_user = CustomUserSerializer()
    class Meta:
        ordering = ['-id']
        model = Reference
        fields = ("id", "reffered_user", "player_id")
        extra_kwargs = {'player_id': {'required': False}}

class ReferenceSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = Reference
        fields = ("id", "reffered_user", "player_id")
        extra_kwargs = {'player_id': {'required': False}}

class ReferenceOutsideSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = ReferenceOutside
        fields = ("id", "reference_name", "contact", "player_id")
        extra_kwargs = {'player_id': {'required': False}}

class PlayerSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    club = ClubSerializer(many=True, read_only=True)
    # current_club_inside = FootballClubSerializer()
    # video_clip = PlayerVideoClipSerializer(many=True, read_only=True)
    carreer_history = PlayerCareerHistorySerializer(many=True, read_only=True)
    player_acheivements = AcheivementsSerializer(many=True, read_only=True)
    # player_current_club_inside = FootballClubSerializer(many=True, read_only=True)
    agent_inside = GetAgentInsideSerializer(many=True, read_only=True)
    agent_outside = AgentOutsideSerializer(many=True, read_only=True)
    reference_users_inside = GetReferenceSerializer(many=True, read_only=True)
    reference_users_outside = ReferenceOutsideSerializer(many=True, read_only=True)

    class Meta:
        ordering = ['-id']
        model = Player
        fields = ("id", "user","primary_position","secondary_position","top_speed", "preferred_foot", "injury_history", "club", "carreer_history", "player_acheivements", "current_club_inside","current_club_inside_name","current_club_outside","agent_inside", "agent_outside", "reference_users_inside", "reference_users_outside")
        extra_kwargs = {'club': {'required': False}, 'carreer_history': {'required': False}, 'player_acheivements': {'required': False}, 'agent_inside': {'required': False}, 'reference_users_inside': {'required': False}, 'agent_outside': {'required': False}, 'reference_users_outside': {'required': False}}

class GetPlayerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    club = ClubSerializer(many=True, read_only=True)
    # current_club_inside = FootballClubSerializer()
    # video_clip = PlayerVideoClipSerializer(many=True, read_only=True)
    carreer_history = PlayerCareerHistorySerializer(many=True, read_only=True)
    player_acheivements = AcheivementsSerializer(many=True, read_only=True)
    # player_current_club_inside = FootballClubSerializer(many=True, read_only=True)
    agent_inside = GetAgentInsideSerializer(many=True, read_only=True)
    agent_outside = AgentOutsideSerializer(many=True, read_only=True)
    reference_users_inside = GetReferenceSerializer(many=True, read_only=True)
    reference_users_outside = ReferenceOutsideSerializer(many=True, read_only=True)

    class Meta:
        ordering = ['-id']
        model = Player
        fields = ("id", "user","primary_position","secondary_position","top_speed", "preferred_foot", "injury_history", "club", "carreer_history", "player_acheivements", "current_club_inside", "current_club_inside_name", "current_club_outside","agent_inside", "agent_outside", "reference_users_inside", "reference_users_outside")
        extra_kwargs = {'club': {'required': False}, 'carreer_history': {'required': False}, 'player_acheivements': {'required': False}, 'agent_inside': {'required': False}, 'reference_users_inside': {'required': False}, 'agent_outside': {'required': False}, 'reference_users_outside': {'required': False}}

class FootballTournamentsSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = FootballTournaments
        fields = ("id", "tournaments_name", "no_of_times", "coach_career_history_id","coach_id")
        extra_kwargs = {'coach_career_history_id': {'required': False}, 'coach_id': {'required': False}}

class FootballCoachCareerHistorySerializer(serializers.ModelSerializer):
    # tournaments_name_won_as_player = FootballTournamentsSerializer(many=True, read_only=True)

    class Meta:
        ordering = ['-id']
        model = FootballCoachCareerHistory
        fields = ("id", "period", "club_id", "club_name", "league", "playoffs_games_coached_in", "playoffs_games_won", "playoffs_games_lost", "total_no_tournaments_won_as_coach", "type", "status", "remarks", "coach_id")
        extra_kwargs = {'coach_id': {'required': False}}

class FootballCoachSerializer(serializers.ModelSerializer):
    carreer_history = FootballCoachCareerHistorySerializer(many=True, read_only=True)
    tournaments_name_won_as_coach = FootballTournamentsSerializer(many=True, read_only=True)
    coach_acheivements = AcheivementsSerializer(many=True, read_only=True)
    # coach_current_club_inside = FootballClubSerializer(many=True, read_only=True)
    # current_club_inside = FootballClubSerializer()

    class Meta:
        ordering = ['-id']
        model = FootballCoach
        fields = ("id", "user", "carreer_history", "from_date", "to_date", "playoffs_games_coached_in", "playoffs_games_won", "playoffs_games_lost", "total_no_tournaments_won_as_coach", "tournaments_name_won_as_coach", "current_team", "current_team_id", "coach_acheivements")
        extra_kwargs = {'carreer_history': {'required': False}, 'tournaments_name_won_as_coach': {'required': False}, 'coach_acheivements': {'required': False}}

class GetFootballCoachSerializer(serializers.ModelSerializer):
    user= CustomUserSerializer()
    carreer_history = FootballCoachCareerHistorySerializer(many=True, read_only=True)
    tournaments_name_won_as_coach = FootballTournamentsSerializer(many=True, read_only=True)
    coach_acheivements = AcheivementsSerializer(many=True, read_only=True)
    # coach_current_club_inside = FootballClubSerializer(many=True, read_only=True)
    # current_club_inside = FootballClubSerializer()

    class Meta:
        ordering = ['-id']
        model = FootballCoach
        fields = ("id", "user", "carreer_history", "from_date", "to_date", "playoffs_games_coached_in", "playoffs_games_won", "playoffs_games_lost", "total_no_tournaments_won_as_coach", "tournaments_name_won_as_coach", "current_team", "current_team_id", "coach_acheivements")
        extra_kwargs = {'carreer_history': {'required': False}, 'tournaments_name_won_as_coach': {'required': False}, 'coach_acheivements': {'required': False}}

class ConnectUserSerializer(serializers.ModelSerializer):
    profile_image = ProfilePhotoSerializer(many=True, read_only=True)
    sport_profile_type = SportProfileTypeSerializer(many=True, read_only=True)
    permanent_address = AddressSerializer(many=True, read_only=True)
    present_address = AddressSerializer(many=True, read_only=True)
    video_clip = PlayerVideoClipSerializer(many=True, read_only=True)
    profile_description = ProfileDescriptionSerializer(many=True, read_only=True)
    player = PlayerSerializer(many=True, read_only=True)
    coach = FootballCoachSerializer(many=True, read_only=True)
    club = FootballClubSerializer(many=True, read_only=True)
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
    # agent_inside = AgentInsideSerializer(many=True, read_only=True)
    # agent_outside = AgentOutsideSerializer(many=True, read_only=True)

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
            'connected_users': {'required': False},
            'club': {'required': False}
        }

    # def validate_password(self, data):
    #     validators.validate_password(password=data, user=CustomUser)
    #     return data
        
    def validate_password(self, value):
        try:
            validators.validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError({'password': exc.messages})
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
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
        fields = ("id", "user", "picture", "description", "posted", "likes", "comments", "video_link", "type")

class GetPostItemSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    comments = GetPostCommentsSerializer(many=True, read_only=True)
    likes = GetPostLikesSerializer(many=True, read_only=True)

    class Meta:
        ordering = ['-id']
        model = PostItem
        fields = ("id", "user", "picture", "description", "posted", "likes", "comments", "video_link", "type")

class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = News
        fields = ("id", "user", "posted", "title", "content", "picture", "start_date", "end_date")

class GetNewsSerializer(serializers.ModelSerializer):
    user=CustomUserSerializer()

    class Meta:
        ordering = ['-id']
        model = News
        fields = ("id", "user", "posted", "title", "content", "picture", "start_date", "end_date")

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
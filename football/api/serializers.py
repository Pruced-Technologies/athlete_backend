from rest_framework import serializers
from football.models import Address, CustomUser, Club, Player, ProfilePhoto, PlayerVideoClip, PlayerCareerHistory, SportProfileType, FootballCoachCareerHistory, FootballCoach, FootballTournaments, Acheivements,ProfileDescription

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
        fields = ("id", "title","description", "user_id")
        extra_kwargs = {'user_id': {'required': False}}

class ClubSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = Club
        fields = ("id", "club_name", "period", "games_played", "club_goals", "club_assists", "club_passes", "club_saved_goals", "interceptions_per_game", "takles_per_game", "shots_per_game", "key_passes_per_game", "dribles_completed_per_game", "clean_sheets_per_game", "club_yellow_card", "club_red_card", "players", "league","type")
        extra_kwargs = {'players': {'required': False}}

# class PlayerPositionSerializer(serializers.ModelSerializer):

#     class Meta:
#         ordering = ['-id']
#         model = PlayerPosition
#         fields = ("id", "player_position", "player_id")
#         extra_kwargs = {'player_id': {'required': False}}
    
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
        fields = ("id", "acheivement_name", "period", "player_id", "coach_id")
        extra_kwargs = {'player_id': {'required': False}, 'coach_id': {'required': False}}
        
class PlayerSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    club = ClubSerializer(many=True, read_only=True)
    # position = PlayerPositionSerializer(many=True, read_only=True)
    # video_clip = PlayerVideoClipSerializer(many=True, read_only=True)
    carreer_history = PlayerCareerHistorySerializer(many=True, read_only=True)
    player_acheivements = AcheivementsSerializer(many=True, read_only=True)

    class Meta:
        ordering = ['-id']
        model = Player
        fields = ("id", "user","primary_position","secondary_position","top_speed", "preferred_foot", "injury_history", "club", "carreer_history", "player_acheivements")
        extra_kwargs = {'club': {'required': False}, 'carreer_history': {'required': False}, 'player_acheivements': {'required': False}}

class FootballTournamentsSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = FootballTournaments
        fields = ("id", "tournaments_name", "no_of_times", "coach_career_history_id","coach_id")
        extra_kwargs = {'coach_career_history_id': {'required': False}, 'coach_id': {'required': False}}

class FootballCoachCareerHistorySerializer(serializers.ModelSerializer):
    tournaments_name_won_as_player = FootballTournamentsSerializer(many=True, read_only=True)

    class Meta:
        ordering = ['-id']
        model = FootballCoachCareerHistory
        fields = ("id", "period", "games_played_as_player", "games_won_as_player", "games_lost_as_player", "games_tied_as_player", "playoffs_games_played_as_player", "total_no_tournaments_won_as_player", "tournaments_name_won_as_player", "coach_id")
        extra_kwargs = {'tournaments_name_won_as_player': {'required': False}, 'coach_id': {'required': False}}

class FootballCoachSerializer(serializers.ModelSerializer):
    carreer_history = FootballCoachCareerHistorySerializer(many=True, read_only=True)
    tournaments_name_won_as_coach = FootballTournamentsSerializer(many=True, read_only=True)
    coach_acheivements = AcheivementsSerializer(many=True, read_only=True)

    class Meta:
        ordering = ['-id']
        model = FootballCoach
        fields = ("id", "user", "carreer_history", "from_date", "to_date", "playoffs_games_coached_in", "playoffs_games_won", "playoffs_games_lost", "total_no_tournaments_won_as_coach", "tournaments_name_won_as_coach", "current_team", "coach_acheivements")
        extra_kwargs = {'carreer_history': {'required': False}, 'tournaments_name_won_as_coach': {'required': False}, 'coach_acheivements': {'required': False}}

class UserSerializer(serializers.ModelSerializer):
    profile_image = ProfilePhotoSerializer(many=True, read_only=True)
    sport_profile_type = SportProfileTypeSerializer(many=True, read_only=True)
    permanent_address = AddressSerializer(many=True, read_only=True)
    present_address = AddressSerializer(many=True, read_only=True)
    video_clip = PlayerVideoClipSerializer(many=True, read_only=True)
    profile_description = ProfileDescriptionSerializer(many=True, read_only=True)
    player = PlayerSerializer(many=True, read_only=True)
    coach = FootballCoachSerializer(many=True, read_only=True)

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
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
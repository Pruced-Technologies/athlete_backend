from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from datetime import date
from .manager import UserManager
# from django.contrib.auth import get_user_model
# User = get_user_model()

# Create your models here.

class Type(models.Model):
    id = models.AutoField(primary_key=True)
    sport_type = models.CharField(max_length=50)
    player_type = models.CharField(max_length=50,unique=True)

class CustomUser(AbstractUser):
    username = models.CharField(max_length=50,null=True,blank=True)
    # username = None
    email = models.EmailField(unique=True)
    sport_type = models.CharField(max_length=50,null=True,blank=True)
    # sport_profile_type = models.ManyToManyField(SportProfileType, blank=True)
    height = models.IntegerField(null=True,blank=True)
    weight = models.IntegerField(null=True,blank=True)
    contact_no = models.CharField(max_length=12,unique=True)
    # present_address = models.ForeignKey(Address, on_delete=models.CASCADE,related_name='present_address',null=True,blank=True)
    # permanent_address = models.ForeignKey(Address, on_delete=models.CASCADE,related_name='permanent_address',null=True,blank=True)
    dob = models.DateField(null=True,blank=True)
    bio = models.TextField(null=True,blank=True)
    profile_photo = models.ImageField(upload_to="profile",null=True,blank=True)
    profile_photo_url = models.TextField(blank=True,null=True)
    citizenship = models.CharField(max_length=100,blank=True,null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['contact_no']

class SportProfileType(models.Model):
    id = models.AutoField(primary_key=True)
    profile_type = models.CharField(max_length=50)
    is_active = models.BooleanField(
        ("active"),
        default=True,
        help_text=(
            "Designates whether this address should be treated as active. "
            "Unselect this instead of deleting address."
        ),
    )
    user_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='sport_profile_type', blank=True, null=True)

class ProfileDescription(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100,null=True,blank=True)
    description = models.TextField(null=True, blank=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='profile_description', blank=True, null=True)

    def __str__(self):
        return self.title

class ProfilePhoto(models.Model):
    id = models.AutoField(primary_key=True)
    photo = models.ImageField(upload_to="profile",null=True,blank=True)
    user_id = models.ManyToManyField(CustomUser, related_name='profile_image', blank=True)

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    address_lane = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    pin = models.IntegerField()
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address_type = models.CharField(max_length=50)
    is_active = models.BooleanField(
        ("active"),
        default=True,
        help_text=(
            "Designates whether this address should be treated as active. "
            "Unselect this instead of deleting address."
        ),
    )
    permanent_user_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='permanent_address', blank=True, null=True)
    present_user_id = models.ManyToManyField(CustomUser, related_name='present_address', blank=True)

    def __str__(self):
        return self.address_lane
    
class FootballClub(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='club', null=True, blank=True)
    founded_in = models.DateField(null=True,blank=True)
    # player_id = models.ManyToManyField(Player, related_name='player_current_club_inside', blank=True)
    # coach_id = models.ManyToManyField(FootballCoach, related_name='coach_current_club_inside', blank=True)

    def __str__(self):
        # return self.user.email
        return "%s %s" % (self.user.email, self.founded_in)
    
class Player(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='player', blank=True, null=True)
    primary_position = models.CharField(max_length=25,blank=True,null=True)
    secondary_position = models.CharField(max_length=25,blank=True,null=True)
    top_speed = models.IntegerField(blank=True,null=True)
    preferred_foot = models.CharField(max_length=10,blank=True,null=True)
    injury_history = models.TextField(null=True,blank=True)
    current_club_outside = models.TextField(null=True, blank=True)
    current_club_inside = models.IntegerField(null=True, blank=True)
    current_club_inside_name = models.TextField(null=True, blank=True)
    # current_club_inside = models.ForeignKey(FootballClub, on_delete=models.CASCADE, related_name='player_club', null=True, blank=True)
    # agent_inside = models.ManyToManyField(Agent, related_name='agent_info_inside', blank=True)
    # reference_inside = models.ManyToManyField(Reference, related_name='reference_info_inside', blank=True)
    # agent_outside = models.ManyToManyField(AgentOutside, related_name='agent_info_outside', blank=True)
    # video_url = models.CharField(max_length=255)
    # league = models.CharField(max_length=200,null=True,blank=True)
    # personal_acheivements = models.ManyToManyField(PlayerAcheivements, blank=True)

    def __str__(self):
        return self.user.email

class PlayerVideoClip(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100,null=True,blank=True)
    profile_type = models.CharField(max_length=50,null=True,blank=True)
    clip_url = models.TextField(null=True, blank=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='video_clip', blank=True, null=True)

    def __str__(self):
        return self.title

class PlayerCareerHistory(models.Model):
    id = models.AutoField(primary_key=True)
    debut_date = models.DateField()
    last_date = models.DateField(null=True, blank=True)
    league_name = models.CharField(max_length=255)
    club_name = models.CharField(max_length=255)
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE,related_name='carreer_history', blank=True, null=True)
    
class Club(models.Model):
    id = models.AutoField(primary_key=True)
    club_id = models.IntegerField(null=True,blank=True)
    club_name = models.CharField(max_length=255)
    period = models.CharField(max_length=25,null=True,blank=True)
    games_played = models.IntegerField(null=True,blank=True)
    club_goals = models.IntegerField(null=True,blank=True)
    club_assists = models.IntegerField(null=True,blank=True)
    club_passes = models.IntegerField(null=True,blank=True)
    club_saved_goals = models.IntegerField(null=True,blank=True)
    interceptions_per_game = models.FloatField(null=True,blank=True)
    takles_per_game = models.FloatField(null=True,blank=True)
    shots_per_game = models.FloatField(null=True,blank=True)
    key_passes_per_game = models.FloatField(null=True,blank=True)
    dribles_completed_per_game = models.FloatField(null=True,blank=True)
    clean_sheets_per_game = models.FloatField(null=True,blank=True)
    club_yellow_card = models.IntegerField(null=True,blank=True)
    club_red_card = models.IntegerField(null=True,blank=True)
    # rating = models.FloatField(null=True,blank=True)
    players = models.ForeignKey(Player, on_delete=models.CASCADE,related_name='club', blank=True, null=True)
    league = models.CharField(max_length=200,null=True,blank=True)
    type = models.CharField(max_length=50,null=True,blank=True)
    status = models.CharField(max_length=50,null=True,blank=True)
    remarks = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.club_name
    
class FootballCoach(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='coach', blank= True, null= True)
    # player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='coach', blank= True, null= True)
    # carreer_history = models.ForeignKey(FootballCoachCareerHistory, on_delete=models.PROTECT, related_name='coach_history', blank= True, null= True)
    from_date = models.IntegerField(null=True, blank=True)
    to_date = models.IntegerField(null=True, blank=True)
    playoffs_games_coached_in = models.IntegerField(null=True, blank=True)
    playoffs_games_won = models.IntegerField(null=True, blank=True)
    playoffs_games_lost = models.IntegerField(null=True, blank=True)
    total_no_tournaments_won_as_coach = models.IntegerField(null=True, blank=True)
    # tournaments_name_won_as_coach = models.ManyToManyField(FootballTournaments, related_name='tournament_name_coach', blank=True)
    current_team = models.CharField(max_length=255,null=True, blank=True)
    current_team_id = models.IntegerField(null=True, blank=True)
    # current_club_inside = models.ForeignKey(FootballClub, on_delete=models.CASCADE, related_name='coach_club', null=True, blank=True)
    # acheivements = models.ManyToManyField(Acheivements, blank=True)

    def __str__(self):
        return self.user.email
    
class FootballCoachCareerHistory(models.Model):
    id = models.AutoField(primary_key=True)
    period = models.CharField(max_length=25,null=True, blank=True)
    club_id = models.IntegerField(null=True, blank=True)
    club_name = models.CharField(max_length=25,null=True, blank=True)
    league = models.CharField(max_length=25,null=True, blank=True)
    playoffs_games_coached_in = models.IntegerField(null=True, blank=True)
    playoffs_games_won = models.IntegerField(null=True, blank=True)
    playoffs_games_lost = models.IntegerField(null=True, blank=True)
    total_no_tournaments_won_as_coach = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=50,null=True,blank=True)
    status = models.CharField(max_length=50,null=True,blank=True)
    remarks = models.TextField(null=True,blank=True)
    coach_id = models.ForeignKey(FootballCoach, on_delete=models.CASCADE, related_name='carreer_history', blank= True, null= True)

    def __str__(self):
        # return self.club_name
        return "%s %s %s" % (self.club_name, self.period, self.league)
    
class FootballTournaments(models.Model):
    id = models.AutoField(primary_key=True)
    tournaments_name = models.CharField(max_length=255,null=True,blank=True)
    no_of_times = models.IntegerField(null=True,blank=True)
    coach_career_history_id = models.ForeignKey(FootballCoachCareerHistory, on_delete=models.CASCADE,related_name='tournaments_name_won_as_player', blank=True, null=True)
    coach_id = models.ForeignKey(FootballCoach, on_delete=models.CASCADE, related_name='tournaments_name_won_as_coach', blank=True, null=True)

    def __str__(self):
        return self.tournaments_name

class FootballClubHistory(models.Model):
    id = models.AutoField(primary_key=True)
    period = models.CharField(max_length=25,null=True, blank=True)
    league_name = models.CharField(max_length=255,null=True, blank=True)
    games_played = models.IntegerField(null=True, blank=True)
    games_won = models.IntegerField(null=True, blank=True)
    games_lost = models.IntegerField(null=True, blank=True)
    games_tied = models.IntegerField(null=True, blank=True)
    points = models.IntegerField(null=True, blank=True)
    position = models.CharField(max_length=100,null=True, blank=True)
    club_id = models.ForeignKey(FootballClub, on_delete=models.CASCADE, related_name='club_history',null=True, blank=True)

    def __str__(self):
        # return self.acheivement_name
        return "%s %s" % (self.league_name, self.period)
    

class FootballClubOfficeBearer(models.Model):
    id = models.AutoField(primary_key=True)
    position = models.CharField(max_length=100,null=True, blank=True)
    name = models.CharField(max_length=255,null=True, blank=True)
    club_id = models.ForeignKey(FootballClub, on_delete=models.CASCADE, related_name='office_bearer',null=True, blank=True)

    def __str__(self):
        return "%s %s" % (self.name, self.position)

class Acheivements(models.Model):
    id = models.AutoField(primary_key=True)
    acheivement_name = models.CharField(max_length=255,null=True, blank=True)
    period = models.CharField(max_length=25,null=True, blank=True)
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_acheivements', blank=True, null=True)
    coach_id = models.ForeignKey(FootballCoach, on_delete=models.CASCADE, related_name='coach_acheivements', blank=True, null=True)

    def __str__(self):
        # return self.acheivement_name
        return "%s %s" % (self.acheivement_name, self.period)
    
class MyNetworkRequest(models.Model):
    id = models.AutoField(primary_key=True)
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    # from_user = models.IntegerField(null=True,blank=True)
    to_user = models.IntegerField(null=True,blank=True)
    status = models.CharField(max_length=100,null=True,blank=True)
    # user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='my_network')

    def __str__(self):
        # return self.to_user
        return "%s %s %s" % (self.from_user.username, self.to_user, self.status)
    
class NetworkConnected(models.Model):
    id = models.AutoField(primary_key=True)
    connect_to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    # connect_to_user2 = models.IntegerField(null=True,blank=True)
    status = models.CharField(max_length=100,null=True,blank=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='connected_users', null=True, blank=True)

    def __str__(self):
        return "%s %s" % (self.connect_to_user.username, self.status)
    
class Reference(models.Model):
    id = models.AutoField(primary_key=True)
    reffered_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='reference_users_inside', null=True, blank=True)

    def __str__(self):
        return self.reffered_user.email
    
class ReferenceOutside(models.Model):
    id = models.AutoField(primary_key=True)
    reference_name = models.CharField(max_length=100,null=True,blank=True)
    contact = models.CharField(max_length=12,null=True,blank=True)
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='reference_users_outside', null=True, blank=True)

    def __str__(self):
        return self.reference_name
    
class Agent(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='agent_inside', null=True, blank=True)

    def __str__(self):
        return self.user.email
    
class AgentOutside(models.Model):
    id = models.AutoField(primary_key=True)
    agent_name = models.CharField(max_length=100,null=True,blank=True)
    contact = models.CharField(max_length=12,null=True,blank=True)
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='agent_outside', null=True, blank=True)

    def __str__(self):
        return self.agent_name


class VerifyRequest(models.Model):
    id = models.AutoField(primary_key=True)
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    to_user = models.IntegerField(null=True,blank=True)
    status = models.CharField(max_length=100,null=True,blank=True)
    profile_type = models.CharField(max_length=100,null=True,blank=True)
    club_id = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True)
    coach_club_id = models.ForeignKey(FootballCoachCareerHistory, on_delete=models.CASCADE, null=True, blank=True)
    # user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='my_network')

    def __str__(self):
        # return self.to_user
        return "%s %s %s" % (self.from_user.username, self.to_user, self.status)
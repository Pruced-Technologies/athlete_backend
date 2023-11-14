from django.contrib import admin
from . models import Type, SportProfileType, CustomUser, Address, Club, Player, ProfilePhoto, PlayerVideoClip, PlayerCareerHistory, FootballTournaments,FootballCoach,FootballCoachCareerHistory, Acheivements, FootballClub, FootballClubHistory, FootballClubOfficeBearer,ProfileDescription,MyNetworkRequest, NetworkConnected, Reference, ReferenceOutside, Agent, AgentOutside, VerifyRequest

# Register your models here.

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ("id", "sport_type","player_type")

@admin.register(SportProfileType)
class SportProfileTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "profile_type","is_active")

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "address_lane","landmark","city","pin","state","country","address_type","is_active")

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "password", "first_name", "last_name", "sport_type")

@admin.register(ProfileDescription)
class ProfileDescriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description")

@admin.register(ProfilePhoto)
class ProfilePhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "photo")

@admin.register(Acheivements)
class PlayerAcheivementsAdmin(admin.ModelAdmin):
    list_display = ("id", "acheivement_name","period")

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("id", "user","top_speed","preferred_foot","injury_history")

@admin.register(PlayerVideoClip)
class PlayerVideoClipAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "profile_type", "clip_url")

# @admin.register(PlayerPosition)
# class PlayerPositionAdmin(admin.ModelAdmin):
#     list_display = ("id", "player_position")

@admin.register(PlayerCareerHistory)
class PlayerCareerHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "debut_date","last_date","league_name","club_name")

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ("id", "club_name","games_played","club_goals","club_assists","type","status")

@admin.register(FootballTournaments)
class FootballTournamentsAdmin(admin.ModelAdmin):
    list_display = ("id", "tournaments_name")

@admin.register(FootballCoachCareerHistory)
class FootballCoachCareerHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "period", "club_id", "club_name", "league", "playoffs_games_coached_in", "playoffs_games_won", "playoffs_games_lost", "total_no_tournaments_won_as_coach", "type", "status")

@admin.register(FootballCoach)
class FootballCoachAdmin(admin.ModelAdmin):
    list_display = ("id", "user","from_date","to_date","playoffs_games_coached_in","playoffs_games_won","playoffs_games_lost","current_team")

@admin.register(FootballClub)
class FootballClubAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "founded_in")

@admin.register(FootballClubHistory)
class FootballClubHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "period", "league_name", "games_played", "games_won", "games_lost", "games_tied", "points", "position")

@admin.register(FootballClubOfficeBearer)
class FootballClubOfficeBearerAdmin(admin.ModelAdmin):
    list_display = ("id", "position", "name")

@admin.register(MyNetworkRequest)
class MyNetworkRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "from_user", "to_user", "status")

@admin.register(NetworkConnected)
class NetworkConnectedAdmin(admin.ModelAdmin):
    list_display = ("id", "connect_to_user", "status")

@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ("id", "reffered_user")

@admin.register(ReferenceOutside)
class ReferenceOutsideAdmin(admin.ModelAdmin):
    list_display = ("id", "reference_name", "contact")

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ("id", "user")

@admin.register(AgentOutside)
class AgentOutsideAdmin(admin.ModelAdmin):
    list_display = ("id", "agent_name", "contact")

@admin.register(VerifyRequest)
class VerifyRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "from_user", "to_user", "status")
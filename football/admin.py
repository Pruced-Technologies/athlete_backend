from django.contrib import admin
from . models import *

# Register your models here.

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ("id", "sport_type")

@admin.register(SportProfileType)
class SportProfileTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "profile_type", "status", "is_active", "user_id")

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

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("id", "user","top_speed","preferred_foot")

@admin.register(PlayerVideoClip)
class PlayerVideoClipAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "profile_type", "clip_url")

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ("id", "club_name","games_played","club_goals","club_assists","league_type","status")

@admin.register(FootballTournaments)
class FootballTournamentsAdmin(admin.ModelAdmin):
    list_display = ("id", "tournaments_name")

@admin.register(FootballCoachCareerHistory)
class FootballCoachCareerHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "league_type", "club_name", "league_name", "status")

@admin.register(FootballCoach)
class FootballCoachAdmin(admin.ModelAdmin):
    list_display = ("id", "user")

@admin.register(FootballClub)
class FootballClubAdmin(admin.ModelAdmin):
    list_display = ("id", "user")

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
    list_display = ("id", "connect_to_user", "status", "user_id", "network_request_id")

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ("id", "user")


@admin.register(VerifyRequest)
class VerifyRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "from_user", "to_user", "status")

@admin.register(PostComments)
class PostCommentsAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "comment", "posted")

@admin.register(PostLikes)
class PostLikesAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "posted")

@admin.register(PostItem)
class PostItemAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "picture", "description", "posted", "likes", "video_link")

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "posted", "title", "content")
    
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", "country_name")
    
@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ("id", "sport_type", "league_name", "league_type")
    
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("id", "club_name", "reg_id", "country_name", "sport_type")
    
@admin.register(SportLicense)
class SportLicenseAdmin(admin.ModelAdmin):
    list_display = ("id", "license_name")
    
@admin.register(AgentCareerHistory)
class AgentCareerHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "contact_no", "email", "address_lane", "zip", "state", "country", "achievements")
    
@admin.register(FootballPlayersAndCoachesUnderMe)
class FootballPlayersAndCoachesUnderMeAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "name")
    
@admin.register(FootballAgentEndorsementRequest)
class FootballAgentEndorsementRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "to_endorser_email", "to_endorser", "from_endorsee", "type", "status")
    
@admin.register(FootballPlayerEndorsementRequest)
class FootballPlayerEndorsementRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "to_endorser_email", "to_endorser", "from_endorsee", "type", "status")
    
@admin.register(FootballCoachEndorsementRequest)
class FootballCoachEndorsementRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "to_endorser_email", "to_endorser", "from_endorsee", "type", "status")
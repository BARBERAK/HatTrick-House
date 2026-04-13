from django.contrib import admin
from .models import Game

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('league', 'home_team', 'away_team', 'game_date')
    
    list_filter = ('league', 'sport_key')
    
    search_fields = ('home_team', 'away_team')
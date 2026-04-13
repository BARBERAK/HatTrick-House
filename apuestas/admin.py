from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Game, UserProfile

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('league', 'home_team', 'away_team', 'game_date')
    
    list_filter = ('league', 'sport_key')
    
    search_fields = ('home_team', 'away_team')
    
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Información Extra (Perfil)'
    
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_money')
    
    def get_money(self, instance):
        try:
            return f"{instance.userprofile.money}"
        except:
            return "0.00€"
        
    #le cambiamos el nombre para entenderlo mejor:
    get_money.short_description = "Saldo Disponible"
    
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
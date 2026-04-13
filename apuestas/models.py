from django.db import models

class Game(models.Model):
    # usamos como ID el que nos proporciona la propia API.
    game_id = models.CharField(primary_key=True, max_length=100, unique=True)
    
    #el tipo de evento que guardamos y en que liga compite:
    sport_key = models.CharField(max_length=50, default="soccer")
    league = models.CharField(max_length=100)
    
    #los dos equipos relacionados a ese partido:
    home_team = models.CharField(max_length=50)
    away_team = models.CharField(max_length=50)
    
    #las apuestas relacionadas a ese partido:
    home_price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    away_price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    draw_price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, null=True, blank=True)
    
    #la date de ese partido: 
    game_date = models.DateTimeField()
    
    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"

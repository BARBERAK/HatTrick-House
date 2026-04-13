import requests
import json
import pytz

from datetime import datetime
from .models import Game


URL_LA_LIGA = "https://api.the-odds-api.com/v4/sports/soccer_spain_la_liga/odds"
URL_PREMIER_LEAGUE = "https://api.the-odds-api.com/v4/sports/soccer_epl/odds"
URL_CHAMPIONS_LEAGUE = "https://api.the-odds-api.com/v4/sports/soccer_uefa_champs_league/odds"
NBA = "https://api.the-odds-api.com/v4/sports/basketball_nba/odds"

PROVA1 = "test_bd/api_output_data.json"
PROVA2 = "test_bd/api_output_data_nba.json"

dict_leagues = {
        "la_liga" : URL_LA_LIGA,
        "champions_league" : URL_CHAMPIONS_LEAGUE,
        "premier_league" : URL_PREMIER_LEAGUE,
        "nba" : NBA
    }

dict_proba = {
    "la_liga" : PROVA1,
    "nba" : PROVA2
}

def fetch_data(url_league=URL_LA_LIGA):
    # parametros para acceder a la API:
    parms = {
        "apiKey" : "6a4aaab34aee9c66694cadfd83b395d2",
        "regions" : "eu",
        "markets" : "h2h",
        "oddsFormat" : "decimal"
    }
    response = requests.get(url_league, params=parms)
    if response.status_code == 200:
        return response.json()
    else:
        # TO DO:
        # controlar error
        return None

def fetch_data_debug(url_league):
    with open(url_league, 'r', encoding='utf-8') as archivo:
        data = json.load(archivo)
    return data

def convert_timezone(game_date):
    utc_time = datetime.strptime(game_date[11:-1], "%H:%M:%S")
    utc = pytz.utc
    spain = pytz.timezone("Europe/Madrid")

    utc_time = utc.localize(utc_time)
    spain_time = utc_time.astimezone(spain)

    return spain_time.time()



def clean_data_league(data):
    games_list = []
    
    for simple_data in data:
        game_id = simple_data["id"]
        
        #guardaremos tambien datos de la liga que es y el deporte.
        sport = simple_data["sport_key"][:6] #soccer
        league = simple_data["sport_title"] #La Liga - Spain
        
        #recibimos de la API un formato diferente al de europa/madrid. Es por eso que lo adaptamos a nuestro horario.
        commence_time = simple_data["commence_time"]
        spain_time = convert_timezone(commence_time)
        
        #en game_date guardamos tanto la fecha como la hora. Lo separamos con el caracter &
        game_date = commence_time[:10] + " " + str(spain_time)
        home_team = simple_data["home_team"]
        away_team = simple_data["away_team"]
        info_bookmakers = simple_data["bookmakers"][0]["markets"][0]
        away_price = None
        home_price = None
        draw_price = None
        
        for outcome in info_bookmakers["outcomes"]:
            if outcome["name"] == home_team:
                home_price = outcome["price"]
            elif outcome["name"] == away_team:
                away_price = outcome["price"]
            elif outcome["name"] == "Draw":
                draw_price = outcome["price"]
    
        game_dict = {
            "game_id" : game_id,
            "sport_key" : sport,
            "league" : league,
            "game_date" : game_date,
            "home_team" : home_team,
            "away_team" : away_team,
            "away_price" : away_price,
            "home_price" : home_price,
            "draw_price" : draw_price
        }
        games_list.append(game_dict)
    
    return games_list
    


def save_to_db(games_list):
    for game in games_list:
        try:
            obj, created = Game.objects.update_or_create(
                game_id = game["game_id"],
                defaults={
                    "sport_key" : game["sport_key"],
                    "league" : game["league"],
                    "game_date" : game["game_date"],
                    "home_team" : game["home_team"],
                    "away_team" : game["away_team"],
                    "away_price" : game["away_price"],
                    "home_price" : game["home_price"],
                    "draw_price" : game["draw_price"],
                }
            )
        except Exception as e:
            print(f"ERROR al guardar el partido {game.get('game_id')}: {e}")

    
    
def execute_update_api():
    games_list = []
    for value in dict_proba.values():
        data = fetch_data_debug(value)
        if data:
            games_list.extend(clean_data_league(data))
        else:
            print(f"Advertencia: No se obtuvieron datos para la url {value}")
        
    #enviamos los datos limpios a la bd
    save_to_db(games_list)

    return True

    
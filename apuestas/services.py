import requests
import json
import pytz

from datetime import datetime
from .models import Game


URL_LA_LIGA = "https://api.the-odds-api.com/v4/sports/soccer_spain_la_liga/odds"
URL_PREMIER_LEAGUE = "https://api.the-odds-api.com/v4/sports/soccer_epl/odds"
URL_CHAMPIONS_LEAGUE = "https://api.the-odds-api.com/v4/sports/soccer_uefa_champs_league/odds"

PROVA1 = "test_bd/prova1.json"

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

def fetch_data_debug():
    PROVA2 = "test_bd/api_output_data.json"
    with open(PROVA2, 'r', encoding='utf-8') as archivo:
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
        away_price = info_bookmakers["outcomes"][0]["price"]
        home_price = info_bookmakers["outcomes"][1]["price"]
        draw_price = info_bookmakers["outcomes"][2]["price"]
    
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
    #simple informacion para el admin:
    count_data_saved = 0
    count_data_updated = 0
    
    for game in games_list:
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
        if created:
            count_data_saved += 1
        else:
            count_data_updated += 1

    print(f"Datos guardados: {count_data_saved}")
    print(f"Datos actualizados: {count_data_updated}")

    
    
def execute_update_api():
    data = fetch_data_debug()
    
    games_list = clean_data_league(data)
    
    #enviamos los datos limpios a la bd
    save_to_db(games_list)

    return True

    
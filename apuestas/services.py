import requests
import json
from datetime import datetime
import pytz

URL_LA_LIGA = "https://api.the-odds-api.com/v4/sports/soccer_spain_la_liga/odds"
URL_PREMIER_LEAGUE = "https://api.the-odds-api.com/v4/sports/soccer_epl/odds"
URL_CHAMPIONS_LEAGUE = "https://api.the-odds-api.com/v4/sports/soccer_uefa_champs_league/odds"

PROVA1 = "test_bd/prova1.json"
PROVA2 = "test_bd/api_output_data.json"

# parametros para acceder a la API:
parms = {
    "apiKey" : "6a4aaab34aee9c66694cadfd83b395d2",
    "regions" : "eu",
    "markets" : "h2h",
    "oddsFormat" : "decimal"
}

def convert_timezone(game_date):
    utc_time = datetime.strptime(game_date[11:-1], "%H:%M:%S")
    utc = pytz.utc
    spain = pytz.timezone("Europe/Madrid")

    utc_time = utc.localize(utc_time)
    spain_time = utc_time.astimezone(spain)

    return spain_time.time()


def clean_data_spanish_league(data):
    games_list = []
    
    for simple_data in data:
        game_id = simple_data["id"]
        
        #recibimos de la API un formato diferente al de europa/madrid. Es por eso que lo adaptamos a nuestro horario.
        commence_time = simple_data["commence_time"]
        spain_time = convert_timezone(commence_time)
        
        #en game_date guardamos tanto la fecha como la hora. Lo separamos con el caracter &
        game_date = commence_time[:10] + "&" + str(spain_time)
        home_team = simple_data["home_team"]
        away_team = simple_data["away_team"]
        info_bookmakers = simple_data["bookmakers"][0]["markets"][0]
        away_price = info_bookmakers["outcomes"][0]["price"]
        home_price = info_bookmakers["outcomes"][1]["price"]
        draw_price = info_bookmakers["outcomes"][2]["price"]
    
        game_dict = {
            "game_id" : game_id,
            "game_date" : game_date,
            "home_team" : home_team,
            "away_team" : away_team,
            "away_price" : away_price,
            "home_price" : home_price,
            "draw_price" : draw_price
        }
        games_list.append(game_dict)
    
    return games_list

    
#response = requests.get(URL_LA_LIGA, params=parms)
# if response.status_code == 200:
#     partidos_brutos = response.json()
#     print(partidos_brutos)
# else:
#     print("error code: " , response.status_code.__str__)

with open(PROVA2, 'r', encoding='utf-8') as archivo:
    data = json.load(archivo)
    
spanish_games_list = clean_data_spanish_league(data)

# TO DO:
# ahora tenemos guardados todos los partidos que la api nos devuelve. 
# Toca guardarlos en nuestra propia BD.
    
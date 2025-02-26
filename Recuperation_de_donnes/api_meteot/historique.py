import requests
from datetime import datetime, timedelta
import pandas as pd


from config import api_key, location
from utils import fetch_data

BASE_URL = 'https://api.weatherapi.com/v1/history.json'
def get_weather_data(api_key, location, start_date, end_date):
    current_date = start_date
    all_data = []

    while current_date <= end_date:
        formatted_date = current_date.strftime('%Y-%m-%d')
        params = {
            'key': api_key,
            'q': location,
            'dt': formatted_date,
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if 'forecast' in data and 'forecastday' in data['forecast']:
            for hour_data in data['forecast']['forecastday'][0]['hour']:
                filtered_data = {
                    'time': hour_data['time'],
                    'temp_c': hour_data['temp_c'],
                    'condition': hour_data['condition']['text'],
                    'wind_kph': hour_data['wind_kph'],
                    'wind_dir': hour_data['wind_dir'],
                    'pressure_mb': hour_data['pressure_mb'],
                    'precip_mm': hour_data['precip_mm'],
                    # 'snow_cm': hour_data.get('snow_cm', 0),  # Peut ne pas être disponible, mettre à 0 par défaut
                    'humidity': hour_data['humidity'],
                    'cloud': hour_data['cloud'],
                    'feelslike_c': hour_data['feelslike_c'],
                    'windchill_c': hour_data['windchill_c'],
                    'heatindex_c': hour_data['heatindex_c'],
                    'dewpoint_c': hour_data['dewpoint_c'],
                    # 'will_it_rain': hour_data['will_it_rain'],
                    # 'chance_of_rain': hour_data['chance_of_rain'],
                    # 'will_it_snow': hour_data['will_it_snow'],
                    # 'chance_of_snow': hour_data['chance_of_snow'],
                    'gust_kph': hour_data['gust_kph'],
                    'uv': hour_data['uv'],
                }
                all_data.append(filtered_data)

        current_date += timedelta(days=1)

    return all_data


# Définir les paramètres
location = 'Nice'
end_date = datetime.now()
start_date = end_date - timedelta(days=7)

# Récupérer les données
weather_data = get_weather_data(api_key, location, start_date, end_date)

# Convertir en DataFrame et enregistrer dans un CSV
df = pd.DataFrame(weather_data)
df.to_csv('historical_weather_data.csv', index=False)

print("Données historiques enregistrées dans 'historical_weather_data.csv'.")

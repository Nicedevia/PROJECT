import requests
import datetime
import csv
import time
import os
import pandas as pd
from config import api_key, location
from utils import fetch_data

base_url = 'http://api.weatherapi.com/v1'


def get_weather_data(url):
    response = requests.get(url)
    return response.json()

def filter_hourly_data(hour_data):
    return {
        'time': hour_data['time'],
        'temp_c': hour_data['temp_c'],
        'condition': hour_data['condition']['text'],
        'wind_kph': hour_data['wind_kph'],
        'wind_dir': hour_data['wind_dir'],
        'pressure_mb': hour_data['pressure_mb'],
        'precip_mm': hour_data['precip_mm'],
        # 'snow_cm': hour_data.get('snow_cm', 0),
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
        'vis_km': hour_data['vis_km'],

    }

def save_to_csv(data, filename):
    file_exists = os.path.isfile(filename)
    
    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        
        if not file_exists:
            writer.writeheader()  # Écrire l'en-tête si le fichier n'existe pas encore
            
        writer.writerows(data)

def save_to_csv(data, filename):
    file_exists = os.path.isfile(filename)
    
    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        
        if not file_exists:
            writer.writeheader()  # Écrire l'en-tête si le fichier n'existe pas encore
            
        writer.writerows(data)

def fetch_and_save_historical_data(location, days=7):
    historical_data = []
    for i in range(days):
        date = (datetime.datetime.now() - datetime.timedelta(days=i+1)).strftime('%Y-%m-%d')
        url = f'{base_url}/history.json?key={api_key}&q={location}&dt={date}'
        data = get_weather_data(url)
        for hour_data in data['forecast']['forecastday'][0]['hour']:
            filtered_data = filter_hourly_data(hour_data)
            historical_data.append(filtered_data)
    
    save_to_csv(historical_data, 'historical_data.csv')

fetch_and_save_historical_data(location)

def fetch_and_save_current_data(location):
    url = f'{base_url}/current.json?key={api_key}&q={location}'
    data = get_weather_data(url)
    current_hour_data = {
        'time': data['location']['localtime'],
        'temp_c': data['current']['temp_c'],
        'condition': data['current']['condition']['text'],
        'wind_kph': data['current']['wind_kph'],
        'wind_dir': data['current']['wind_dir'],
        'pressure_mb': data['current']['pressure_mb'],
        'precip_mm': data['current']['precip_mm'],
        #'snow_cm': 0,  # 
        'humidity': data['current']['humidity'],
        'cloud': data['current']['cloud'],
        'feelslike_c': data['current']['feelslike_c'],
        'windchill_c': data['current']['windchill_c'],
        'heatindex_c': data['current']['heatindex_c'],
        'dewpoint_c': data['current']['dewpoint_c'],
        #'will_it_rain': 0,  # 
        #'chance_of_rain': 0,  #
        #'will_it_snow': 0,  # 
        #'chance_of_snow': 0,  # 
        'gust_kph': data['current']['gust_kph'],
        'uv': data['current']['uv'],
        'vis_km': data['current']['vis_km'],
    }
    
    save_to_csv([current_hour_data], 'current_data.csv')

fetch_and_save_current_data(location)

def fetch_and_save_forecast_data(location, days=3):
    url = f'{base_url}/forecast.json?key={api_key}&q={location}&days={days}'
    data = get_weather_data(url)
    forecast_data = []
    
    for day in data['forecast']['forecastday']:
        for hour_data in day['hour']:
            filtered_data = filter_hourly_data(hour_data)
            forecast_data.append(filtered_data)
    
    save_to_csv(forecast_data, 'forecast_data.csv')

fetch_and_save_forecast_data(location)


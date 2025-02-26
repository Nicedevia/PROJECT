
import pandas as pd
from config import api_key, location
from utils import fetch_data

def get_weather_data(api_key, location):
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
    return fetch_data(url)

def extract_data(data):
    if data:
        try:
            location_name = data['location']['name']
            temp_c = data['current'].get('temp_c', None)
            precipitation = data['current'].get('precip_mm', None)
            visibility = data['current'].get('vis_km', None)
            return {
                'Location': location_name,
                'Temperature_C': temp_c,
                'Precipitation_mm': precipitation,
                'Visibility_km': visibility
            }
        except KeyError as e:
            print(f"Key error: {e}")
    return None

def save_to_csv(data, filename='part1/datag/data_weth/weather_data.csv'):
    df = pd.DataFrame([data])
    df.to_csv(filename, mode='a', header=not pd.io.common.file_exists(filename), index=False)

def main():
    data = get_weather_data(api_key, location)
    extracted_data = extract_data(data)
    if extracted_data:
        save_to_csv(extracted_data)
        print(pd.DataFrame([extracted_data]))
    else:
        print("Aucune donnée à enregistrer.")

if __name__ == "__main__":
    main()

import requests
import csv

def get_speed_limits_for_nice():
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = """
    [out:json];
    area[name="Nice"]->.searchArea;
    way["highway"](area.searchArea);
    out body geom;
    """
    
    response = requests.get(overpass_url, params={'data': overpass_query})
    
    if response.status_code != 200:
        print("Erreur lors de la requête à l'API Overpass.")
        return None

    data = response.json()
    
    # Filtrer les données pour ne garder que celles qui ont une limitation de vitesse 
    speed_limits = []
    for element in data['elements']:
        if 'tags' in element and 'maxspeed' in element['tags']:
            speed_limits.append(element)
    
    return speed_limits

def save_speed_limits_to_csv(speed_limits):
    filename = 'nice_speed_limits.csv'
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Latitude', 'Longitude', 'Limitation de Vitesse'])
        
        for element in speed_limits:
            if 'geometry' in element:
                for coord in element['geometry']:
                    lat = coord['lat']
                    lon = coord['lon']
                    maxspeed = element['tags'].get('maxspeed', 'Non spécifié')
                    writer.writerow([lat, lon, maxspeed])
            else:
                print("Pas de données géométriques pour cet élément.")

speed_limits = get_speed_limits_for_nice()
if speed_limits:
    save_speed_limits_to_csv(speed_limits)
    print(f"Les limitations de vitesse pour Nice ont été enregistrées dans 'nice_speed_limits.csv'.")
else:
    print("Aucune donnée n'a été récupérée.")

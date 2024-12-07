import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

PUBLIC_HOLIDAYS_URL = "https://publicholidays.info/country/france/2025"
SAVE_DIRECTORY = os.path.join("app", "donnée")  # Dossier de sauvegarde

def scrape_public_holidays(url):
    """
    Fonction pour scraper les jours fériés à partir de l'URL spécifiée.
    Retourne une liste de dictionnaires avec les dates et les noms des jours fériés.
    """
    try:
        logging.info(f"Scraping public holidays from {url}")
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        holidays = []
        
        holiday_table = soup.find("table")
        if holiday_table:
            for row in holiday_table.find_all("tr")[1:]: 
                cols = row.find_all("td")
                if len(cols) >= 2:
                    holiday_date = cols[0].text.strip() 
                    holiday_name = cols[1].text.strip()  
                    holidays.append({"date": holiday_date, "holiday": holiday_name})
        
        logging.info(f"Successfully scraped {len(holidays)} holidays.")
        return holidays
    
    except Exception as e:
        logging.error(f"Error scraping public holidays: {e}")
        return []

def save_to_csv(holidays, filename="joursf.csv"):
    """
    Fonction pour sauvegarder les jours fériés en CSV dans le dossier app/donnée.
    """
    try:
        # Assure que le dossier existe
        os.makedirs(SAVE_DIRECTORY, exist_ok=True)
        
        file_path = os.path.join(SAVE_DIRECTORY, filename)
        logging.info(f"Saving data to {file_path}")
        
        holidays_df = pd.DataFrame(holidays)
        holidays_df.to_csv(file_path, index=False)
        logging.info(f"Data successfully saved to {file_path}")
        
    except Exception as e:
        logging.error(f"Error saving to CSV: {e}")

holidays = scrape_public_holidays(PUBLIC_HOLIDAYS_URL)

if holidays:
    save_to_csv(holidays)

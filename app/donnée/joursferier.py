import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import unittest

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

PUBLIC_HOLIDAYS_URL = "https://publicholidays.info/country/france/2025"

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
    Fonction pour sauvegarder les jours fériés en CSV.
    """
    try:
        logging.info(f"Saving data to {filename}")
        holidays_df = pd.DataFrame(holidays)
        holidays_df.to_csv(filename, index=False)
        logging.info(f"Data successfully saved to {filename}")
        
    except Exception as e:
        logging.error(f"Error saving to CSV: {e}")

holidays = scrape_public_holidays(PUBLIC_HOLIDAYS_URL)

if holidays:
    save_to_csv(holidays)


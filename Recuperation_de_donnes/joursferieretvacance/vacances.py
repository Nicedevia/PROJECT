import requests
from bs4 import BeautifulSoup
import pandas as pd
import unittest
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

URL = "https://vacances-scolaires.education/"

def scrape_school_holidays(url):
    """
    Scrape les dates de vacances scolaires depuis le site et retourne une liste de dictionnaires avec les informations.

    :param url: URL du site à scraper
    :return: Liste de dictionnaires contenant les vacances scolaires
    """
    try:
        logging.info(f"Scraping school holidays from {url}")
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        holidays = []

        holiday_sections = soup.find_all("div", class_="vacances_zones")
        if not holiday_sections:
            logging.error("No holiday section found on the webpage.")
            return holidays

        for section in holiday_sections:
            zone_name = section.find("h2").text.strip()
            rows = section.find_all("tr")

            for row in rows:
                columns = row.find_all("td")
                if len(columns) == 3:
                    holiday = {
                        "Zone": zone_name,
                        "Vacation": columns[0].text.strip(),
                        "Dates": columns[1].text.strip()
                    }
                    holidays.append(holiday)

        logging.info(f"Successfully scraped {len(holidays)} holiday entries.")
        return holidays

    except Exception as e:
        logging.error(f"Error scraping school holidays: {e}")
        return []

def save_to_csv(data, filename="holidays_2024_2025.csv"):
    """
    Sauvegarde les données dans un fichier CSV.

    :param data: Données à sauvegarder
    :param filename: Nom du fichier CSV
    """
    try:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        logging.info(f"Data successfully saved to {filename}")
    except Exception as e:
        logging.error(f"Error saving to CSV: {e}")

# Tests unitaires
class TestScraping(unittest.TestCase):

    def test_scrape_school_holidays(self):
        holidays = scrape_school_holidays(URL)
        self.assertTrue(len(holidays) > 0, "Failed to scrape school holidays")

    def test_save_to_csv(self):
        data = [{"Zone": "Zone A", "Vacation": "Vacances de la Toussaint", "Dates": "Samedi 15 février 2025"}]
        save_to_csv(data, "test_holidays.csv")
        df = pd.read_csv("test_holidays.csv")
        self.assertTrue(len(df) > 0, "CSV file is empty")
        self.assertIn("Zone", df.columns, "CSV does not contain expected columns")

if __name__ == "__main__":
    holidays = scrape_school_holidays(URL)
    if holidays:
        save_to_csv(holidays)
    unittest.main(argv=[''], exit=False)

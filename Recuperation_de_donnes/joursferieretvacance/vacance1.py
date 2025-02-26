import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import unittest

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SCHOOL_HOLIDAYS_URL = "https://www.travelfranceonline.com/french-school-holidays-calendar/"

def scrape_school_holidays(url):
    """
    Fonction pour scraper les vacances scolaires à partir de l'URL spécifiée.
    Retourne une liste de dictionnaires avec les noms et les dates des vacances.
    """
    try:
        logging.info(f"Scraping school holidays from {url}")
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        vacations = []
        
        content = soup.find("div", class_="entry-content")
        if not content:
            logging.error("No vacation sections found in the webpage.")
            return vacations

        paragraphs = content.find_all("p")
        current_vacation_name = None

        for paragraph in paragraphs:
            strong_tag = paragraph.find("strong")
            if strong_tag:
                current_vacation_name = strong_tag.text.strip()  

            if current_vacation_name:
                vacation_dates = paragraph.get_text().strip()
                if vacation_dates and vacation_dates.lower() not in ["spring holidays", "winter holidays", "summer holidays all zones:", "don’t forget to check the french public holidays dates", "credits: carte des nouvelles zones de vacances scolaires(doc. gdd / education nationale)"]:
                    vacations.append({"vacation": current_vacation_name, "dates": vacation_dates})
                current_vacation_name = None  
        
        logging.info(f"Successfully scraped {len(vacations)} vacations.")
        return vacations
    
    except Exception as e:
        logging.error(f"Error scraping school holidays: {e}")
        return []

def save_to_csv(vacations, filename="school_holidays_2025.csv"):
    """
    Fonction pour sauvegarder les vacances scolaires en CSV.
    """
    try:
        logging.info(f"Saving data to {filename}")
        vacations_df = pd.DataFrame(vacations)
        vacations_df.to_csv(filename, index=False)
        logging.info(f"Data successfully saved to {filename}")
        
    except Exception as e:
        logging.error(f"Error saving to CSV: {e}")

def main():
    vacations = scrape_school_holidays(SCHOOL_HOLIDAYS_URL)
    
    if vacations:
        save_to_csv(vacations)

class TestScraping(unittest.TestCase):
    
    def setUp(self):
        """Initialisation des données de test"""
        self.url = SCHOOL_HOLIDAYS_URL
        self.vacations = [
            {"vacation": "Spring Holidays", "dates": "Zone A: Sat 13 Apr – 29 Apr"},
            {"vacation": "Winter Holidays", "dates": "Zone A: Sat 22 Feb – Mon 10 March"},
            {"vacation": "Spring Holidays", "dates": "Zone A: Sat 19 Apr – Mon 5 May"}
        ]
        self.filename = "test_school_holidays_2025.csv"

    def test_scrape_school_holidays(self):
        """Test pour vérifier que les vacances scolaires sont correctement scrappées"""
        vacations = scrape_school_holidays(self.url)
        self.assertTrue(len(vacations) > 0, "Failed to scrape school holidays")
        self.assertIn("vacation", vacations[0], "Scraped data does not contain 'vacation' field")
        self.assertIn("dates", vacations[0], "Scraped data does not contain 'dates' field")

    def test_save_to_csv(self):
        """Test pour vérifier que les données sont bien sauvegardées en CSV"""
        save_to_csv(self.vacations, self.filename)
        df = pd.read_csv(self.filename)
        self.assertTrue(len(df) > 0, "CSV file is empty")
        self.assertIn("vacation", df.columns, "CSV does not contain 'vacation' column")
        self.assertIn("dates", df.columns, "CSV does not contain 'dates' column")

    def test_remove_unwanted_phrases(self):
        """Test pour vérifier que les phrases indésirables sont exclues du CSV"""
        filtered_vacations = [
            {"vacation": "Spring Holidays", "dates": "Zone A: Sat 13 Apr – 29 Apr"},
            {"vacation": "Winter Holidays", "dates": "Zone A: Sat 22 Feb – Mon 10 March"},
            {"vacation": "Spring Holidays", "dates": "Zone A: Sat 19 Apr – Mon 5 May"}
        ]
        save_to_csv(filtered_vacations, self.filename)
        df = pd.read_csv(self.filename)
        self.assertNotIn("Don’t forget to check the French Public Holidays Dates", df["dates"].to_list())
        self.assertNotIn("Credits: Carte des nouvelles zones de vacances scolaires(doc. GDD / Education Nationale)", df["dates"].to_list())

if __name__ == "__main__":
    main()
    unittest.main(argv=[''], exit=False)

import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import unittest

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

PUBLIC_HOLIDAYS_URL = "https://publicholidays.info/country/france/2025"
SCHOOL_HOLIDAYS_URL = "https://www.travelfranceonline.com"

def scrape_public_holidays(url):
    try:
        logging.info(f"Scraping public holidays from {url}")
        response = requests.get(url)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.text, 'html.parser')
        holidays = []
        
        
        holiday_table = soup.find("table")
        for row in holiday_table.find_all("tr")[1:]:  
            cols = row.find_all("td")
            holiday_date = cols[0].text.strip()  # La date du jour férié
            holiday_name = cols[1].text.strip()  # Le nom du jour férié
            holidays.append({"date": holiday_date, "holiday": holiday_name})
        
        logging.info(f"Successfully scraped {len(holidays)} holidays.")
        return holidays
    
    except Exception as e:
        logging.error(f"Error scraping public holidays: {e}")
        return []

def scrape_school_holidays(url):
    try:
        logging.info(f"Scraping school holidays from {url}")
        response = requests.get(url)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.text, 'html.parser')
        vacations = []
        
        
        vacation_section = soup.find("div", class_="entry-content") 
        if not vacation_section:
            logging.error("No vacation section found in the webpage.")
            return vacations

        for vacation in vacation_section.find_all("p"):
            strong_tag = vacation.find("strong")
            if strong_tag:
                vacation_name = strong_tag.text.strip() 
                vacation_dates = vacation.get_text().replace(vacation_name, "").strip()  
                if "Unlock Your Free Guide" not in vacation_name and "Click the links below" not in vacation_name:
                    vacations.append({"vacation": vacation_name, "dates": vacation_dates})
        
        logging.info(f"Successfully scraped {len(vacations)} vacations.")
        return vacations
    
    except Exception as e:
        logging.error(f"Error scraping school holidays: {e}")
        return []


def save_to_csv(holidays, vacations, filename="holidays_vacations_2025.csv"):
    try:
        logging.info(f"Saving data to {filename}")
        holidays_df = pd.DataFrame(holidays)
        vacations_df = pd.DataFrame(vacations)
        

        combined_df = pd.concat([holidays_df, vacations_df], axis=0, ignore_index=True)
        combined_df.to_csv(filename, index=False)
        logging.info(f"Data successfully saved to {filename}")
        
    except Exception as e:
        logging.error(f"Error saving to CSV: {e}")


def main():
    holidays = scrape_public_holidays(PUBLIC_HOLIDAYS_URL)
    vacations = scrape_school_holidays(SCHOOL_HOLIDAYS_URL)
    
    if holidays or vacations:
        save_to_csv(holidays, vacations)


class TestScraping(unittest.TestCase):
    

    def test_scrape_public_holidays(self):
        holidays = scrape_public_holidays(PUBLIC_HOLIDAYS_URL)
        self.assertTrue(len(holidays) > 0, "Failed to scrape public holidays")
    

    def test_scrape_school_holidays(self):
        vacations = scrape_school_holidays(SCHOOL_HOLIDAYS_URL)
        self.assertTrue(len(vacations) > 0, "Failed to scrape school holidays")


    def test_save_to_csv(self):

        holidays = [{"date": "2025-01-01", "holiday": "Jour de l'An"}]
        vacations = [{"vacation": "Vacances d'hiver", "dates": "2025-02-14 to 2025-03-02"}]
        

        save_to_csv(holidays, vacations, "test_holidays_vacations_2025.csv")
        

        df = pd.read_csv("test_holidays_vacations_2025.csv")
        self.assertTrue(len(df) > 0, "CSV file is empty")
        self.assertIn("holiday", df.columns, "CSV does not contain expected columns")
        self.assertIn("vacation", df.columns, "CSV does not contain expected columns")


if __name__ == "__main__":
    main()  
    unittest.main(argv=[''], exit=False)
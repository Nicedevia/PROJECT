import requests
from bs4 import BeautifulSoup
import csv
import logging
import unittest

logging.basicConfig(level=logging.INFO)

def scrape_vacation_data(url):
    logging.info("Starting to scrape vacation data...")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Error fetching the page: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    
    table = soup.find('table') 

    if not table:
        logging.error("No table found on the page.")
        return None
    
    vacation_data = []
    
    rows = table.find_all('tr')
    for row in rows[1:]:  
        cells = row.find_all('td')
        
        if len(cells) >= 4:
            vacation_name = cells[0].text.strip()
            zone_a = cells[1].text.strip()
            zone_b = cells[2].text.strip()
            zone_c = cells[3].text.strip()
            corsica = cells[4].text.strip() if len(cells) > 4 else ""
            
            vacation_data.append({
                "Vacation Name": vacation_name,
                "Zone A": zone_a,
                "Zone B": zone_b,
                "Zone C": zone_c,
                "Corsica": corsica
            })
    
    if not vacation_data:
        logging.error("No data scraped. Please check the website structure.")
        return None
    
    logging.info(f"Scraped {len(vacation_data)} vacation entries.")
    return vacation_data

def save_to_csv(vacation_data, filename):
    logging.info(f"Saving data to {filename}...")
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Vacation Name', 'Zone A', 'Zone B', 'Zone C', 'Corsica']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in vacation_data:
            writer.writerow(row)
    
    logging.info(f"Data successfully saved to {filename}")

def main():
    url = "https://www.service-public.fr/particuliers/vosdroits/F31952"  # Adjust with the correct URL
    vacation_data = scrape_vacation_data(url)
    
    if vacation_data:
        save_to_csv(vacation_data, "vacation_data_2024_2025.csv")

class TestVacationScraping(unittest.TestCase):
    
    def test_scrape_vacation_data(self):
        url = "https://www.service-public.fr/particuliers/vosdroits/F31952"
        data = scrape_vacation_data(url)
        self.assertIsNotNone(data)
        self.assertGreater(len(data), 0)  # Ensure that data is not empty
        self.assertIn('Vacation Name', data[0])  # Check for expected keys

    def test_save_to_csv(self):
        test_data = [
            {"Vacation Name": "Vacances de la Toussaint", "Zone A": "19/10/2024", "Zone B": "19/10/2024", "Zone C": "19/10/2024", "Corsica": "19/10/2024"}
        ]
        save_to_csv(test_data, "test_vacation_data.csv")
        with open("test_vacation_data.csv", newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["Vacation Name"], "Vacances de la Toussaint")

if __name__ == "__main__":
    main()
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
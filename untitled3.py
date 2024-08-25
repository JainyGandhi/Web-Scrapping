# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1qH9Acn638W3JRlr3_K9mh8-T5FMFZf7L
"""

!apt-get update
!apt-get install -y wget unzip
!wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
!unzip chromedriver_linux64.zip
!mv chromedriver /usr/local/bin/
!apt-get install -y libnss3 libgconf-2-4
!wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
!dpkg -i google-chrome-stable_current_amd64.deb
!apt-get -f install
!apt-get update
!apt-get install -y chromium-chromedriver google-chrome-stable
!pip install selenium webdriver-manager pandas

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = '/usr/bin/google-chrome'  # Update if necessary

# Use ChromeDriverManager to automatically manage the driver
service = Service(ChromeDriverManager().install())

# Set up Selenium WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL to scrape (you can change this to any URL you want to scrape)
url = 'http://quotes.toscrape.com/'  # Replace with your target URL

# Open the webpage
driver.get(url)

try:
    # Wait for the page to load and the target elements to be present
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".quote"))
    )

    # Extract data
    data = []
    elements = driver.find_elements(By.CSS_SELECTOR, ".quote")
    for element in elements:
        text = element.find_element(By.CSS_SELECTOR, ".text").text
        author = element.find_element(By.CSS_SELECTOR, ".author").text
        tags = [tag.text for tag in element.find_elements(By.CSS_SELECTOR, ".tags .tag")]
        data.append({
            'Quote': text,
            'Author': author,
            'Tags': ', '.join(tags)
        })

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Save the DataFrame to an Excel file
    df.to_excel('/content/quotes_data.xlsx', index=False)
    print("Data has been saved to 'quotes_data.xlsx'")

finally:
    # Close the driver
    driver.quit()

from google.colab import files
files.download('/content/quotes_data.xlsx')


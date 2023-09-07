#! /usr/bin/env python3
import os
import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

with open('config.json') as config_file:
    config = json.load(config_file)

def get_data():
    """Fetch the list of companies to search for form an excel file"""
    fh = pd.ExcelFile(f"/Users/{os.environ['USER']}+{config['data_file']}")
    data = pd.read_excel(fh, sheet_name='hv', usecols=['name'])['name'].to_list()
    return data

companies = get_data()

# Set the path to chromedriver
path_chromedriver = f"/Users/{os.environ['USER']}+{config['chromedriver']}"

# Initialize a WebDriver instance (e.g., Chrome)
browser = webdriver.Chrome(executable_path=path_chromedriver)
browser.get('https://www.finder.fi/')

# Implicit wait (5 seconds) for general page loading
browser.implicitly_wait(5)

# check for each company, find the right page, and scrape the page
for company in companies:
    # Identify the search input field and send keys
    search_input = browser.find_element_by_name('search')
    search_input.clear()
    search_input.send_keys(company + Keys.RETURN)

    # Find the links that match the company name
    links = browser.find_elements(By.PARTIAL_LINK_TEXT, company)

    # Iterate through the links and click the right one
    for link in links:
        if link.text == company:
            print(f'scrapping page {company}, URL: {link.get_attribute("href")}')
            browser.execute_script("arguments[0].click();", link) # native selenium click() method does not work
            kaupparekisteri_elem = browser.find_elements_by_xpath('(//span[@class="Profile__RegistrationDate"]) [4]')
            
            print(f'Company: {company}, Registration date: {kaupparekisteri_elem[0].text}')
browser.quit()

# Test the script
#if __name__ == '__main__':

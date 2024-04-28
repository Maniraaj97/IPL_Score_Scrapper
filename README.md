# Cricket Data Scraping with Selenium and BeautifulSoup

This project involves scraping cricket match data from ESPN Cricinfo using Selenium and BeautifulSoup. The data scraped includes batting and bowling statistics for matches in the Indian Premier League (IPL) across different seasons.

## Prerequisites

- Python 3.x
- Selenium
- BeautifulSoup
- pandas
- Chrome WebDriver
- Install the required libraries using pip

## Explanation of the Code

- getURL(url,driver): This function navigates to the Cricket Stats section on ESPN Cricinfo, searches for IPL matches, and returns URLs for all IPL seasons.
- getMatchURL(url,driver): This function extracts URLs for individual matches from a given IPL season page.
- scoreScrap(url, table_name): This function scrapes batting and bowling statistics from a given match URL using BeautifulSoup.
- teamScrap(url): This function scrapes the names of the teams playing in a match from the given match URL.
- export_csv(url, folder_path, batting, bowling): This function exports the scraped data into CSV files.
- The main part of the script iterates through each IPL season, and each match within that season, scrapes batting and bowling data for each match, and saves the data into CSV files.

- ## Folder Structure

- cricket_data_scraping.py: Main Python script for scraping cricket data.
- README.md: This file, contains instructions and explanations.
- C:/Users/manir/IPL/: The folder where the scraped data is saved. You can change this path as needed in the script.

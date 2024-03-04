from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import StaleElementReferenceException
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import csv
import time
        
def getURL(url,driver):
    driver.find_element(By.XPATH,"//a[@title='Cricket Stats']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//input[@placeholder='Search for a trophy']").send_keys("ind")
    series = driver.find_elements(By.CLASS_NAME,"ds-flex")
    for i in series:
        if i.text == "Indian Premier League":
            i.click()
            break
    time.sleep(5)
    driver.find_element(By.XPATH, "//ul[@class='ds-flex ds-flex-col']/li[3]").click()
    time.sleep(3)
    years = driver.find_elements(By.CLASS_NAME,"ds-leading-none")
    all_seasons = [year.get_attribute("href") for year in years if "20" in year.text]
    return all_seasons   

def getMatchURL(url,driver):
    table = driver.find_element(By.TAG_NAME, "table")
    rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # Exclude the header row
    links = []
    
    for row in rows:
        last_element = row.find_elements(By.TAG_NAME, "td")[-1]
        last_element_url = last_element.find_element(By.TAG_NAME, "a").get_attribute("href")
        links.append(last_element_url)
    return links

def scoreScrap(url, table_name):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    tables = soup.find_all("table", class_=table_name)
    all_rows = []
    for table in tables:
        headers = table.find_all("th")
        titles = [header.text for header in headers]
        rows = table.find_all("tr")
        new_rows = []
        for row in rows[1:]:
            data = row.find_all("td")
            row = [td.text for td in data]
            new_rows.append(row)
        df_table = pd.DataFrame(new_rows, columns=titles)
        all_rows.append(df_table)
    return all_rows

def teamScrap(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    team_name_spans = soup.find_all("span", class_="ds-text-tight-l ds-font-bold ds-text-typo hover:ds-text-typo-primary ds-block ds-truncate")
    team_names = [span.text.strip() for span in team_name_spans]
    return team_names

def export_csv(url,folder_path, batting, bowling):
    file_name = url.split("/")[-2]
    file_path = os.path.join(folder_path, file_name)
    batting.to_csv(file_path + "_innings1.csv", index=False)
    bowling.to_csv(file_path + "_innings2.csv", index=False)
        
url = "https://www.espncricinfo.com/"
folder_path = "C:/Users/manir/IPL/"
ex_st_time = time.time()
driver = webdriver.Chrome()
driver.get(url)
driver.maximize_window()
seasonURL = getURL(url,driver)
i=1
for matchURL in seasonURL:
    start_time = time.time()
    dir = matchURL.split("/")[-3] + str(i)
    parent_dir = folder_path
    path = os.path.join(parent_dir,dir)
    os.makedirs(path)
    driver.get(matchURL)
    links = getMatchURL(matchURL,driver)
    for link in links:
        batting_table = "ci-scorecard-table"
        bowling_table = "ds-w-full ds-table ds-table-md ds-table-auto"
        batting_scorecard = scoreScrap(link, batting_table)
        bowling_scorecard = scoreScrap(link, bowling_table)
        team_names = teamScrap(link)
        team1 = team_names[0]
        team2 = team_names[1]
        df_batting = pd.DataFrame()
        df_bowling= pd.DataFrame()
        for j in range(len(batting_scorecard)):
            temp_batting = pd.DataFrame(columns=batting_scorecard[j].columns, data=[[team_names[j]]*len(batting_scorecard[j].columns)])
            temp_bowling = pd.DataFrame(columns=bowling_scorecard[j].columns, data=[[team_names[j]]*len(bowling_scorecard[j].columns)])
            df_batting = pd.concat([df_batting,temp_batting,batting_scorecard[j]], ignore_index=True)
            df_bowling = pd.concat([df_bowling,temp_bowling,bowling_scorecard[j]], ignore_index=True)
        export_csv(link,path,df_batting,df_bowling)
    end_time = time.time()
    print(f"Season {i} Duration:", end_time - start_time)
    i=i+1
ex_end_time = time.time()
print("Overall Duration:", ex_end_time - ex_st_time)
        




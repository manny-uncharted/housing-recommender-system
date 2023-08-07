# import libraries
import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm
import requests
import pandas as pd
from bs4 import BeautifulSoup

    
def webscrape_openrent(SCROLL_PAUSE_TIME = 0.5,no_of_scrolls = 100):
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    
    url = 'https://www.openrent.co.uk/properties-to-rent/london?term=London'
    driver.get(url)
    

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    WebDriverWait(driver, 300)

    for i in tqdm(range(no_of_scrolls)):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        
    html_content = driver.page_source

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    property_listings = soup.find(id = 'property-data')

    all_links = [propert['href'] for propert in property_listings.find_all('a',class_ = 'pli clearfix')]
    
    all_specs = []
    for link in tqdm(all_links):
        page = requests.get(f'https://www.openrent.co.uk{link}').text.replace('\r','').replace("\n",'').replace('\xa0', ' ')

        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(page, 'html.parser')
        spec_dict = {}
        spec_dict['title'] = soup.find('h1').text
        spec_dict['description'] = soup.find(class_ = 'description').text

        for table in soup.find(id= 'FeaturesTab').find_all('table'):
            for row in table.find_all('tr'):
                feature = row.find_all('td')[0].text#.replace('\n','')#.replace('\r','')
                if len(row.find_all('td')[1].find_all('i'))>0:
                    if row.find_all('td')[1].find_all('i')[0]['class'] == 'fa fa-check':
                        value = 'Yes'
                    else:
                        value = 'No'
                else:
                    value = row.find_all('td')[1].text#.replace('\n','').replace('\r','')
                spec_dict[feature] = value
        station_distances = []
        for row in soup.find(id = 'LocalTransport').find_all('tr')[1:]:
            station = row.find_all('td')[1].text
            distance = row.find_all('td')[2].text
            station_distances.append([station,distance])
        spec_dict['station_distances'] = station_distances
        all_specs.append(spec_dict)
        
    df = pd.DataFrame.from_dict(all_specs, orient='columns')
    return df


# class Webscraper:

#     def soup

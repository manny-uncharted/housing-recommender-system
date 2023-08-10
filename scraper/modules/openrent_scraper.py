import time
import requests
import os
from bs4 import BeautifulSoup
import pandas as pd
import csv
import boto3
from dotenv import load_dotenv
import pathlib

load_dotenv()

# AWS S3 Config
ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
SECRET_KEY = os.environ.get("AWS_SECRET_KEY")

# You should not have to set this
ENDPOINT= None

# Your s3-bucket region
REGION = os.environ.get("REGION") or "us-east-1"

BUCKET_NAME = os.environ.get("BUCKET_NAME")


os.environ["AWS_ACCESS_KEY_ID"] = ACCESS_KEY
os.environ["AWS_SECRET_ACCESS_KEY"] = SECRET_KEY

def convert_list_to_dict(summarize_headlines):
  d1 = {}
  for i in summarize_headlines:
      d1.update(i)
  return d1

def openrent_scrape():
    url = f"https://www.openrent.co.uk/properties-to-rent/london?term=london&viewingProperty=31"
    headers = {
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
          "Accept-Language": "en-US,en;q=0.9"
      }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    property_listings = soup.find_all("a", class_="pli")
    # print(property_listings)
    # print(len(property_listings))
    properties = []
    count = 0
    for listing in property_listings:
        link = listing.get("href")
        # print(link)
        price = listing.find("div", class_="lpcc").find("div", class_="listing-info").find("div", class_="price-location").find("div", class_="pl-cont").find("div", class_="pim").find("h2").text.strip()
        distance = listing.find("div", class_="lpcc").find("div", class_="listing-info").find("div", class_="price-location").find("div", class_="pl-cont").find("div", class_="ltc").text.strip()
        timestamp = listing.find("div", class_="lpcc").find("div", class_="listing-info").find("div", class_="price-location").find("div", class_="timestamp")
        title = listing.find("div", class_="lpcc").find("div", class_="listing-info").find("div", class_="location-description").find("div", class_="ldc").find("span", class_="banda").text.strip()
        description = listing.find("div", class_="lpcc").find("div", class_="listing-info").find("div", class_="location-description").find("div", class_="ldc").find("p", class_="listing-desc").text.strip()
        details = listing.find("div", class_="lpcc").find("div", class_="listing-info").find("div", class_="location-detail").find("ul", class_="lic").text.strip()
        if timestamp:
          timestamp = timestamp.text.strip()
        else:
          timestamp = "Not present"
        if link:
          link = url + link
        properties.append({
            "Title": str(title),
            "Location": str('london'),
            "Timestamp": str(timestamp),
            "Price": str(price),
            "Distance": str(distance),
            "Desc": str(description),
            "Details": str(details),
            "Link": link,
        })
        count += 1
        save_to_dict = convert_list_to_dict(properties)
        df = pd.DataFrame.from_dict(properties, orient='columns')
        files = df.to_csv('results.csv', sep=',', index=False, encoding='utf-8')
        BASE_DIR = pathlib.Path().resolve()
        DATA_PATH = BASE_DIR / 'results.csv'
        print("File exists: ", DATA_PATH)
        DATA_PATH_KEY_NAME = f"exports/data/{DATA_PATH}"
        print("S3 path: ", DATA_PATH_KEY_NAME)
        try:
          session = boto3.session.Session()
          client = session.client('s3', region_name=REGION)
          client.upload_file(str(DATA_PATH), BUCKET_NAME,  DATA_PATH_KEY_NAME)
        except:
          print("Files did not upload")
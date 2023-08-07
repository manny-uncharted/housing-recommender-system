from modules.selenium_start import webscrape_openrent
import pandas


selenium_instance = webscrape_openrent()
selenium_instance.to_csv('Openrent.csv', index = False)
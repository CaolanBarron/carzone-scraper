from genericpath import isfile
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
import os
import csv

# Set up selenium using the firefox webdriver
# Configure it to open the browser as headless so the browser window will not open
options = Options()
options.headless = True
service=FirefoxService(executable_path='geckodriver-v0.32.0-linux64/geckodriver')
browser = webdriver.Firefox(options=options,service=service)

# Returns an array of string urls carzone search page 1 to the provided argument amount
def getUrls(amount):
    urls = []
    for i in range(1,amount+1):
        urls.append('https://www.carzone.ie/search?page=' + str(i))
    
    return urls

# Takes an array of string urls which it then uses selenium to load each
# After saving the html as a BS4 object it returns an array of elements that match 'stock-summary-item'

def getRawHtml(urls):
    soups = []
    for i in urls:
        browser.get(i)
        # Necessary as selenium needs some time to load the page(I think)
        # (EDIT: Seems like its not necessary)
        # time.sleep(1)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        soup = soup.find_all('stock-summary-item')
        soups.append(soup)
    return soups

# Writes each raw html to a file into a folder
def writeRawHtml(soups):
    for id, soup in enumerate(soups):
        f = open("raw-html/page-{}.html".format(id+1), "w")
        f.write(soup.__str__())
        f.close()

# Takes each raw html file from the folder and creates a new file in a more human readable format
def writeFormattedHtml():
    formattedDir = 'raw-html'
    soups=[]
    for filename in os.listdir(formattedDir):
        f = os.path.join(formattedDir, filename)
        if os.path.isfile(f):
            file = open(f)
            soups.append(BeautifulSoup(file, 'html.parser'))
            file.close()
    
    for id, soup in enumerate(soups):
        f = open("formatted-html/page-{}.html".format(id+1), 'w')
        f.write(soup.prettify())
        f.close

"""
This block Loads the first 50 pages of the website and stores the raw html into a folder
It then gets each of the raw html and formats it into readable language in another folder
This is to make it easier to make a scraping program. It will not be neccessary when scraping is implemented.
I can just store the html in a raw format
"""
"""
urls = getUrls(50)
rawHtml = getRawHtml(urls)
writeRawHtml(rawHtml)
writeFormattedHtml()
"""

# Retrive Car data and append it to csv file
def writeCarCSV(fileName):
    file = open(fileName)

    # Get csv file in append file
    csv_file = open('cars-csv/car-data.csv', 'a')
    car_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL )

    soup = BeautifulSoup(file, 'html.parser')
    car_elements = soup.find_all('stock-summary-item')
    # Iterates through each car section and extracts specific data before writing it to the csv file
    for car_element in car_elements:
        features_details = car_element.find('span', class_='stock-summary__features__details').find('strong').text
        features_details = features_details.split()
        manu_year =  features_details[0]
        engine_type = features_details[-1]
        price = car_element.find('div', class_='cz-price').find('span').find('span').text
        dealer_loc = car_element.find('span', class_='stock-summary__features__dealer').text
        dealer_loc = dealer_loc[6:]

        car_url = car_element.find('a' )['href']
        car_writer.writerow([manu_year, price,dealer_loc, car_url])
    file.close()
    csv_file.close()

def  populateCSV():
    with open('cars-csv/car-data.csv','w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Manufacturing year', 'Price', 'Dealer location', 'URL'])

    for filename in os.listdir('raw-html'):
        f = os.path.join('raw-html', filename)
        if os.path.isfile(f):
            writeCarCSV(f)

populateCSV()

import pandas
df = pandas.read_csv('cars-csv/car-data.csv')
print(df)
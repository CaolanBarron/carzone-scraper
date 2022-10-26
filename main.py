from concurrent.futures.process import _chain_from_iterable_of_lists
from fileinput import filename
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

# Returns an array of string urls carzone search page 1 to the provided argument amount
def getCarSummaryUrls(amount):
    urls = []
    for i in range(1,amount+1):
        urls.append('https://www.carzone.ie/search?page=' + str(i))
    
    return urls

# Takes an array of string urls which it then uses selenium to load each
# After saving the html as a BS4 object it returns an array of elements that match 'stock-summary-item'

def getRawHtml(urls, delimiter):
    browser = webdriver.Firefox(options=options,service=service)
    soups = []
    for index, url in enumerate(urls):
        browser.get(url)
        # Necessary as selenium needs some time to load the page(I think)
        time.sleep(0.5)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        if delimiter:
            soup = soup.find_all(delimiter)
        print("Scraped: {}/{}".format(index + 1, len(urls)))
        soups.append(soup)
    browser.close()
    return soups

# Writes each raw html to a file into a folder
def writeRawHtml(soups, directory):
    for id, soup in enumerate(soups):
        f = open("{}/page-{}.html".format(directory,id+1), "w")
        f.write(soup.__str__())
        print("Wrote {} raw html file".format(id+1))
        f.close()

# Retrive Car summary data and append it to csv file
def writeCarSummaryCSV(fileName):
    file = open(fileName)

    # Get csv file in append file
    csv_file = open('cars-csv/car-summary-data.csv', 'a')
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

def  populateSummaryCSV():
    with open('cars-csv/car-summary-data.csv','w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Manufacturing year', 'Price', 'Dealer location', 'URL'])

    for filename in os.listdir('raw-summary-html'):
        f = os.path.join('raw-summary-html', filename)
        if os.path.isfile(f):
            writeCarSummaryCSV(f)
            
def getCarDetailsUrls(limit):
    urls = []
    with open('cars-csv/car-summary-data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for count,row in enumerate(csv_reader):
            if count > limit:
                break
            if count == 0:
                continue
            url = 'https://www.carzone.ie' + row[3]
            urls.append(url)
    return urls

def writeCarDetailsCSV(fileName):
    print(fileName)
    file = open(fileName)
    csv_file = open('cars-csv/car-detail-data.csv','a')
    car_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    
    soup = BeautifulSoup(file, 'html.parser')
    soups = soup.find_all('fpa-main-detail')

    for soup in soups:
        price = soup.find('div', class_='cz-price').find('span').text
        price = price.replace('€','')
        price = price.replace(',','')
        carDetailsList = soup.find('ul', class_='fpa-features')

        def findInnerSpan(input):
            object = carDetailsList.find('li',{'id':input})
            if object:
                return object.find('span', class_='fpa-features__item__text').text
            else:
                return 'missing'

        engine = findInnerSpan('engine') 
        body = findInnerSpan('bodytype')
        transmission = findInnerSpan('transmission')
        mileage = findInnerSpan('mileage') 
        color = findInnerSpan('colour')
        numDoors = findInnerSpan('doors')
        manYear = findInnerSpan('year').split()[0]

        phoneNo = soup.find('p', class_='fpa-actions__phone').text

        brand = soup.find('h1', class_='fpa-title').find('span').text
        if ')' in brand:
            brand = brand.split(')')[1].split()[0]
        else:
            brand = brand.split()[1]

        car_writer.writerow([price, engine, body, transmission, mileage, 
                            color, numDoors, manYear, phoneNo, brand])
    file.close()
    csv_file.close()

def populateDetailsCSV():
    with open('cars-csv/car-detail-data.csv','w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(['Price', 'Engine Type', 'Body Type', 'Transmission', 'Mileage',
                        'Colour','Door Number','Manufacturing Year','Phone Number','Car Brand'])
    
    for filename in os.listdir('raw-details-html'):
        f = os.path.join('raw-details-html', filename)
        if os.path.isfile(f):
            writeCarDetailsCSV(f)

import pandas as pd
import matplotlib.pyplot as plot

def csvFileToDataframe(file):
    df = pd.read_csv(file)
    yearPriceDF = df[["Price","Manufacturing Year"]]
    return yearPriceDF

def scatterGraphYearPrice():
    df = csvFileToDataframe('cars-csv/car-detail-data.csv')
    sp = df.plot.scatter(x='Manufacturing Year',
                         y= 'Price',
                         c='DarkBlue')
    plot.show(block=True)

def dataVisMenu():
    while True:

        print("1. Display Price/Year scatter graph")
        print("2. Return", end='\n'*2)
        print("Enter choice: ")
        option_choice = input()

        print('\n'*2)

        if option_choice == "1":
            scatterGraphYearPrice()
        elif option_choice == "2":
            break



# Interface for user to make interaction easier
if __name__ == '__main__':
    while True:
        print("1. Write car summarys as raw html")
        print("2. Convert car summarys to single csv details file")
        print("3. Write car details as raw html")
        print("4. Convert car details to csv file using car summary csv urls", end='\n'*2)
        print("5. Open data visualisation menu", end='\n'*2)
        print("6. Exit",end='\n'*2)
        print("Enter choice: ")
        option_choice = input()

        print('\n'*2)

        if option_choice == "1":
            urls = getCarSummaryUrls(50)
            rawHtml = getRawHtml(urls, 'stock-summary-item')
            writeRawHtml(rawHtml, 'raw-summary-html')
        elif option_choice == "2":
            populateSummaryCSV()
        elif option_choice == "3":
            urls = getCarDetailsUrls(300)
            rawHtml = getRawHtml(urls,'fpa-main-detail')
            writeRawHtml(rawHtml, 'raw-details-html')
        elif option_choice == "4":
            populateDetailsCSV()
        elif option_choice == "5":
            dataVisMenu()
        elif option_choice == "6":
            break
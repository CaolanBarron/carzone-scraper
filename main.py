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
def getCarSummaryUrls(amount):
    urls = []
    for i in range(1,amount+1):
        urls.append('https://www.carzone.ie/search?page=' + str(i))
    
    return urls

# Takes an array of string urls which it then uses selenium to load each
# After saving the html as a BS4 object it returns an array of elements that match 'stock-summary-item'

def getRawSummaryHtml(urls):
    soups = []
    for i in urls:
        browser.get(i)
        # Necessary as selenium needs some time to load the page(I think)
        time.sleep(0.5)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        soup = soup.find_all('stock-summary-item')
        print("Scraped {} elements from: {}".format(soup.__len__(), i))
        soups.append(soup)
    return soups

# Writes each raw html to a file into a folder
def writeRawHtml(soups, directory):
    for id, soup in enumerate(soups):
        f = open("{}/page-{}.html".format(directory,id+1), "w")
        f.write(soup.__str__())
        print("Wrote {} raw html file".format(id+1))
        f.close()

# Takes each raw html file from the folder and creates a new file in a more human readable format
def writeFormattedHtml(rawDirectory, formattedDirectory):
    soups=[]
    for filename in os.listdir(rawDirectory):
        f = os.path.join(rawDirectory, filename)
        if os.path.isfile(f):
            file = open(f)
            soups.append(BeautifulSoup(file, 'html.parser'))
            file.close()
    
    for id, soup in enumerate(soups):
        f = open("{}/page-{}.html".format(formattedDirectory,id+1), 'w')
        f.write(soup.prettify())
        print("wrote {} formatted hmtl file".format(id+1))
        f.close

# Retrive Car data and append it to csv file
def writeCarCSV(fileName):
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
            writeCarCSV(f)
            
"""
This block Loads the first 50 pages of the website and stores the raw html into a folder
It then gets each of the raw html and formats it into readable language in another folder
This is to make it easier to make a scraping program. It will not be neccessary when scraping is implemented.
I can just store the html in a raw format
"""


if __name__ == '__main__':
    while True:
        print("1. Write car summarys as raw html")
        print("2. Convert raw car summary html to human readable")
        print("3. Convert car summarys to single csv details file")
        print("4. Exit",end='\n'*2)
        print("Enter choice: ")
        option_choice = input()

        print('\n'*2)

        if option_choice == "1":
            urls = getCarSummaryUrls(50)
            rawHtml = getRawSummaryHtml(urls)
            writeRawHtml(rawHtml, 'raw-summary-html')
        elif option_choice == "2":
            writeFormattedHtml('raw-summary-html','formatted-summary-html')
        elif option_choice == "3":
            populateSummaryCSV()
        elif option_choice == "4":
            break
from genericpath import isfile
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
import os

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

# Retrive Car data and save to csv file

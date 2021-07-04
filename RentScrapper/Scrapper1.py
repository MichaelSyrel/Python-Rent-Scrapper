import csv
import os
import random
import time
from bs4 import BeautifulSoup
from selenium import webdriver



def start():
    download_posts(1, 70000)


##################################### WEBSITE 1 #####################################

#Downloads all posts for a given range of pages
def download_posts(min_page, max_page):
    browser = get_browser()
    for i in range(min_page, max_page):

        browser.get(f'https://[WEBSITE-URL]{i}')#Selenium opens the relevant rent page
        soup = BeautifulSoup(browser.page_source, "html.parser")
        page_file = get_pages_file(f'page_{i}')
        main = soup.find_all("div", {"class": "right_panel"})
        if len(main) < 1:
            continue
        main = main[0].find_all("div", {"class": "main"})
        if len(main) < 1:
            continue

        header = soup.find("div", {"class": "toptitle"})
        main[0].insert(2,header)

        page_file.write("%s\n" % main[0].prettify())
        page_file.close()

#If doesnt exists - creates then return the relevant file
def get_pages_file(page_name):
    write_type = "x"
    if os.path.exists(f"pages/{page_name}.html"):
        write_type = "w"
    f = open(f"pages/{page_name}.html", write_type, encoding='utf-8')
    return f

#Initialization of the selenium webdriver as a Chrome browser with options
def get_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    browser = webdriver.Chrome(options=options,
                               executable_path=r'C:\Users\syrel\PycharmProjects\Yad2RentScrapper\venv\Scripts\chromedriver.exe')
    return browser




if __name__ == '__main__':
    start()

import csv
import os
import random
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver



def start():
    download_posts(1, 70000)


##################################### WEBSITE 2 #####################################

#Scrapes the data of each link in a given csv file
def scrape_links(start_index, end):
    browser = get_browser()
    for i in range(start_index, end):
        f = get_links_file(f'links_{i}')
        links = get_current_page_links(browser, i)
        if len(links) == 0:
            links = get_current_page_links(browser, i)
        for link in links:
            f.write("%s,\n" % link)
        f.close()

#returns a file from 'links' folder with links for the relevant posts
def get_links_file(page_name):
    write_type = "x"
    if os.path.exists(f"links/{page_name}.txt"):
        write_type = "w"
    f = open(f"links/{page_name}.txt", write_type, encoding='utf-8')
    return f


#Gets the links of the current page
def get_current_page_links(browser, page_index):
    links = []
    browser.get(f'https://[WEBSITE-URL]/{page_index}')
    soup = BeautifulSoup(browser.page_source, "html.parser")
    main_table = soup.find("table", {"id": "mainresults"})
    feed_items = main_table.find_all("td", {"class": "details"})
    for j in range(len(feed_items)):
        link = feed_items[j].find("a")
        af = link["href"]
        links.append(af)
    return links

#Initialization of the selenium webdriver as a Chrome browser with options
def get_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    browser = webdriver.Chrome(options=options,
                               executable_path=r'C:\Users\syrel\PycharmProjects\Yad2RentScrapper\venv\Scripts\chromedriver.exe')
    return browser


##################################### COMMON UTIL ####################################


#Generic function to return address,apartment type and amount of rooms from the title
def get_title_data(soup):
    h1_split = soup.find("div",{"class":"toptitle"}).find("h1").text.split("|")
    rooms_split = h1_split[0].split("חדרים")[0].split("\n")[1].strip().split(" ")
    print(rooms_split)
    rooms = rooms_split[0]
    apartment_type = rooms_split.split(" ")[5]
    print(apartment_type)
    return {
        "address":h1_split[1].split("\n")[0],
        "apartment_type":apartment_type,
        "rooms":rooms
    }


if __name__ == '__main__':
    start()

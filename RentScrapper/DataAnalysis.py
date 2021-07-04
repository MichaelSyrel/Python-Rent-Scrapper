import csv
import os
import re

import matplotlib as matplotlib
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency


def start():
    write_all_posts_to_csv_file()


#Returns boolean value that represents if a property exists in the current rent post
def property_is_cheked(properties, property_index):
    checked = properties[property_index].find("img")['src'] == "/Images/checked.png"
    return '1' if checked else '0'

# Returns the current and the max floor
def get_floors(properties, property_index):
    floors_split = properties[property_index].find("span").text.split(" ")
    return {
        "floor": '-1' if len(floors_split) < 13 else floors_split[6],
        "max_floor": '-1' if len(floors_split) < 13 else floors_split[8].split("\n")[0]
    }

# Returns the size of the apartment in square meters
def get_size_in_meters(properties, property_index):
    size_split = properties[property_index].text.split(" ")
    if (len(size_split) < 16):
        return '-1'
    return size_split[16].split("\n")[0]

# Returns the price of the current post
def get_price(soup):
    price_split = soup.find("div", {"class": "PriceInAd"}).text.split(" ")
    if (len(price_split) < 16):
        return '-1'
    return price_split[16].split("\n")[0]


def get_title_data(soup):
    h1_split = soup.find("div", {"class": "toptitle"}).find("h1").text.split("|")
    rooms_split = h1_split[0].split("חדרים")[0].split("\n")[1].strip().split(" ")
    rooms = rooms_split[len(rooms_split) - 1]
    appartment_type_string_length = 1 if len(rooms_split) < 3 else 2
    apartment_type = " ".join(rooms_split[:appartment_type_string_length])
    return {
        #         "address": '' if len(h1_split) < 2 else h1_split[1].split("\n")[0],
        "apartment_type": apartment_type,
        "rooms": rooms
    }

# Generic function to return address,apartment type and amount of rooms from the title
def get_page_data(page_number):
    with open(f'C://Users//syrel//PycharmProjects//Yad2RentScrapper//pages/page_{page_number}.html', 'r',
              encoding="UTF-8") as f:
        page_html = f.read()
        soup = BeautifulSoup(page_html)
        properties = soup.find("div").find("div").find("div").find("div").find_all("div")
        floors = get_floors(properties, 18)
        title_data = get_title_data(soup)
        obj = {
            #             'address':title_data['address'],
            'apartment_type': title_data['apartment_type'],
            'rooms': title_data["rooms"],
            'price': get_price(soup),
            'window_bars': property_is_cheked(properties, 4),
            'partners': property_is_cheked(properties, 5),
            'furniture': property_is_cheked(properties, 6),
            'elevator': property_is_cheked(properties, 7),
            'balcony': property_is_cheked(properties, 8),
            'air_conditioner': property_is_cheked(properties, 10),
            'parking': property_is_cheked(properties, 11),
            'floor': floors["floor"],
            'max_floor': floors["max_floor"],
            'size_in_meters': get_size_in_meters(properties, 19),
        }
        return obj

# Returns csv representation of a given post properties
def get_post_csv(post):
    csv_string = ''
    for key in post:
        csv_string += f'{post[key]},'
    return csv_string[:-1]


# returns a list of headers of given csv file
def get_csv_header(page_index):
    random_post = get_page_data(page_index)
    csv_headers = ''
    for key in random_post:
        csv_headers += f'{key},'
    return csv_headers[:-1]


def write_all_posts_to_csv_file():
    with open(f'./main.csv', 'a', encoding="UTF-8") as f:
        f.write(f'{get_csv_header(51)}\n')
        for i in range(1, 70000):
            file_path = f'C://Users//syrel//PycharmProjects//Yad2RentScrapper//pages//page_{i}.html'
            if os.path.exists(file_path):
                page_data = get_page_data(i)
                post_csv = get_post_csv(page_data)
                if post_csv is not None:
                    f.write(post_csv + "\n")
                    if (i % 100 == 0):
                        print(i)
    return





if __name__ == '__main__':
    start()
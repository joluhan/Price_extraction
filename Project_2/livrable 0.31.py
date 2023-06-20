# ============================== Étape 3 : Extraire les données du site ==============================

import requests
from bs4 import BeautifulSoup

# import csv
# import os
# import re
from unicodedata import normalize
from urllib.parse import urljoin


# # >>>>>>==========================TODO============================
# A= Create a loop that collect all url of each category
# # >>>>>>==========================TEST============================
# extract all urls of each category
base_url = "https://books.toscrape.com/catalogue/page-1.html"


def category_urls_list(base_url):
    category_urls_list = []

    response = requests.get(base_url)
    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")

    category_list = soup.find("ul", class_="nav-list")
    category_items = category_list.find_all("li")

    for index, category_item in enumerate(category_items):
        if index > 0:  # Start appending from the second element
            category_url = urljoin(base_url, category_item.find("a")["href"])
            category_urls_list.append(category_url)

    return category_urls_list


list_urls = category_urls_list(base_url)
# print(list_urls)
# # ==========================TEST============================<<<<<<<


# # >>>>>>==========================TODO============================
# B= create another loop that get the book url in each category
# # >>>>>>==========================TEST============================


# # ==========================TEST============================<<<<<<<


# # >>>>>>==========================TODO============================
# and put them in a list and then use a for loop to extract the data and save them is a csv file
# # >>>>>>==========================TEST============================


# # ==========================TEST============================<<<<<<<

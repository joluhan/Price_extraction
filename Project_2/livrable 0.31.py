# ============================== Étape 3 : Extraire les données du site ==============================

import requests
from bs4 import BeautifulSoup
import csv
import os
import re
from unicodedata import normalize
from urllib.parse import urljoin


# # >>>>>>==========================TODO============================
# A= Create a loop that collect all url of each category
# # >>>>>>==========================TEST============================
# extract all urls of each category
base_url = "https://books.toscrape.com/catalogue/page-1.html"


def category_urls_list(base_url):
    category_urls_list = []

    # Send a GET request to the specified URL
    response = requests.get(base_url)
    # Parse the HTML
    soup = BeautifulSoup(response, "html.parser")

    url_category_extraction = (
        soup.find("ul", {"class": "nav nav-list"}).find("li").find("a").find_all("a")
    )
    for url_category in url_category_extraction:
        category_urls_list.append(url_category.find("a")["href"])


# # ==========================TEST============================<<<<<<<


# # >>>>>>==========================TODO============================
# B= create another loop that get the book url in each category
# # >>>>>>==========================TEST============================


# # ==========================TEST============================<<<<<<<


# # >>>>>>==========================TODO============================
# and put them in a list and then use a for loop to extract the data and save them is a csv file
# # >>>>>>==========================TEST============================


# # ==========================TEST============================<<<<<<<

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

# # ==========================TEST============================<<<<<<<


# # >>>>>>==========================TODO============================
# B= create another loop that get the book url in each category
# # >>>>>>==========================TEST============================
# Function ==========> urls extraction
def extract_urls():
    urls = []
    while True:
        # Send a GET request to the specified URL
        response = requests.get(url_home)

        # Retrieve the content of the response
        html_content = response.content
        # Check if the request was successful
        if response.status_code == 200:
            print(f"Access to {url_home} successful")
        else:
            print(f"Access to {url_home} unsuccessful")

        # Parse the HTML
        soup = BeautifulSoup(html_content, "html.parser")

        # Find and extract every URL
        url_home = response.url  # Get the base URL of the page

        # Find all article elements with the specified class
        articles = soup.find_all("article", class_="product_pod")
        for article in articles:
            # Find the href attribute of the nested <a> element
            href = article.find("h3").find("a")["href"]
            absolute_url = urljoin(
                url_home, href
            )  # Convert relative URL to absolute URL
            urls.append(absolute_url)  # Add the absolute URL to the list of URLs

        # Find the next page link
        next_link = soup.find("li", class_="next")
        if next_link is None:
            break  # Exit the loop if there is no next page

        # Get the URL for the next page
        next_page_url = urljoin(url_home, next_link.find("a")["href"])
        url_home = next_page_url

    return urls


# # ==========================TEST============================<<<<<<<


# # >>>>>>==========================TODO============================
# and put them in a list and then use a for loop to extract the data and save them is a csv file
# # ==========================TODO============================<<<<<<<


# # >>>>>>==========================TEST============================

# # ==========================TEST============================<<<<<<<

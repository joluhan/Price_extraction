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
    category_urls_list = []  # Create an empty list to store category URLs

    response = requests.get(base_url)  # Send a GET request to the specified URL
    html_content = response.content  # Get the content of the response
    soup = BeautifulSoup(html_content, "html.parser")  # Parse the HTML content

    category_list = soup.find("ul", class_="nav-list")  # Find the category list element
    category_items = category_list.find_all(
        "li"
    )  # Find all list items within the category list

    for index, category_item in enumerate(category_items):
        if index > 0:  # Start appending from the second element
            category_url = urljoin(
                base_url, category_item.find("a")["href"]
            )  # Get the URL of the category item
            category_urls_list.append(
                category_url
            )  # Append the category URL to the list

    return category_urls_list  # Return the list of category URLs


# Call the function to get the list of category URLs
list_urls = category_urls_list(base_url)
# /print(list_urls)  # Print the list of category URLs
# # ==========================TEST============================<<<<<<<


# # >>>>>>==========================TODO============================
# B= create another loop that get the book url in each category
# # >>>>>>==========================TEST============================
# Function ==========> urls extraction
def extract_urls(list_urls):
    urls = []

    for url in list_urls:
        # Send a GET request to the specified URL
        response = requests.get(url)

        # Retrieve the content of the response
        html_content = response.content
        # Check if the request was successful
        if response.status_code == 200:
            print(f"Access to {url} successful")
        else:
            print(f"Access to {url} unsuccessful")

        # Parse the HTML
        soup = BeautifulSoup(html_content, "html.parser")

        # Find and extract every URL
        url_home = response.url  # Get the base URL of the page

        # Find all article elements with the specified class
        articles = soup.find_all("article", class_="product_pod")
        for article in articles:
            # Find the href attribute of the <a> element
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
        list_urls.append(next_page_url)  # Append the next page URL to the list of URLs

    return urls


# /print(extract_urls(list_urls))

# # ==========================TEST============================<<<<<<<


# # >>>>>>==========================TODO============================
# and put them in a list and then use a for loop to extract the data and save them is a csv file
# # >>>>>>==========================TEST============================


# # ==========================TEST============================<<<<<<<

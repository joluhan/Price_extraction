# ============================== Étape 1 : Extraire les données d’un seul produit ==============================

import requests
from bs4 import BeautifulSoup
import csv
import os
from urllib.parse import urljoin

# Specify the URL to scrape
url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
base_url = "https://books.toscrape.com"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    print(f"Access to {url} successful")
else:
    print(f"Access to {url} unsuccessful")


# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Book URL
book_url = "catalogue/a-light-in-the-attic_1000/index.html"
# Join the URLs
absolute_url = urljoin(base_url, book_url)

# Extract the desired information

product_page_url = absolute_url
universal_product_code = soup.find("th", string="UPC").find_next_sibling("td").string
title = soup.find("h1").string
price_including_tax = (
    soup.find("th", string="Price (incl. tax)").find_next_sibling("td").string
)
price_excluding_tax = (
    soup.find("th", string="Price (excl. tax)").find_next_sibling("td").string
)
number_available = soup.find("th", string="Availability").find_next_sibling("td").string
product_description = (
    soup.find("div", {"id": "product_description"}).find_next("p").string.strip()
)
category = soup.find("a", href="../category/books/poetry_23/index.html").string

review_rating = soup.find("p", class_="star-rating")["class"][1]
image_url = urljoin(base_url, soup.img["src"])

# Prepare the data to write to the CSV file
data = [
    [
        "product_page_url",
        "universal_product_code",
        "title",
        "price_including_tax",
        "price_excluding_tax",
        "number_available",
        "product_description",
        "category",
        "review_rating",
        "image_url",
    ],
    [
        product_page_url,
        universal_product_code,
        title,
        price_including_tax,
        price_excluding_tax,
        number_available,
        product_description,
        category,
        review_rating,
        image_url,
    ],
]

# Write the data to the CSV file
directory = r"C:\Users\johan\Desktop"
filename = "book_data01.csv"
filepath = os.path.join(directory, filename)

with open(filepath, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)

# Print the success message
print(r"Data has been successfully saved to C:\Users\johan\Desktop\book_data.csv")

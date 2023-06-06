# écrire un script Python qui visite page et extrait les informations détaillées dans le document des exigences.

import requests  # librairy to make HTTP requests and interact with web ressources
from bs4 import (
    BeautifulSoup,
)  # Importing BeautifulSoup from the bs4 module for HTML parsing and manipulation
import csv  # Import the csv module for reading and writing CSV files
import os  # Import the os module for operating system-related functionalities

url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"  # variable creation of website I want to scrape

response = requests.get(url)  # variable requesting opening the website

# condition to check if access to the website susscessful or not
if response.status_code == 200:
    print(f"access to {url} successful")
else:
    print(f"access to {url} unsuccessful")

soup = BeautifulSoup(
    response.content, "html.parser"
)  # create a BeautifulSoup object by passing in the response content while specifying the parser to use


book_containers = soup.find_all(
    "article", class_="product_pod"
)  # Find all the book containers

book_data = []  # Initialize a list to store the extracted data

for container in book_containers:
    product_page_url = url
    universal_product_code = (
        soup.find("th", string="UPC").find_next_sibling("td").string
    )
    title = soup.find("h1").string
    price_including_tax = (
        soup.find("th", string="Price (incl. tax)").find_next_sibling("td").string
    )
    price_excluding_tax = (
        soup.find("th", string="Price (excl. tax)").find_next_sibling("td").string
    )
    number_available = (
        soup.find("th", string="Availability").find_next_sibling("td").string
    )
    product_description = (
        soup.find("div", {"id": "product_description"}).find_next("p").string.strip()
    )
    category = soup.find("a", href="../category/books/poetry_23/index.html").string

    review_rating = soup.find("p", class_="star-rating")["class"][1]
    image_url = soup.find("div", {"id": "product_gallery"}).find("img")["src"]

    # title = container.h3.a.text
    # price = container.find("p", class_="price_color").text

    book_data.append(
        {
            "Pdt url": product_page_url,
            "UPC": universal_product_code,
            "Title": title,
            "Price incl VAT": price_including_tax,
            "Price excl VAT": price_excluding_tax,
            "Nb available": number_available,
            "Pdt description": product_description,
            "Category": category,
            "Review Rating": review_rating,
            "Img url": image_url,
        }
    )

folder_path = input(
    "Enter the desired folder path: "
)  # Prompt the user to enter the desired folder path

filename = os.path.join(
    folder_path, "book_data.csv"
)  # Define filename for the CSV file

# Write the data to the CSV file
with open(filename, "w", newline="") as csvfile:
    fieldnames = ["Title", "Price"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(book_data)

print(f"Data extraction successful. Saved as {filename}")  # Print success message

print(f"Location: {os.path.abspath(filename)}")  # Print location of data file

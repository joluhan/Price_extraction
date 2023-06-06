# ============================== Étape 2 : Extraire les données de tout une catégorie ==============================

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

# create a BeautifulSoup object by passing in the response content while specifying the parser to use
soup = BeautifulSoup(response.content, "html.parser")

# Find all the book containers
book_containers = soup.find_all("article", class_="product_pod")

# ==>> ajouter une fonction qui rentre dans chaque page pour extraire les données
# ===>> prendre en compte si "next" parcourir toute les pages

book_data = []  # Initialize a list to store the extracted data

for container in book_containers:
    product_page_url = container.h3.a
    universal_product_code = soup.find("th", string="UPC")
    title = soup.find("h1").string
    price_including_tax = soup.find("th", string="Price (incl. tax)")
    price_excluding_tax = soup.find("th", string="Price (excl. tax)")
    number_available = soup.find("th", string="Availability")
    product_description = soup.find("div", {"id": "product_description"})
    category = soup.find("a", href="../category/books/poetry_23/index.html")

    review_rating = soup.find("p", class_="star-rating")["class"][1]
    image_url = soup.find("img")

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

# Prompt the user to enter the desired folder path
csv_location = input("Enter the desired folder path: ")

# Define filename for the CSV file
csv_filename = input("Please enter the filename: ")
# Replace with the actual folder path
folder_path = "path/to/folder"
file_path = os.path.join(folder_path, csv_filename + ".csv")

# Write the data to the CSV file
# Define the column names for the CSV file
fieldnames = [
    "Pdt url",
    "UPC",
    "Title",
    "Price incl VAT",
    "Price excl VAT",
    "Nb available",
    "Pdt description",
    "Category",
    "Review Rating",
    "Img url",
]

# Write the data to the CSV file
with open(f"{csv_location}/{csv_filename}.csv", "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(book_data)

print(f"Data extraction successful. Saved as {csv_filename}")  # Print success message

print(f"Location: {os.path.abspath(csv_filename)}")  # Print location of data file

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

# ========================= TO ADD =========================
# ==>> ajouter une loop qui rentre dans chaque page pour extraire les données
# for into_page(range 21):
# ===>> prendre en compte si "next" parcourir toute les pages, faire une def
# def turn_the_page():
# ========================= TO ADD =========================

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

    # ========================= reminders soup.find =========================
    # title = container.h3.a.text
    # price = container.find("p", class_="price_color").text
    # ========================= reminders soup.find =========================

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


# Write the data to the CSV file
# Define the column names for the CSV file
fieldnames = [
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
filename = "book_data.csv"
filepath = os.path.join(directory, filename)

with open(filepath, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(fieldnames)

# Print success message
print(r"Data has been successfully saved to C:\Users\johan\Desktop\book_data.csv")

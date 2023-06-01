# ============================== Étape 2 : Extraire les données d’un seul produit ==============================

import requests
from bs4 import BeautifulSoup
import csv
import os

url = "http://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"  # variable creation of page to be scraped

response = requests.get(url)  # Send a GET request to the URL

# condition to check if access to the website susscessful or not
if response.status_code == 200:
    print(f"access to {url} successful")
else:
    print(f"access to {url} unsuccessful")

content_page = response.text  # print to check content of website

response_content = BeautifulSoup(
    response.content, "html.parser"
)  # create a BeautifulSoup object by passing in the response content while specifying the parser to use

book_container = response_content.find(
    "article", class_="product_page"
)  # Find the book container for the specific book

# Extract the title and price for the book
title_element = book_container.find("h1")
title = title_element.text.strip() if title_element else ""
price_element = book_container.find("p", class_="price_color")
price = price_element.text.strip() if price_element else ""
book_data = [{"Title": title, "Price": price}]

folder_path = input(
    "Enter the desired folder path: "
)  # Prompt the user to enter the desired folder path

name_file_result = input("Give a name to the file: ")

filename = os.path.join(
    folder_path, name_file_result + ".csv"
)  # Define filename for the CSV file

# Write the data to the CSV file
with open(filename, "w", newline="") as csvfile:
    fieldnames = ["Title", "Price"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(book_data)

print(f"Data extraction successful. Saved as {filename}")  # Print success message
print(f"Location: {os.path.abspath(filename)}")  # Print location of data file

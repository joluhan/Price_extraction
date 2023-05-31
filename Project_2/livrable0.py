# écrire un script Python qui visite page et extrait les informations détaillées dans le document des exigences.

import requests  # librairy to make HTTP requests and interact with web ressources
from bs4 import (
    BeautifulSoup,
)  # Importing BeautifulSoup from the bs4 module for HTML parsing and manipulation
import csv  # Import the csv module for reading and writing CSV files
import os  # Import the os module for operating system-related functionalities

url = "http://books.toscrape.com/"  # variable creation of website I want to scrape

response = requests.get(url)  # variable requesting opening the website

# condition to check if access to the website susscessful or not
if response.status_code == 200:
    print(f"access to {url} successful")
else:
    print(f"access to {url} unsuccessful")

content_page = response.text  # print to check content of website

response_content = BeautifulSoup(
    response.content, "html.parser"
)  # create a BeautifulSoup object by passing in the response content while specifying the parser to use


# ========= to review !! imported & saved data are not correct =========
# Find the <h3> tag containing the book title
title_element = response_content.find("h3")
# Find the <p> tag containing the price
price_element = response_content.find("p", class_="price_colour")
# ========= to review !! imported & saved data are not correct =========

rows = [
    {"Title": title_element, "Price": price_element}
]  # Create a list of dictionaries (rows) to hold the extracted data

filename = "book_data.csv"  # Define filename for the CSV file

# Write the data to the CSV file
with open(filename, "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Data extraction successful. Saved as {filename}")  # Print success message

print(f"Location: {os.path.abspath(filename)}")  # Print location of data file

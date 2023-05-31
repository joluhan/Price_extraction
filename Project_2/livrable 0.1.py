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


book_containers = response_content.find_all(
    "article", class_="product_pod"
)  # Find all the book containers

book_data = []  # Initialize a list to store the extracted data

for container in book_containers:  # Iterate over each book container
    # Extract the title and price for each book
    title = container.h3.a.text
    price = container.find("p", class_="price_color").text

    book_data.append({"Title": title, "Price": price})

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

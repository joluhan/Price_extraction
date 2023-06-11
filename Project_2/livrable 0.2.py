import requests
from bs4 import BeautifulSoup
import csv
import os


# >>>>============= test =============

# url joining librairies
from urllib.parse import urljoin
import posixpath

# ============= test =============<<<<


# Target URL and base URL
url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
base_url = "https://books.toscrape.com"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    print(f"Access to {url} successful")
else:
    print(f"Access to {url} unsuccessful")

# Parse the response content with BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")


# >>>>============= test =============


# Category URL
category_url = "catalogue/category/books/travel_2/index.html"
# Book URL
book_url = "catalogue/a-light-in-the-attic_1000/index.html"
# Join the URLs
absolute_url = urljoin(base_url, book_url)


# ============= test =============<<<<


# List to store book data
book_data = []

# Loop to scrape data from multiple pages
while True:
    # Find all book containers
    book_containers = soup.find_all("article", class_="product_pod")
    print(book_containers)
    # ===============use tr/th to find the data =================================
    # Iterate through each book container to extract data
    for container in book_containers:
        # Extract data using appropriate selectors
        product_page_url = urljoin(base_url, container.h3.a["href"])
        title = container.h3.a["title"]
        price_incl_tax = container.find("p", class_="price_color").text
        price_excl_tax = (
            container.find("p", class_="price_color").find_next_sibling("p").text
        )
        availability = container.find("p", class_="instock availability").text.strip()
        product_desc_elem = container.find("p", class_="excerpt")
        product_desc = product_desc_elem.text if product_desc_elem else None
        category = soup.find("h1").text
        review_rating = container.find("p", class_="star-rating")["class"][1]
        image_url = urljoin(base_url, container.img["src"])
        upc_elem = container.find("th", string="UPC")
        upc = upc_elem.find_next_sibling("td").text.strip() if upc_elem else None
        # ===============use tr/th to find the data =================================

        # Append the extracted data as a dictionary to the book_data list
        book_data.append(
            {
                "Pdt url": product_page_url,
                "UPC": upc,
                "Title": title,
                "Price incl VAT": price_incl_tax,
                "Price excl VAT": price_excl_tax,
                "Nb available": availability,
                "Pdt description": product_desc,
                "Category": category,
                "Review Rating": review_rating,
                "Img url": image_url,
            }
        )

    # Find the next page button
    next_button = soup.find("li", class_="next")
    if next_button is None:
        break

    # Get the URL for the next page
    next_page_url = urljoin(base_url, next_button.a["href"])
    next_page_response = requests.get(next_page_url)
    soup = BeautifulSoup(next_page_response.content, "html.parser")

# Define fieldnames for CSV header
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

# Specify the directory, filename, and file path for the CSV
directory = r"C:\Users\johan\Desktop"
filename = "book_data.csv"
filepath = os.path.join(directory, filename)

# Write data to the CSV file
with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(book_data)

print(f"Data has been successfully saved to {filepath}")

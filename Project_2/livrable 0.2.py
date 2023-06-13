import requests
from bs4 import BeautifulSoup
import csv
import os

# url joining librairies
from urllib.parse import urljoin
import posixpath

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
# ============= test =============<<<<

# Category URL
category_url = "catalogue/category/books/travel_2/index.html"
# Book URL
book_url = "catalogue/a-light-in-the-attic_1000/index.html"
# Join the URLs
absolute_url = urljoin(base_url, book_url)

# List to store book data
book_data = []

# Loop to scrape data from multiple pages
while True:
    # Find all book containers
    book_containers = soup.find_all("article", class_="product_pod")

    # ===============use tr/th to find the data =================================
    # Iterate through each book container to extract data
    for container in book_containers:
        # Extract the desired information
        product_page_url = absolute_url
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
            soup.find("div", {"id": "product_description"})
            .find_next("p")
            .string.strip()
        )
        category = soup.find("a", href="../category/books/poetry_23/index.html").string

        review_rating = soup.find("p", class_="star-rating")["class"][1]
        image_url = urljoin(base_url, soup.img["src"])
        # ===============use tr/th to find the data =================================

        # Append the extracted data as a dictionary to the book_data list
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

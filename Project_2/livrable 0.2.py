# ============================== Étape 2 : Extraire les données d’une catégorie ==============================

# process:
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find
# https://www.geeksforgeeks.org/how-to-get-the-next-page-on-beautifulsoup/


import requests
from bs4 import BeautifulSoup
import csv
import os

# url joining librairies
from urllib.parse import urljoin

# Target URL and base URL
catalogue_url = (
    "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
)
base_url = "https://books.toscrape.com/"

# Send a GET request to the URL
response = requests.get(catalogue_url)

# Check if the request was successful
if response.status_code == 200:
    print(f"Access to {catalogue_url} successful")
else:
    print(f"Access to {catalogue_url} unsuccessful")

# Parse the response content with BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# >>>>============= test =============

# collect url of each book

# Initialize an empty list to store the book URLs
book_data = []

# Assuming `soup` refers to the BeautifulSoup object of the webpage content


# Find all book articles on the webpage
def find_all_book_articles(soup):
    book_articles = soup.findAll("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
    for article in book_articles:
        book_url = article.find("a", href=True)["href"]
        # join url with the base URL of the website
        book_url = urljoin(base_url, book_url)
        book_data.append(book_url)

        print(book_data)


find_all_book_articles(soup)
# # Iterate over each book article and collect the URLs
# for book_article in book_data:
#     # Find the anchor tag within the book article
#     if anchor_tag:
#         # Extract the relative URL
#         relative_url = anchor_tag
#         # Construct the absolute URL using the base URL of the website
#         absolute_url = urljoin(base_url, relative_url)
#         # Append the absolute URL to the book_data list
#         book_data.append(absolute_url)
#         # Print the absolute URL (optional)
#         print(absolute_url)
#     else:
#         # Handle cases where the anchor tag is not found
#         print("Anchor tag not found for a book article")

# extaire données de chaque url


# sauvegarder les données


# ============= test =============<<<<

# # Category URL
# category_url = "catalogue/category/books/travel_2/index.html"
# # Book URL
# book_url = "catalogue/a-light-in-the-attic_1000/index.html"
# # Join the URLs


# # Loop to scrape data from multiple pages
# while True:
#     # Request the URL of each page
#     response = requests.get(absolute_url)

#     soup_url = BeautifulSoup(response, "html.parser")
#     # Check if the request was successful
#     if response.status_code == 200:
#         print(f"Access to {absolute_url} successful")
#         continue

#     # Find all book containers
#     container = soup_url.find_all("article", class_="product_pod")

#     # ===============use tr/th to find the data =================================
#     # Iterate through each book container to extract data
#     for container in response:
#         # Extract the desired information

#         product_page_url = absolute_url
#         universal_product_code = (
#             soup.find("th", string="UPC").find_next_sibling("td").string
#         )
#         title = soup.find("h1").string
#         price_including_tax = (
#             soup.find("th", string="Price (incl. tax)").find_next_sibling("td").string
#         )
#         price_excluding_tax = (
#             soup.find("th", string="Price (excl. tax)").find_next_sibling("td").string
#         )
#         number_available = (
#             soup.find("th", string="Availability").find_next_sibling("td").string
#         )
#         product_description = (
#             soup.find("div", {"id": "product_description"})
#             .find_next("p")
#             .string.strip()
#         )
#         category = soup.find("a", href="../category/books/poetry_23/index.html").string

#         review_rating = soup.find("p", class_="star-rating")["class"][1]
#         image_url = urljoin(base_url, soup.img["src"])
#         # ===============use tr/th to find the data =================================

#         # Append the extracted data as a dictionary to the book_data list
#         book_data.append(
#             {
#                 "Pdt url": product_page_url,
#                 "UPC": universal_product_code,
#                 "Title": title,
#                 "Price incl VAT": price_including_tax,
#                 "Price excl VAT": price_excluding_tax,
#                 "Nb available": number_available,
#                 "Pdt description": product_description,
#                 "Category": category,
#                 "Review Rating": review_rating,
#                 "Img url": image_url,
#             }
#         )

#     # Find the next page button
#     next_button = soup.find("li", class_="next")
#     if next_button is None:
#         break

#     # Get the URL for the next page
#     next_page_url = urljoin(base_url, next_button.a["href"])
#     next_page_response = requests.get(next_page_url)
#     soup = BeautifulSoup(next_page_response.content, "html.parser")


# # Define fieldnames for CSV header
# fieldnames = [
#     "Pdt url",
#     "UPC",
#     "Title",
#     "Price incl VAT",
#     "Price excl VAT",
#     "Nb available",
#     "Pdt description",
#     "Category",
#     "Review Rating",
#     "Img url",
# ]

# # Specify the directory, filename, and file path for the CSV
# directory = r"C:\Users\johan\Desktop"
# filename = "book_data.csv"
# filepath = os.path.join(directory, filename)

# # Write data to the CSV file
# with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#     writer.writerows(book_data)

# print(f"Data has been successfully saved to {filepath}")

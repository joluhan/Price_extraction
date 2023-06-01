import requests
from bs4 import BeautifulSoup
import csv

# Specify the URL to scrape
category_url = "http://books.toscrape.com/catalogue/category/books/poetry_23/index.html"

# Send a GET request to the URL
category_response = requests.get(category_url)

# Create a BeautifulSoup object to parse the HTML content
category_soup = BeautifulSoup(category_response.content, "html.parser")

# Find the total number of pages in the category
pager = category_soup.find("ul", class_="pager")
last_page_url = (
    pager.find("li", class_="current").find_next_siblings("li").find("a")["href"]
)
total_pages = int(last_page_url.split("/")[-2])

# Create an empty list to store the book URLs
book_urls = []

# Iterate over each page of the category
for page in range(1, total_pages + 1):
    # Construct the URL of the current page
    current_page_url = category_url.replace("index.html", f"page-{page}.html")


# # Extract the desired information
# product_page_url = url
# universal_product_code = soup.find("th", string="UPC").find_next_sibling("td").string
# title = soup.find("h1").string
# price_including_tax = (
#     soup.find("th", string="Price (incl. tax)").find_next_sibling("td").string
# )
# price_excluding_tax = (
#     soup.find("th", string="Price (excl. tax)").find_next_sibling("td").string
# )
# number_available = soup.find("th", string="Availability").find_next_sibling("td").string
# product_description = (
#     soup.find("div", {"id": "product_description"}).find_next("p").string.strip()
# )
# category = soup.find("a", href="../category/books/poetry_23/index.html").string

# review_rating = soup.find("p", class_="star-rating")["class"][1]
# image_url = soup.find("div", {"id": "product_gallery"}).find("img")["src"]

# # Specify the filename and location to save the CSV file
# csv_filename = input("Enter the filename for the CSV file (without extension): ")
# csv_location = input("Enter the location to save the CSV file: ")

# # Prepare the data to write to the CSV file
# data = [
#     [
#         "product_page_url",
#         "universal_product_code",
#         "title",
#         "price_including_tax",
#         "price_excluding_tax",
#         "number_available",
#         "product_description",
#         "category",
#         "review_rating",
#         "image_url",
#     ],
#     [
#         product_page_url,
#         universal_product_code,
#         title,
#         price_including_tax,
#         price_excluding_tax,
#         number_available,
#         product_description,
#         category,
#         review_rating,
#         image_url,
#     ],
# ]

# # Write the data to the CSV file
# with open(f"{csv_location}/{csv_filename}.csv", "w", newline="") as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerows(data)

# # Print the success message
# print(f"Data has been successfully saved to {csv_location}\{csv_filename}.csv.")

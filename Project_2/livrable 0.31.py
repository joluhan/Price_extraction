import requests
from bs4 import BeautifulSoup
import csv
import os
import re
from unicodedata import normalize
from urllib.parse import urljoin


# Function to extract category URL
def category_urls_list(base_url):
    category_urls_list = []  # Create an empty list to store category URLs

    response = requests.get(base_url)  # Send a GET request to the specified URL
    html_content = response.content  # Get the content of the response
    soup = BeautifulSoup(html_content, "html.parser")  # Parse the HTML content

    category_list = soup.find("ul", class_="nav-list")  # Find the category list element
    category_items = category_list.find_all(
        "li"
    )  # Find all list items within the category list

    for index, category_item in enumerate(category_items):
        if index > 0:  # Start appending from the second element
            category_url = urljoin(
                base_url, category_item.find("a")["href"]
            )  # Get the URL of the category item
            category_urls_list.append(
                category_url
            )  # Append the category URL to the list

    return category_urls_list  # Return the list of category URLs


# Function to extract book URLs from each category
def extract_urls(list_urls):
    urls = []

    for url in list_urls:
        response = requests.get(url)  # Send a GET request to the specified URL
        html_content = response.content  # Retrieve the content of the response

        if response.status_code == 200:  # Check if the request was successful
            print(f"Access to {url} successful")
        else:
            print(f"Access to {url} unsuccessful")

        soup = BeautifulSoup(html_content, "html.parser")  # Parse the HTML content

        url_home = response.url  # Get the base URL of the page

        # Find all article elements with the specified class
        articles = soup.find_all("article", class_="product_pod")
        for article in articles:
            href = article.find("h3").find("a")[
                "href"
            ]  # Find the href attribute of the <a> element
            absolute_url = urljoin(
                url_home, href
            )  # Convert relative URL to absolute URL
            urls.append(absolute_url)  # Add the absolute URL to the list of URLs

        next_link = soup.find("li", class_="next")  # Find the next page link
        if next_link is None:
            break  # Exit the loop if there is no next page

        next_page_url = urljoin(
            url_home, next_link.find("a")["href"]
        )  # Get the URL for the next page
        list_urls.append(next_page_url)  # Append the next page URL to the list of URLs

    return urls


# # Function to extract data from a list of URLs
# def extract_data(book_urls):
#     book_data = []  # Initialize an empty list to store book data

#     for url in book_urls:
#         print(f"Processing URL: {url}")
#         response = requests.get(url)  # Send a GET request to the URL
#         html_content = response.content  # Get the content of the response
#         soup = BeautifulSoup(
#             html_content, "html.parser"
#         )  # Create a BeautifulSoup object for parsing HTML

#         # Extract various data from the HTML using BeautifulSoup .find
#         product_page_url = url
#         universal_product_code = (
#             soup.find("table", class_="table-striped").find("td").text
#         )
#         title = soup.find("div", class_="product_main").find("h1").text
#         price_including_tax = (
#             soup.find("th", string="Price (incl. tax)")
#             .find_next_sibling("td")
#             .string.strip("£")
#         )
#         price_excluding_tax = (
#             soup.find("th", string="Price (excl. tax)")
#             .find_next_sibling("td")
#             .string.strip("£")
#         )

#         availability_text = soup.find("p", class_="instock availability").text.strip()
#         match = re.search(
#             r"\d+", availability_text
#         )  # Search for any sequence of digits
#         number_available = match.group() if match else None

#         extracted_text = (
#             soup.find("div", {"id": "product_description"})
#             .find_next("p")
#             .string.strip()
#         )
#         product_description = (
#             normalize("NFKD", extracted_text)
#             .encode("ascii", "ignore")
#             .decode("utf-8")
#             .strip()
#         )

#         category = soup.find("ul", class_="breadcrumb").find_all("a")[2].text
#         review_rating = soup.find("p", class_="star-rating")["class"][1]
#         image_url = urljoin(
#             url, soup.find("div", class_="item active").find("img")["src"]
#         )

#         # Create a dictionary with the extracted data and append it to the book_data list
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

#     return book_data  # Return the list of extracted book data

# ======================================TEST======================================

# ======================================TEST======================================


# Function to save data to a CSV file
def save_data_to_csv(book_data, directory, category):
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
    filename = f"book_data_{category}.csv"  # Create the filename for the category
    filepath = os.path.join(directory, filename)

    with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(book_data)

    print(f"Data has been successfully saved to {filepath}")


# Function that uses functions category_urls_list(), extract_urls(), extract_data(), and save_data_to_csv() to save data to a CSV file for each category
def save_data_to_csv_all_categories(directory):
    base_url = "https://books.toscrape.com/catalogue/page-1.html"
    # Extract URLs
    list_urls = category_urls_list(base_url)

    for category_url in list_urls:
        category_name = category_url.split("/")[
            -2
        ]  # Extract the category name from the URL
        book_urls = extract_urls(
            [category_url]
        )  # Extract URLs for books in the category
        book_data = extract_data(book_urls)  # Extract data for books in the category

        if book_data:
            save_data_to_csv(book_data, directory, category_name)


# Define the directory where the files will be saved
directory = r"C:\Users\johan\Desktop"

# Call the function to save data to CSV files for all categories
save_data_to_csv_all_categories(directory)

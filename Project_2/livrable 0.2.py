# ============================== Étape 2 : Extraire les données d’une catégorie ==============================

import requests
from bs4 import BeautifulSoup
import csv
import os
import re

# import html

# url joining libraries
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
# print(soup.prettify())


# >>>>==========================WORKING============================
# Function ==========> urls extraction
def extract_urls(catalogue_url):
    # Send a GET request to the specified URL
    response = requests.get(catalogue_url)
    # Retrieve the content of the response
    html_content = response.content

    # Parse the HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # Find and extract every URL
    base_url = response.url  # Get the base URL of the page
    urls = []

    # Find all article elements with the specified class
    articles = soup.find_all("article", class_="product_pod")
    for article in articles:
        # Find the href attribute of the nested <a> element
        href = article.find("h3").find("a")["href"]
        absolute_url = urljoin(base_url, href)  # Convert relative URL to absolute URL
        urls.append(absolute_url)  # Add the absolute URL to the list of URLs

    return urls  # Return the list of extracted URLs


# Call the extract_urls function and store the result in the 'result' variable
result = extract_urls(catalogue_url)
# print(result)


# Function ==========> extract data from a list of URLs
def extract_data(result):
    book_data = []  # Initialize an empty list to store book data

    for url in result:  # Iterate over each URL in the input list
        response = requests.get(url)  # Send a GET request to the URL
        html_content = response.content  # Get the content of the response

        # Create a BeautifulSoup object for parsing HTML
        soup = BeautifulSoup(html_content, "html.parser")

        # Extract various data from the HTML using BeautifulSoup .find
        product_page_url = url
        universal_product_code = (
            soup.find("table", class_="table-striped").find("td").text
        )
        title = soup.find("div", class_="product_main").find("h1").text

        price_including_tax = (
            soup.find("th", string="Price (incl. tax)").find_next_sibling("td").string
        ).text.strip("£")
        price_excluding_tax = (
            soup.find("th", string="Price (excl. tax)").find_next_sibling("td").string
        ).text.strip("£")

        # Extract availability text
        availability_text = soup.find("p", class_="instock availability").text.strip()
        # Extract the number from the availability text using regular expressions and string manipulation
        match = re.search(
            r"\d+", availability_text
        )  # Search for any sequence of digits
        if match:
            number_available = match.group()  # Extract the matched digits
        else:
            number_available = None  # Set to None if no match is found

        product_description = (
            soup.find("div", {"id": "product_description"})
            .find_next("p")
            .string.strip()
        )
        # >>>>>>==========================TEST============================

        # ==========================TEST============================<<<<<<<

        category = soup.find("ul", class_="breadcrumb").find_all("a")[2].text
        review_rating = soup.find("p", class_="star-rating")["class"][1]
        image_url = urljoin(
            url, soup.find("div", class_="item active").find("img")["src"]
        )

        # Create a dictionary with the extracted data and append it to the book_data list
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

    return book_data  # Return the list of extracted book data


# Pass the result of extract_urls() to extract_data()
book_data = extract_data(result)


# Function ==========> save data to a CSV file
def save_data_to_csv(book_data, directory, filename):
    # Define the field names for the CSV file
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
    # Create the file path by joining the directory and filename
    filepath = os.path.join(directory, filename)

    # Open the CSV file in write mode with UTF-8 encoding
    with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
        # Create a CSV writer object using the field names
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # Write the header row with the field names
        writer.writeheader()
        # Write the data rows to the CSV file
        writer.writerows(book_data)

    # Print a success message with the file path
    print(f"Data has been successfully saved to {filepath}")


# Define the directory where the file will be saved
directory = r"C:\Users\johan\Desktop"

# Specify the filename for the CSV file
filename = "book_data.csv"

# Call the function to save the book_data to a CSV file in the specified directory
save_data_to_csv(book_data, directory, filename)

# >>>>==========================WORKING============================

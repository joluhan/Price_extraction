# ============================== Étape 2 : Extraire les données d’une catégorie ==============================

import requests
from bs4 import BeautifulSoup
import csv
import os

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
    # Fetch the page content
    response = requests.get(catalogue_url)
    html_content = response.content

    # Parse the HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # Find and extract every URL
    base_url = response.url  # Get the base URL of the page
    urls = []
    articles = soup.find_all("article", class_="product_pod")
    for article in articles:
        href = article.find("h3").find("a")["href"]
        absolute_url = urljoin(base_url, href)  # Convert relative URL to absolute URL
        urls.append(absolute_url)

    return urls


result = extract_urls(catalogue_url)
# print(result)


# Function ==========> data extraction
def extract_data(result):
    book_data = []

    for url in result:
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, "html.parser")

        product_page_url = url
        universal_product_code = (
            soup.find("table", class_="table-striped").find("td").text
        )
        title = soup.find("div", class_="product_main").find("h1").text
        price_including_tax = soup.find("p", class_="price_color").text.strip("£")
        price_excluding_tax = soup.find_all("p", class_="price_color")[1].text.strip(
            "£"
        )
        number_available = soup.find("p", class_="instock availability").text.strip()
        product_description = (
            soup.find("article", class_="product_page")
            .find("p", recursive=False)
            .text.strip()
        )
        category = soup.find("ul", class_="breadcrumb").find_all("a")[2].text
        review_rating = soup.find("p", class_="star-rating")["class"][1]
        image_url = urljoin(
            url, soup.find("div", class_="item active").find("img")["src"]
        )

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

    return book_data


# Pass the result of extract_urls() to extract_data()
book_data = extract_data(result)


# Function ==========> save data to csv file
def save_data_to_csv(book_data, directory, filename):
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
    filepath = os.path.join(directory, filename)

    with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(book_data)

    print(f"Data has been successfully saved to {filepath}")


# >>>>==========================WORKING============================


# >>>>==========================TEST============================

# ==========================TEST============================<<<<<


# Example usage
directory = r"C:\Users\johan\Desktop"
filename = "book_data.csv"
save_data_to_csv(book_data, directory, filename)

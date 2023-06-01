import csv
import requests
from bs4 import BeautifulSoup
import os


def extract_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    product_page_url = url
    universal_product_code = get_element_text(soup, "th", text="UPC")
    title = get_element_text(soup, "h1")
    price_including_tax = get_element_text(
        soup, "th", text="Price (incl. tax)", remove_currency_symbol=True
    )
    price_excluding_tax = get_element_text(
        soup, "th", text="Price (excl. tax)", remove_currency_symbol=True
    )
    number_available = get_element_text(
        soup, "th", text="Availability", split_text=True, index=2
    )
    product_description = get_element_text(
        soup, "article", class_="product_page", child_tag="p"
    )
    category = get_element_text(soup, "ul", class_="breadcrumb", child_tag="a", index=2)
    review_rating = get_element_attribute(
        soup,
        "div",
        class_="col-sm-6 product_main",
        child_tag="p",
        attribute="class",
        attribute_value="star-rating",
        index=1,
    )
    image_url = get_element_attribute(
        soup,
        "div",
        class_="item active",
        child_tag="img",
        attribute="src",
        replace=["../../", "http://books.toscrape.com/"],
    )

    data = {
        "product_page_url": product_page_url,
        "universal_product_code (upc)": universal_product_code,
        "title": title,
        "price_including_tax": price_including_tax,
        "price_excluding_tax": price_excluding_tax,
        "number_available": number_available,
        "product_description": product_description,
        "category": category,
        "review_rating": review_rating,
        "image_url": image_url,
    }

    return data


def get_element_text(
    soup,
    tag,
    text=None,
    class_=None,
    remove_currency_symbol=False,
    split_text=False,
    index=0,
):
    element = soup.find(tag, string=text, class_=class_)
    if element is not None:
        text = element.find_next("td").text
        if remove_currency_symbol:
            text = text[1:]
        if split_text:
            text = text.split()[index]
        return text
    return ""


def get_element_attribute(
    soup,
    tag,
    class_=None,
    child_tag=None,
    attribute=None,
    attribute_value=None,
    replace=None,
    index=0,
):
    element = soup.find(tag, class_=class_)
    if element is not None:
        if child_tag is not None:
            element = element.find(child_tag, {attribute: attribute_value})
        if element is not None:
            attribute_value = element[attribute]
            if replace is not None:
                for old, new in replace:
                    attribute_value = attribute_value.replace(old, new)
            return attribute_value
    return ""


def write_to_csv(data, filename):
    keys = data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)


def main():
    # URL de la page à extraire
    url = "http://example.com"

    # Extraire les données
    data = extract_data(url)

    # Demander le chemin du dossier où enregistrer le fichier CSV
    folder_path = input("Enter the desired folder path: ")

    # Demander un nom pour le fichier
    name_file_result = input("Give a name to the file: ")

    # Définir le nom complet du fichier CSV
    filename = os.path.join(folder_path, name_file_result + ".csv")

    # Vérifier si les données sont présentes
    if all(value for value in data.values()):
        # Écrire les données dans un fichier CSV
        write_to_csv([data], filename)

        # Afficher le message de succès et l'emplacement du fichier
        print(f"Data extraction successful. Saved as {filename}")
        print(f"Location: {os.path.abspath(filename)}")
    else:
        # Afficher un message d'erreur si des données sont manquantes
        print("Error: Some data is missing. Data extraction unsuccessful.")


if __name__ == "__main__":
    main()

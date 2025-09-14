import requests
from bs4 import BeautifulSoup
import pandas as pd


"""
Serviço para web scraping de categorias e livros do site http://books.toscrape.com/
Pegar os dados do site e salvar em arquivos CSV.

"""


def _scrape_website(url):
    """
    Scrape the content of all pages for a given category URL.
    Args:
        url (str): The category URL to scrape.
    Returns:
        list: List of BeautifulSoup objects (one per page).
    """
    soups = []
    next_page = url

    while next_page:
        response = requests.get(next_page)
        if response.status_code != 200:
            raise Exception(f"Erro ao acessar {next_page}, status {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')
        soups.append(soup)

        # procura se existe link "next"
        next_link = soup.select_one("li.next a")
        if next_link:
            # constrói a URL absoluta
            base_url = "/".join(next_page.split("/")[:-1])  # remove o nome do arquivo
            next_page = base_url + "/" + next_link["href"]
        else:
            next_page = None

    return soups


def _scrape_service_get_books(category_name, category_url, tag, class_name):

    """
    Scrape books from a given category URL based on the specified tag and class name.
    Args:
        category_name (str): The name of the category.
        category_url (str): The URL of the category to scrape.
        tag (str): The HTML tag to search for.
        class_name (str): The class name of the HTML elements to search for.
    Returns:
        list: A list of books with their details.
    """

    book_id = 1

    soups = _scrape_website(category_url)

    data = []
    for soup in soups:
        elements = soup.find_all(tag, class_=class_name)

        for element in elements:
            title = element.h3.a.get("title") if element.h3 else None
            price = element.find("p", class_="price_color").get_text(strip=True) if element.find("p", class_="price_color") else None
            stock = element.find("p", class_="instock availability").get_text(strip=True) if element.find("p", class_="instock availability") else None
            image_tag = element.select_one("div a img")
            image_url = image_tag["src"] if image_tag else None

            rating_tag = element.find("p", class_="star-rating")
            rating_number = None
            if rating_tag:
                for cls in rating_tag.get("class", []):
                    if cls != "star-rating":
                        mapping = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
                        rating_number = mapping.get(cls, 0)
                        break

            data.append({
                "id": book_id,
                "title": title,
                "price": price,
                "stock": stock,
                "category": category_name,
                "rating": rating_number,
                "image_url": image_url
            })
            
            book_id += 1

    return data



def scrape_service_get_categories(url):

    """
    Extract categories from the website.
    Args:
        url (str): The URL of the website to scrape.
    Returns:
        list: A list of categories with their names and links.
    """

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Erro ao acessar {url}, status {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    # pega todos os <li> dentro do segundo <ul>
    categories = soup.select("aside .side_categories ul ul li")

    data = []
    for cat in categories:
        name = cat.get_text(strip=True)
        link = cat.a["href"]
        data.append({
            "category": name,
            "link": link
        })

    if data:
        
        print(f"✅ {len(data)} categorias extraídas com sucesso!")
        
        df = pd.DataFrame(data)
        
        df.to_csv("./src/data/categories_data.csv", index=False, encoding="utf-8")
        
        print("✅ Arquivo 'categories_data.csv' salvo com sucesso!")

    return data

    

def scrape_all_books(base_url):
    """
    Scrape all books from all categories on the website.
    Args:
        base_url (str): The base URL of the website to scrape.
    Returns:
        list: A list of all books with their details.
    """

    categories = scrape_service_get_categories(base_url)
    all_books = []

    for cat in categories:
        category_name = cat["category"]
        category_url = base_url.rstrip("/") + "/" + cat["link"]  # garantir URL absoluta

        print(f"Scraping category: {category_name} ({category_url})")

        books = _scrape_service_get_books(
            category_name=category_name,
            category_url=category_url,
            tag="li",
            class_name="col-xs-6 col-sm-4 col-md-3 col-lg-3"
        )
        all_books.extend(books)


    if all_books:
        print(f"✅ {len(all_books)} livros extraídos com sucesso!")
        
        df = pd.DataFrame(all_books)
        
        df.to_csv("./src/data/books_data.csv", index=False, encoding="utf-8")
        
        print("✅ Arquivo 'books_data.csv' salvo com sucesso!")

    

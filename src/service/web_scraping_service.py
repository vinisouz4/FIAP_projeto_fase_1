# src/services/scraping.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
import uuid
import time

from src.log.logs import LoggerHandler


class Scraper:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.logger = LoggerHandler(context="WebScraping")

    def _get_soup_pages(self, url: str):
        """
        Retorna lista de objetos BeautifulSoup para todas as páginas paginadas.
        """
        soups = []
        next_page = url

        while next_page:
            try:
                response = requests.get(next_page, timeout=50)
                response.raise_for_status()
            except requests.RequestException as e:
                self.logger.ERROR(f"Erro ao acessar {next_page}: {e}")
                break

            soup = BeautifulSoup(response.text, "html.parser")
            soups.append(soup)

            next_link = soup.select_one("li.next a")
            if next_link:
                base = "/".join(next_page.split("/")[:-1])
                next_page = f"{base}/{next_link['href']}"
            else:
                next_page = None

            time.sleep(1)  # evita sobrecarregar o servidor

        return soups

    def get_categories(self):
        """
        Extrai categorias do site e salva em CSV.
        """
        try:
            response = requests.get(self.base_url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            self.logger.ERROR(f"Erro ao acessar {self.base_url}: {e}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        categories = soup.select("aside .side_categories ul ul li")

        data = []
        for cat in categories:
            name = cat.get_text(strip=True)
            link = cat.a["href"]
            data.append({"category": name, "link": link})

        if data:
            self.logger.INFO(f"{len(data)} categorias extraídas com sucesso!")
            df = pd.DataFrame(data)
            df.to_csv("./src/data/categories_data.csv", index=False, encoding="utf-8")
            self.logger.INFO("Arquivo 'categories_data.csv' salvo com sucesso!")

        return data

    def get_books_by_category(self, category_name: str, category_url: str):
        """
        Retorna lista de livros de uma categoria específica.
        """
        soups = self._get_soup_pages(category_url)
        books = []

        for soup in soups:
            elements = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
            for element in elements:
                title = element.h3.a.get("title") if element.h3 else None
                price_text = element.find("p", class_="price_color").get_text(strip=True) if element.find("p", class_="price_color") else None
                stock = element.find("p", class_="instock availability").get_text(strip=True) if element.find("p", class_="instock availability") else None
                image_tag = element.select_one("div a img")
                image_url = image_tag["src"] if image_tag else None


                # Converte rating
                rating_tag = element.find("p", class_="star-rating")
                rating_number = None
                if rating_tag:
                    mapping = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
                    rating_number = next((mapping[cls] for cls in rating_tag.get("class", []) if cls in mapping), 0)

                books.append({
                    "id": str(uuid.uuid4()),  # id único global
                    "title": title,
                    "price": price_text,
                    "stock": stock,
                    "category": category_name,
                    "rating": rating_number,
                    "image_url": image_url
                })

        self.logger.INFO(f"{len(books)} livros extraídos da categoria '{category_name}'.")
        return books

    def scrape_all_books(self):
        """
        Scrape todos os livros de todas as categorias e salva em CSV.
        """
        categories = self.get_categories()
        all_books = []

        for cat in categories:
            category_name = cat["category"]
            category_url = f"{self.base_url}/{cat['link']}"

            self.logger.INFO(f"Iniciando scraping da categoria: {category_name}")
            books = self.get_books_by_category(category_name, category_url)
            all_books.extend(books)

        if all_books:
            self.logger.INFO(f"{len(all_books)} livros extraídos no total.")
            df = pd.DataFrame(all_books)
            df.to_csv("./src/data/books_data.csv", index=False, encoding="latin1")
            self.logger.INFO("Arquivo 'books_data.csv' salvo com sucesso!")

        return all_books

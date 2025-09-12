import requests
from bs4 import BeautifulSoup



def _scrape_website(url, pages=1):
    
    """
    Scrape the content of a website and return the parsed HTML.
    Args:
        url (str): The URL of the website to scrape.
        pages (int): The number of pages to scrape.
    Returns:
        BeautifulSoup: Parsed HTML content of the website."""
    
    
    for n_pages in range(1, pages + 1):
        print(f"Scraping page {n_pages} of {pages}...")

    
    response = requests.get(url)
    
    if response.status_code == 200:

        html = response.text

        soup = BeautifulSoup(html, 'html.parser')
        return soup
    
    else:
        raise Exception(f"Failed to retrieve content from {url}, status code: {response.status_code}")


def scrape_service(url, tag, class_name, pages=1):
    """
    Extract data from the parsed HTML based on the specified tag and class name.
    Args:
        url (str): The URL of the website to scrape.
        tag (str): The HTML tag to search for.
        class_name (str): The class name of the HTML elements to search for.
    Returns:
        list: A list of extracted data strings.
    """

    soup = _scrape_website(url)

    elements = soup.find_all(tag, class_=class_name)
    
    data = []
    for element in elements:
        # Aqui você escolhe o que quer puxar
        title = element.h3.a.get("title") if element.h3 else None
        price = element.find("p", class_="price_color").get_text(strip=True) if element.find("p", class_="price_color") else None
        stock = element.find("p", class_="instock availability").get_text(strip=True) if element.find("p", class_="instock availability") else None


        data.append({
            "title": title,
            "price": price,
            "stock": stock
        })
    
    
    return data

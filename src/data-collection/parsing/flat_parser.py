from bs4 import BeautifulSoup

# load the html content
with open("test.html", "r") as file:
    html = file.read()

def get_price(soup: BeautifulSoup) -> str:
    """Get the price from the soup."""
    price = soup.find("span", class_="price-eur").get_text(strip=True)
    return price

def get_address(soup: BeautifulSoup) -> str:
    """Get the address from the soup."""
    address = soup.find("h1", class_="obj-header-text").get_text(strip=True)
    return address

def get_info_table(soup: BeautifulSoup) -> dict:
    """Get the info table from the soup."""
    dt_tags = soup.find_all('dt')
    dd_tags = soup.find_all('dd')

    table = {}

    for dt, dd in zip(dt_tags, dd_tags):
        description = dt.get_text(strip=True)
        value = dd.get_text(strip=True)
        table[description] = value

    return table

def get_description(soup: BeautifulSoup) -> str:
    """Get the description from the soup."""
    description = soup.find('div', id='collapsedText')
    return description
from bs4 import BeautifulSoup
from typing import List
import re

def get_ids(html: str) -> List[str]:
    soup = BeautifulSoup(html, 'html.parser')
    href_tags = soup.find_all(href=True)   
    hrefs = [tag["href"] for tag in href_tags]
    pattern = r"[0-9]-[0-9][0-9][0-9][0-9][0-9][0-9][0-9]"
    ids = [re.search(pattern, href).group(0) for href in hrefs if re.search(pattern, href)]
    ids = list(set(ids))
    return ids

def get_max_page(html: str) -> int:
    soup = BeautifulSoup(html, 'html.parser')
    hrefs = [a['href'] for a in soup.find_all('a', href=True)]
    pattern = r"/butai/puslapis/(\d+)/"
    max_page = max([int(re.search(pattern, href).group(1)) for href in hrefs if re.search(pattern, href)])
    return max_page
import re
from typing import List, Tuple

from bs4 import BeautifulSoup


def process_stats_row(
    row_soup: BeautifulSoup, strip_names: bool = True,
) -> Tuple[List[str], List[str]]:
    names = row_soup.find_all('td', class_='stat-col-second')
    values = row_soup.find_all('b')
    names = [name.get_text(strip=strip_names) for name in names]
    values = [value.get_text(strip=True) for value in values]
    return names, values


def extract_buses_from_names(names: List[str]) -> List[str]:
    return re.findall(r'\s{3,}(\d+)\s{3,}', names)


def extract_bus_stops_from_names(names: List[str]) -> str:
    return re.findall(r'\n(.*?)\n', names)[0]

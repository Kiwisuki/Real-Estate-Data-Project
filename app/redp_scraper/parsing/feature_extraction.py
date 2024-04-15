from typing import List, Tuple
import logging

from bs4 import BeautifulSoup
from redp_scraper.parsing.helpers import (
    extract_bus_stops_from_names,
    extract_buses_from_names,
    process_stats_row,
)
from redp_scraper.utils import exception_handler

LOGGER = logging.getLogger(__name__)

@exception_handler(LOGGER)
def get_price(soup: BeautifulSoup) -> str:
    """Get the price from the soup."""
    price = soup.find('span', class_='price-eur').get_text(strip=True)
    return price

@exception_handler(LOGGER)
def get_address(soup: BeautifulSoup) -> str:
    """Get the address from the soup."""
    address = soup.find('h1', class_='obj-header-text').get_text(strip=True)
    return address

@exception_handler(LOGGER)
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

@exception_handler(LOGGER)
def get_description(soup: BeautifulSoup) -> str:
    """Get the description from the soup."""
    description = soup.find('div', id='collapsedText').get_text(strip=False)
    return description

@exception_handler(LOGGER, expected_message='Accurate coordinates not found')
def get_coordinates(soup: BeautifulSoup) -> str:
    return soup.find('a', class_='link-obj-thumb vector-thumb-directions')[
        'href'
    ].split('=')[-1]

@exception_handler(LOGGER)
def get_inaccurate_coordinates(soup: BeautifulSoup) -> List[str]:
    return (
        soup.find('a', class_='link-obj-thumb vector-thumb-map')['href']
        .split('=')[-1]
        .split('%2C')
    )

@exception_handler(LOGGER)
def get_bus_info(soup: BeautifulSoup) -> Tuple[List[str], List[str], List[str]]:
    stats = soup.find_all('div', class_='statistic-info-row')
    bus = next(stat for stat in stats if '-bus-' in str(stat))
    names, values = process_stats_row(bus, False)
    buses = [extract_buses_from_names(name) for name in names]
    stops = [extract_bus_stops_from_names(name) for name in names]
    distances = list(values)
    return buses, stops, distances

@exception_handler(LOGGER)
def get_store_info(soup) -> Tuple[List[str], List[str]]:
    stats = soup.find_all('div', class_='statistic-info-row')
    store = next(stat for stat in stats if '-store-' in str(stat))
    return process_stats_row(store)

@exception_handler(LOGGER)
def get_school_info(soup: BeautifulSoup) -> Tuple[List[str], List[str]]:
    stats = soup.find_all('div', class_='statistic-info-row')
    school = next(stat for stat in stats if '-school-' in str(stat))
    return process_stats_row(school)

@exception_handler(LOGGER)
def get_kinder_info(soup: BeautifulSoup) -> Tuple[List[str], List[str]]:
    stats = soup.find_all('div', class_='statistic-info-row')
    kinder = next(stat for stat in stats if '-kinder-' in str(stat))
    return process_stats_row(kinder)

@exception_handler(LOGGER)
def get_images(soup: BeautifulSoup) -> List[str]:
    obj_thumbs = soup.find_all('img', class_='obj-thumb')
    return [img['data-full'] for img in obj_thumbs if img.has_attr('data-full')]

@exception_handler(LOGGER)
def get_id(soup: BeautifulSoup) -> str:
    try:
        info_table = get_info_table(soup)
        return info_table['Nuoroda'].split('/')[-1]
    except KeyError:
        
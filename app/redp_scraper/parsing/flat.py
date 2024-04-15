from bs4 import BeautifulSoup
from redp_scraper.parsing.feature_extraction import (
    get_address,
    get_bus_info,
    get_coordinates,
    get_description,
    get_inaccurate_coordinates,
    get_info_table,
    get_kinder_info,
    get_price,
    get_school_info,
    get_store_info,
    get_images,
    get_id
)


class FlatParser:
    def __init__(self, html: str):
        self.html = html
        self.soup = BeautifulSoup(html, 'html.parser')
        self._parse_flat_details()

    def _parse_flat_details(self):
        self.price = get_price(self.soup)
        self.address = get_address(self.soup)
        self.info_table = get_info_table(self.soup)
        self.description = get_description(self.soup)
        self.coordinates = get_coordinates(self.soup)
        self.inaccurate_coordinates = get_inaccurate_coordinates(self.soup)
        self.buses, self.bus_stops, self.bus_distances = get_bus_info(self.soup)
        self.stores, self.store_distances = get_store_info(self.soup)
        self.schools, self.school_distances = get_school_info(self.soup)
        self.kinders, self.kinder_distances = get_kinder_info(self.soup)
        self.images = get_images(self.soup)
        self.aruodas_id = get_id(self.soup)

    def to_dict(self):
        return {
            'price': self.price,
            'address': self.address,
            'info_table': self.info_table,
            'description': self.description,
            'coordinates': self.coordinates,
            'inaccurate_coordinates': self.inaccurate_coordinates,
            'buses': self.buses,
            'bus_stops': self.bus_stops,
            'bus_distances': self.bus_distances,
            'stores': self.stores,
            'store_distances': self.store_distances,
            'schools': self.schools,
            'school_distances': self.school_distances,
            'kinders': self.kinders,
            'kinder_distances': self.kinder_distances,
            'images': self.images,
            'aruodas_id': self.aruodas_id,
        }

from redp_scraper.scraping.driver import SmartDriver
from redp_scraper.parsing.flat import FlatParser
from redp_scraper.scraping.mongo import upload_dict, get_scraped_ids
from redp_scraper.parsing.listings import get_ids, get_max_page
from redp_scraper.utils import set_logger_config
from time import sleep

import logging

LOGGER = logging.getLogger(__name__)
BASE_URL = 'https://www.aruodas.lt/butai/puslapis/{page}/?FOrder=AddDate'
BASE_AD_URL = 'https://www.aruodas.lt/{_id}'

set_logger_config()

def main():
    driver = SmartDriver(
        refresh_rate=10,
        refresh_timer=60*10,
        wait_to_load=10,
    )
    base_html = driver.get_html(BASE_URL.format(page=1))
    max_page = get_max_page(base_html)
    #scraped_ids = get_scraped_ids()
    LOGGER.info(f'Max page: {max_page}')
    for page in range(1, max_page+1):
        listing_html = driver.get_html(BASE_URL.format(page=page))
        ids = get_ids(listing_html)
        LOGGER.info(f'Found following ids: {ids}')
        # save html to file
        with open(f'listings.html', 'w') as f:
            f.write(listing_html)
        #ids = [_id for _id in ids if _id not in scraped_ids]
        for _id in ids:
            link = BASE_AD_URL.format(_id=_id)
            html = driver.get_html(link)
            flat = FlatParser(html)
            data_dict = flat.to_dict()
            if data_dict:
                upload_dict(data_dict)
                LOGGER.info(f'Uploaded data from {link}')
                #scraped_ids.add(data_dict['id'])
            else:
                LOGGER.error(f'Failed to parse data from {link}')
        LOGGER.info(f'Finished page {page}')
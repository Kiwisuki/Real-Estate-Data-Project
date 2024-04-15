from pymongo import MongoClient
from pymongo.server_api import ServerApi
from redp_scraper.settings import MongoSettings
from typing import List

DEFAULT_SETTINGS = MongoSettings()


def upload_dict(
    data_dict: dict,
    uri: str = DEFAULT_SETTINGS.uri,
    database_name=DEFAULT_SETTINGS.database_name,
    collection_name: str = DEFAULT_SETTINGS.collection_name,
) -> None:
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client[database_name]
    collection = db[collection_name]
    collection.insert_one(data_dict)

def get_scraped_ids(
    uri: str = DEFAULT_SETTINGS.uri,
    database_name=DEFAULT_SETTINGS.database_name,
    collection_name: str = DEFAULT_SETTINGS.collection_name,
) -> List[str]:
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client[database_name]
    collection = db[collection_name]
    aruodas_ids = collection.distinct('aruodas_id')
    return aruodas_ids
import os
from dataclasses import dataclass


@dataclass
class MongoSettings:
    uri: str = os.environ['MONGODB_URI']
    database_name: str = 'Scraping'
    collection_name: str = 'aruodas/butai'

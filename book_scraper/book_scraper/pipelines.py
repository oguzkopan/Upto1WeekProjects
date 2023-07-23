# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
import sys
from .items import BookScraperItem

class BookScraperPipeline:

    def __init__(self, mongodb_uri, mongodb_db, collection_name):
        self.mongodb_uri = mongodb_uri
        self.mongodb_db = mongodb_db
        self.collection_name = collection_name
        if not self.mongodb_uri: sys.exit("You need to provide a Connection String.")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongodb_uri=crawler.settings.get('MONGODB_URI'),
            mongodb_db=crawler.settings.get('MONGODB_DATABASE', 'items'),
            collection_name=crawler.spider.collection_name
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongodb_uri)
        self.db = self.client[self.mongodb_db]
        # Start with a clean database
        self.db[self.collection_name].delete_many({})

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # Remove newline character and replace it with a space in the price
        item['price'] = item['price'].replace('\n', ' ')
        collection = self.db[self.collection_name]
        collection.insert_one(dict(item))
        return item
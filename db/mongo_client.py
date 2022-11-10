import asyncio
import aiofiles
import pymongo
import os
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv()


# In MongoDB, use GridFS for storing files larger than 16 MB.
# You may use the BinData data type to store the binary data

class Database(object):
    URI = os.environ.get("DB_URI")
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client.get_default_database()

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection, query, data):
        Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def remove(collection, query):
        return Database.DATABASE[collection].remove(query)


async def download(out_file_path, contents):
    async with aiofiles.open(out_file_path, 'wb') as out_file:
        await out_file.write(contents)


if __name__ == "__main__":
    Database.initialize()
    collection = Database.DATABASE[os.environ.get('DB_COLLECTION_CREDENTIALS')]
    rst = collection.find({"_id": ObjectId("62cf6638be6b14afb2bc6042")})
    content = rst[0]['data']
    asyncio.run(download("../download/20210825155000_download.pdf", content))
    # 20210825162910.pdf
    # rst = collection.find({"filename": "2008.00364.pdf"})
    # print(rst)62cb6f83a78f112d1be55e56

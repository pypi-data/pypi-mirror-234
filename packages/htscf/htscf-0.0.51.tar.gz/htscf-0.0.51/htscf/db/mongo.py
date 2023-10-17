from pymongo import MongoClient
from pymongo.collection import Collection


def connect(dbName, collectionName, host="0.0.0.0", port=27017, ) -> Collection:
    client = MongoClient(host=host, port=port)
    db = client[dbName]
    return db[collectionName]
from pathlib import Path
from typing import Union

from pymongo import MongoClient


def create(_id, program, script, settings: Union[dict, str], dbName, collectionName, host, port):
    client = MongoClient(host=host, port=port)
    db = client[dbName]
    collection = db[collectionName]
    return collection.insert_one({
        "_id": _id,
        "program": program,
        "script": script,
        "settings": settings
    })


if __name__ == '__main__':
    res = create("6",
                 "python",
                 Path("stepScript.py").read_text(),
                 settings={
                     "a": 10
                 },
                 dbName="test",
                 collectionName="steps",
                 host="42.244.24.75",
                 port=27000
                 )
    print(res)

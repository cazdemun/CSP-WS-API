
from monads.either import Right, Left, Either
from monads.task import Task
from monads.utils import fromNullableTag, tryCatchTag, prop
from toolz import curry

from pymonad import List

from pymongo import MongoClient
from bson import BSON, Binary
from bson.objectid import ObjectId

import time

client = MongoClient("mongodb+srv://charles:rTjQgVHm61X5GS8R@tesiscluster-tfsop.mongodb.net/test?retryWrites=true&w=majority")
print(" * db connection successful")
# print(client.list_database_names())
# print(client['TesisDB'].list_collection_names())


db = client['TesisDB']
tareas_collection = client['TesisDB']['tareas']


def find_one(collection, query):
    """
    f:: Collection, Query -> Either[str Error, Doc]
    """
    return tryCatchTag(f'Error: collection {collection} not found!', lambda: db[collection].find_one(query)) \
        .bind(lambda doc: fromNullableTag(f'Error: query {query} in {collection} not found!', doc))

@curry
def get_id(collection, name):
    """
    f :: str, str -> Either[str Error, str Id]
    We assumed this is for docs who have a 'name' field
    """
    return find_one(collection, {"name": name}) \
        .bind(prop('_id'))

def insert_one(collection, doc):
    """
    f :: Collection, Doc -> Task[Either[str Error, str Id]]
    """
    return Task(lambda rej, res: \
        res(tryCatchTag("Error: on inserting document", lambda: str(collection.insert_one(doc).inserted_id) + f' succesfully added!' )))

def save_task(userid: str= '5eada9b16d6559317acacf07', protocolid: str= '5eada98a6d6559317acacf05', movementid: str ='5eaeee353a5a3656fbda4ff5'):
    """
    f :: str Id, str Id, str Id -> Task[Either[str Error, str Id]]
    """
    # time.sleep(3)
    f = open("cortex/data/charls_1_1573323536.201569_raw.fif","rb")
    f_bson = f.read()
    timestamp = 1573597702

    tarea_doc = {
        "protocol": ObjectId(userid),
        "user": ObjectId(protocolid),
        "movement": ObjectId(movementid),
        "binary_data": Binary(f_bson),
        "timestamp": timestamp
    }

    return insert_one(tareas_collection, tarea_doc)



from monads.either import Right, Left, Either
from monads.task import Task
from monads.utils import tryCatch, trace, eitherToTask

from pymonad import List

from pymongo import MongoClient
from bson import BSON, Binary
from bson.objectid import ObjectId

import time

client = MongoClient("mongodb+srv://charles:rTjQgVHm61X5GS8R@tesiscluster-tfsop.mongodb.net/test?retryWrites=true&w=majority")
print("db connection successful")
# print(client.list_database_names())
# print(client['TesisDB'].list_collection_names())

# usuarios_collection = client['TesisDB']['usuarios']
# protocolos_collection = client['TesisDB']['protocolos']
db = client['TesisDB']
tareas_collection = client['TesisDB']['tareas']


def get_id(collection, name): # should be a Task/Either
    try:
        return db[collection].find_one({"name": name})['_id']
    except:
        return name

# f :: Obj, Obj -> Task[Either[str Error, str Id]]
def insert_doc(collection, doc):
    return Task(lambda rej, res: \
        res(tryCatch(lambda: str(collection.insert_one(doc).inserted_id) + 'succesfully added!' )))
            # .fold(lambda e: rej(trace(e)), lambda id: res(trace(f'{id} succesfully added!'))))

# f :: Obj, Obj -> Task[Either[str Error, str Id]]
def save_task(userid: str= '5eada9b16d6559317acacf07', protocolid: str= '5eada98a6d6559317acacf05', movement: str ='right') -> Task: #[Either[str, str]]

    time.sleep(3)
    f = open("cortex/data/charls_1_1573323536.201569_raw.fif","rb")
    f_bson = f.read()
    timestamp = 1573597702

    user_id = get_id('usuarios', userid)
    protocol_id = get_id('protocolos', protocolid)
    movement = get_id('movimientos', movement)

    tarea_doc = {
        "protocol": ObjectId(user_id),
        "user": ObjectId(protocol_id),
        "binary_data": Binary(f_bson),
        "timestamp": timestamp,
        "movement": movement
    }

    # tarea_id = tareas_collection.insert_one(tarea_obj).inserted_id

    return insert_doc(tareas_collection, tarea_doc)
            #.fork(lambda e: f'error saving document: {e}', lambda id: f'{id} succesfully added!')

    # return Task(lambda rej, res:
    #             res(Right(f'task {tarea_id} succesfully added!') if userid == 'cazdemun' else Left('error on the database!')))



from pymongo import MongoClient

# conda install -c anaconda pymongo
# pip3 install pymongo[srv]

# databases and collections lazy evaluation

# Cluster
client = MongoClient("mongodb+srv://charles:rTjQgVHm61X5GS8R@tesiscluster-tfsop.mongodb.net/test?retryWrites=true&w=majority")

print("i like types")
print(client.list_database_names())
print(client['TesisDB'].list_collection_names())

db = client["TesisDB"]

from bson import BSON, Binary
from bson.objectid import ObjectId 

f = open("cortex/data/charls_1_1573323536.201569_raw.fif","rb")
f_bson = f.read()
# f_bson = BSON.encode() #not

archivos = db['archivos']
# file_id = archivos.insert_one({
#   "binary_data": Binary(f_bson)
# }).inserted_id
# print(file_id)

import pprint

#pprint.pprint(archivos.find_one({"_id": ObjectId("5ea20ad86f4926474326bd32")}))

raw_from_db = archivos.find_one({"_id": ObjectId("5ea20ad86f4926474326bd32")})
raw_from_db = raw_from_db["binary_data"]

import mne
import matplotlib.pyplot as plt

raw_from_file = mne.io.read_raw_fif("cortex/data/charls_1_1573323536.201569_raw.fif")
# raw_from_file.plot()
# plt.show()

import io

raw_from_file = mne.io.read_raw_fif(io.BytesIO(raw_from_db),preload=True)
# raw_from_file.plot()
# plt.show()

print(
  Identity(1)
  .map(lambda x : x + 1)
  .fold(lambda x : x + 1)
)



from monads.task import Task
from dotenv import load_dotenv
import os

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import pprint

load_dotenv()

#set up mongo connection and navigate to collection
uri = os.getenv('MONGO_CONNECTION_STRING')

# Create a client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# List db names
db_names = client.list_database_names()
#print(db_names)

# List collection Names
collections = db.list_collection_names()
#print(collections)

# Navigate to sample_geospatial database
db = client['sample_geospatial']

# Navigate to shipwrecks collection
wrecks = db.shipwrecks

pprint.pprint(wrecks.find_one())

wat = 'always dry'
for wreck in wrecks.find({'watlev': {'$eq': wat}}):
    pprint.pprint(wreck)
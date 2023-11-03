#! /bin/python
# vector_search.py
# use ollama embedding to 

import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load .env file
load_dotenv()

MONGODB_ATLAS_CLUSTER_URI = os.getenv('MONGO_CONNECTION_STRING')

# initialize MongoDB python client
client = MongoClient(MONGODB_ATLAS_CLUSTER_URI)

DB_NAME = "langchain_db"
COLLECTION_NAME = "test"
ATLAS_VECTOR_SEARCH_INDEX_NAME = "gettysburg"

MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]

print(MONGODB_COLLECTION.index_information())
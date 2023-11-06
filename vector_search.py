#! /bin/python
# vector_search.py
# use ollama embedding to 

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import MongoDBAtlasVectorSearch

# Load .env file
load_dotenv()

MONGODB_ATLAS_CLUSTER_URI = os.getenv('MONGO_CONNECTION_STRING')

# initialize MongoDB python client
client = MongoClient(MONGODB_ATLAS_CLUSTER_URI)

DB_NAME = "langchain_db"
COLLECTION_NAME = "test"
ATLAS_VECTOR_SEARCH_INDEX_NAME = "default"

MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]

vector_search = MongoDBAtlasVectorSearch.from_connection_string(
    MONGODB_ATLAS_CLUSTER_URI,
    DB_NAME + "." + COLLECTION_NAME,
    OllamaEmbeddings(),
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
)

query = "How many years ago?"

results = vector_search.similarity_search_with_score(
    query=query,
    k=5,
)

# Display results
for result in results:
    print(result)
#! /bin/python
# embed_and_insert.py
# break up text, create embeddings, and upload to mongodb

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
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

# Load Data
loader = TextLoader('./gettysburg.txt')
data = loader.load()

# Split text
text_splitter = RecursiveCharacterTextSplitter(chunk_size=50, 
                                               chunk_overlap=10
                                              )
docs = text_splitter.split_documents(data)

print(len(docs))
print(docs[0])

# insert the documents in MongoDB Atlas with their embedding
# len llama2 = 4095
# len orca-mini = 3199 
"""
vector_search = MongoDBAtlasVectorSearch.from_documents(
    documents=docs,
    embedding=OllamaEmbeddings(model='orca-mini'),
    collection=MONGODB_COLLECTION,
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
)

#String for creating mongo index
"""

"""
{
  "mappings": {
    "dynamic": true,
    "fields": {
      "embedding": {
        "dimensions": 1536,
        "similarity": "cosine",
        "type": "knnVector"
      }
    }
  }
}
"""
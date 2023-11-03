# Adapted from https://python.langchain.com/docs/integrations/vectorstores/mongodb_atlas

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import MongoDBAtlasVectorSearch
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOllama
from langchain.llms import Ollama

# Load .env file
load_dotenv()

MONGODB_ATLAS_CLUSTER_URI = os.getenv('MONGO_CONNECTION_STRING')

# initialize MongoDB python client
client = MongoClient(MONGODB_ATLAS_CLUSTER_URI)

DB_NAME = "langchain_db"
COLLECTION_NAME = "test"
ATLAS_VECTOR_SEARCH_INDEX_NAME = "gettysburg"

MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]

# # Load Data
# loader = TextLoader('./gettysburg.txt')
# data = loader.load()

# # Split text
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
# docs = text_splitter.split_documents(data)

# # insert the documents in MongoDB Atlas with their embedding
# vector_search = MongoDBAtlasVectorSearch.from_documents(
#     documents=docs,
#     embedding=OllamaEmbeddings(),
#     collection=MONGODB_COLLECTION,
#     index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
# ) 
# Querying data
vector_search = MongoDBAtlasVectorSearch.from_connection_string(
    MONGODB_ATLAS_CLUSTER_URI,
    DB_NAME + "." + COLLECTION_NAME,
    OllamaEmbeddings(),
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
)

#Simple Similarity Search
print('Simple Similarity Search')
query = "What are we engaged in ?"
results = vector_search.similarity_search(query)

#print(results[0].page_content)
print(results)

#Similarity Search with score
print('Similarity Search with score')
query = "What are we engaged in ?"
results = vector_search.similarity_search(query)

results = vector_search.similarity_search_with_score(
    query=query,
    k=5,
)

# Display results
for result in results:
    print(result)

#Question Answering
print('Question Answering')
qa_retriever = vector_search.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 100, "post_filter_pipeline": [{"$limit": 25}]},
)

prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
"""

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

qa = RetrievalQA.from_chain_type(
    llm=Ollama(model='llama2'),
    chain_type="stuff",
    retriever=qa_retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT},
)

docs = qa({"query": "What are we engaged in"})

print(docs["result"])
print(docs["source_documents"])
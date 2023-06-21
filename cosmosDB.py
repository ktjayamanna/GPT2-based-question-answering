from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

connection_string = os.getenv("COSMOS_CONNECTION_STRING")

client = MongoClient(connection_string)

database_name = "SampleDB"
collection_name = "SampleCollection"
document_id = "64919660eac15917a079ef27"

database = client[database_name]
collection = database[collection_name]
document = collection.find_one({"id": 'B6591222-0FB9-415F-8F2B-18B56A483AA1'})
print(document)

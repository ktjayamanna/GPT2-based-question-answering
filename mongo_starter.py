from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os
import json
load_dotenv(find_dotenv())

client = MongoClient(os.getenv('MONGO_CONNECTION_STRING'))
db = client['patient-qna']
collection = db['qna-pairs']

data_path = './data'
qa_data = []

for filename in os.listdir(data_path):
    if filename.endswith('.json'):
        with open(os.path.join(data_path, filename), 'r') as f:
            qa_data.append(json.load(f))
result = collection.insert_many(qa_data)

print('Inserted IDs:', result.inserted_ids)

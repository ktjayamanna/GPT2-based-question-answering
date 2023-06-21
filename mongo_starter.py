from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os
import json
from tqdm import tqdm

load_dotenv(find_dotenv())

client = MongoClient(os.getenv('MONGO_CONNECTION_STRING'))
db = client['patient-qna']
collection = db['qna-pairs']

data_path = './data'
qa_data = []

for filename in tqdm(os.listdir(data_path, desc='loading data into the memory')):
    if filename.endswith('.json'):
        with open(os.path.join(data_path, filename), 'r') as f:
            qa_data.append(json.load(f))
result = collection.insert_many(qa_data)

print('Inserted IDs:', result.inserted_ids)

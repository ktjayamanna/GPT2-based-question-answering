from dotenv import load_dotenv, find_dotenv
import os
import pinecone
import json
import torch
from transformers import GPT2Model, GPT2Tokenizer

load_dotenv(find_dotenv())
pinecone_api_key = os.getenv('PINECONE_API_KEY')

data_path = './data'
qa_data = []

for filename in os.listdir(data_path):
    if filename.endswith('.json'):
        with open(os.path.join(data_path, filename), 'r') as f:
            qa_data.append(json.load(f))


tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2Model.from_pretrained('gpt2')
model.eval() 

pinecone.init(api_key=pinecone_api_key, environment="us-west1-gcp-free")
index_name = "patient-records"
pinecone_index = pinecone.Index(index_name=index_name)

for qa in qa_data:
    inputs = tokenizer(qa['Question'], return_tensors='pt')
    with torch.no_grad():
        outputs = model(**inputs)

    question_embedding = outputs.last_hidden_state.mean(dim=1).tolist()

    pinecone_index.upsert(
        vectors=[{'id':qa['ID'],
                  'values': question_embedding[0]}])

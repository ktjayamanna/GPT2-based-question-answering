from dotenv import load_dotenv, find_dotenv
import os
import pinecone
import json
import torch
from transformers import GPT2Model, GPT2Tokenizer
from tqdm import tqdm

load_dotenv(find_dotenv())
pinecone_api_key = os.getenv('PINECONE_API_KEY')

data_path = './data'
qa_data = []
for filename in tqdm(os.listdir(data_path), desc='loading data into the memory'):
    if filename.endswith('.json'):
        with open(os.path.join(data_path, filename), 'r') as f:
            qa_data.append(json.load(f))

#load the model and the tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2Model.from_pretrained('gpt2')
model.eval() 

#Initialize pinecone
pinecone.init(api_key=pinecone_api_key, environment="us-west1-gcp-free")
index_name = "patient-records"
pinecone_index = pinecone.Index(index_name=index_name)

for qa in tqdm(qa_data, desc='generating and upserting embeddings...'):
    inputs = tokenizer(qa['Question'], return_tensors='pt')
    with torch.no_grad():
        outputs = model(**inputs)
    question_embedding = outputs.last_hidden_state.mean(dim=1).tolist()

    pinecone_index.upsert(
        vectors=[{'id':qa['ID'],
                  'values': question_embedding[0]}])

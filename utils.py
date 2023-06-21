import os
import pinecone
import torch
from transformers import GPT2Model, GPT2Tokenizer
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def get_relevant_answer_from_pinecone(user_input):
    """
    Retrieves the most relevant answer from Pinecone index based on the user input.

    Args:
        user_input (str): The user input to be used for searching relevant answer.

    Returns:
        list: A list containing the most relevant answer from Pinecone index if found else None.
    """
    load_dotenv(find_dotenv())
    pinecone_api_key = os.getenv('PINECONE_API_KEY')

    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    model = GPT2Model.from_pretrained('gpt2')
    model.eval()

    pinecone.init(api_key=pinecone_api_key, environment="us-west1-gcp-free")
    index_name = "patient-records"
    pinecone_index = pinecone.Index(index_name=index_name)
    inputs = tokenizer(user_input, return_tensors='pt')

    with torch.no_grad():
        outputs = model(**inputs)

    user_input_embedding = outputs.last_hidden_state.mean(dim=1).tolist()

    query_results = pinecone_index.query(vector=user_input_embedding[0], top_k=1)
    if query_results:
        return query_results
    else:
        return None


def get_qna_by_id_from_mongodb(id):
    """
    Retrieves a single question-answer pair from the MongoDB collection 'qna-pairs'
    based on the provided ID.

    Args:
        id (str): The ID of the question-answer pair to retrieve.

    Returns:
        str: The answer associated with the provided ID.
    """
    client = MongoClient(os.getenv('MONGO_CONNECTION_STRING'))
    db = client['patient-qna']
    collection = db['qna-pairs']
    result = collection.find_one({'ID': id})

    return result['Answer']
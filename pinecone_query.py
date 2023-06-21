
from utils import get_qna_by_id_from_mongodb, get_relevant_answer_from_pinecone

print("Question 1: What if I have COVID-19?\n")
answer_id = get_relevant_answer_from_pinecone("What if I have COVID-19?")['matches'][0]['id']
answer = get_qna_by_id_from_mongodb(answer_id)
print(answer, "\n")

print("Question 2: what happens if you combine aspirin and ibuprofen?\n")
answer_id = get_relevant_answer_from_pinecone(" what happens if you combine aspirin and ibuprofen?")['matches'][0]['id']
answer = get_qna_by_id_from_mongodb(answer_id)
print(answer, "\n")

print("Question 3: I went out yesterday and tested positive for covid\n")
answer_id = get_relevant_answer_from_pinecone("I went out yesterday and tested positive for covid")['matches'][0]['id']
answer = get_qna_by_id_from_mongodb(answer_id)
print(answer, "\n")

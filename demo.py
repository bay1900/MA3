from mistralai import Mistral
import requests
import numpy as np
import faiss
from pathlib import Path
from getpass import getpass
from dotenv import load_dotenv
from helper import get_env

# GET API KEY
MISTRAL_API_KEY =  get_env.retreive_value( "MISTRAL_API_KE")


#CALL AI SERVICE
client = Mistral( api_key = MISTRAL_API_KEY )

# BASE KNOWLEDGE
response = requests.get('https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/paul_graham/paul_graham_essay.txt')
text = response.text

f = open('essay.txt', 'w')
f.write(text)
f.close()

# SPLIT TEXT INTO CHUNK
chunk_size = 2048
chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
chuck_size = len(chunks)


# EMBEDED TO VECTOR
def get_text_embedding(input):
    embeddings_batch_response = client.embeddings.create(
          model="mistral-embed",
          inputs=input
      )
    return embeddings_batch_response.data[0].embedding

text_embeddings = np.array([get_text_embedding(chunk) for chunk in chunks])

# LOAD EMBEDED DATA INTO VECTOR DATABASE
d = text_embeddings.shape[1]
index = faiss.IndexFlatL2(d)
index.add(text_embeddings)


question = "What were the two main things the author worked on before college?"  # QUESTION 
question_embeddings = np.array([get_text_embedding(question)])                   # EMBEDED THE QUESTION


D, I = index.search(question_embeddings, k=2) # distance, index
retrieved_chunk = [chunks[i] for i in I.tolist()[0]]

prompt = f"""
Context information is below.
---------------------
{retrieved_chunk}
---------------------
Given the context information and not prior knowledge, answer the query.
Query: {question}
Answer:
"""



def run_mistral(user_message, model="mistral-large-latest"):
    print ( "try to run mistral")
    messages = [
        {
            "role": "user", 
            "content": user_message
        }
    ]
    chat_response = client.chat.complete(
        model=model,
        messages=messages
    )
    return (chat_response.choices[0].message.content)

test = run_mistral(prompt)

print ( test )
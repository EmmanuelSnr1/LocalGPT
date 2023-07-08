import os
import sys
import json
import requests

import openai
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma

import constants

os.environ["OPENAI_API_KEY"] = constants.APIKEY

def get_loader(loader_type='text', directory=".", filename='data.txt', glob="*.txt"):
    if loader_type == 'text':
        return TextLoader(filename)
    else:
        return DirectoryLoader(directory, glob)
    
    
def run_chat():
    loader = get_loader(loader_type='text')
    index = VectorstoreIndexCreator().from_loaders([loader])

    print('*' * 30)
    print('* Welcome to Emmanuel GPT *')
    print('*' * 30)

    while True:
        query = input("\nPlease enter a question: ")
        response = index.query(query, llm=ChatOpenAI())
        print(response)
        
        # Send the user's query and receive the chatbot's response
        response = requests.post('http://localhost:5000/chat', json={'message': query})
        data = json.loads(response.text)
        print('Chatbot response:', data['response'])


# Set loader_type to either 'text' or 'directory' as per your need
loader = get_loader(loader_type='text')
index = VectorstoreIndexCreator().from_loaders([loader])

# Display the welcome message
print('*' * 30)
print('* Welcome to Emmanuel GPT *')
print('*' * 30)

# while True:
#     query = input("\nPlease enter a question: ")
#     print(index.query(query, llm=ChatOpenAI()))

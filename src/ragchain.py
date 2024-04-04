import os
from langchain_openai import ChatOpenAI
from chromadb import Client
from langchain_community.embeddings import OpenAIEmbeddings

from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction


from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader,DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
import random
from uuid import uuid4
# import SentenceTransformersTokenTextSplitter 
from langchain.text_splitter import SentenceTransformersTokenTextSplitter


class ChainQA: 
    def __init__(self):
        # create chromadb instance and collection
        self.client = Client()
        rand = uuid4().hex + "-" + str(random.randint(0,200))
        self.collection_name = f"chainqa-" + rand

        self.embedding_function = SentenceTransformerEmbeddingFunction()
        
        self.collection = self.client.get_or_create_collection(self.collection_name,embedding_function=self.embedding_function)
    

    def add_document(self,doc):
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=0)
        self.client.add_document(self.collection_name,doc)
        self.token_splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=0)
        
        character_split_texts = self.text_splitter.split_text(doc)
        token_split_texts = [] 
        for t in character_split_texts: 
            token_split_texts += self.token_splitter.split_text(t) 
        ids = [str(i) for i in range(len(token_split_texts))]
        self.client.add(ids=ids,documents=token_split_texts, embedding_function=self.embedding_function, collection_name=self.collection_name)
        print("Added doc to vector storage")


    def set_llm(self,temp=0):
        print("Creating LLM instance.")
        self.openai_api_key = os.environ['OPENAI_API_KEY']
        self.llm = ChatOpenAI(openai_api_key=self.openai_api_key, temperature=temp)
        print("Success.")
    

    def vectorize(self): 
        print("Getting embeddings and creating Vector store.")
        embeddings = OpenAIEmbeddings()
        persist_directory = './duckdb'
        self.docsearch = Chroma.from_documents(self.docs,embeddings,persist_directory=persist_directory)
        print("Success")

    def get_qa_session(self): 
        return RetrievalQA.from_chain_type(llm=self.llm, chain_type="stuff", retriever=self.docsearch.as_retriever())
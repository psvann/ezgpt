import os
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings

class ChainQA: 
    def __init__(self,folder_path="files"):
        print("Getting files in folder path and splitting to docs.")
        self.folder_path = folder_path
        print("Running DR")
        loader = DirectoryLoader(self.folder_path, glob="**/*.txt")
        self.documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=0)
        self.docs = text_splitter.split_documents(self.documents)
        print("Success. Docs: %s" % len(self.docs))


    def set_llm(self,temp=0):
        print("Creating LLM instance.")
        self.openai_api_key = os.environ['OPENAI_API_KEY']
        self.llm = OpenAI(openai_api_key=self.openai_api_key, temperature=temp)
        print("Success.")
    
    def vectorize(self): 
        print("Getting embeddings and creating Vector store.")
        embeddings = OpenAIEmbeddings()
        persist_directory = './duckdb'
        self.docsearch = Chroma.from_documents(self.docs,embeddings,persist_directory=persist_directory)
        print("Success")

    def get_qa_session(self): 
        return RetrievalQA.from_chain_type(llm=self.llm, chain_type="stuff", retriever=self.docsearch.as_retriever())
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

openai_api_key = os.environ['OPENAI_API_KEY']

## get documents
folder_path = "./files"

# Get the list of files in the folder
file_list = os.listdir(folder_path)
print(file_list)

# Read the contents of each text file
file_contents = []
for file_name in file_list:
    if file_name.endswith('.txt'):
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as file:
            content = file.read()
            file_contents.append(content)

# # Print the contents of each file
# for content in file_contents:
#     print(content)

llm = OpenAI(openai_api_key=openai_api_key, temperature=1)

# Split results string into chunks
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
# docs = text_splitter.create_documents([megastring])
loader = DirectoryLoader(folder_path, glob="**/*.txt")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=0)
docs = text_splitter.split_documents(documents)


# print (f"You have {len(docs)} documents")
# print ("Preview:")
# print (docs[0].page_content, "\n")
# print (docs[1].page_content)

embeddings = OpenAIEmbeddings()
# print (f"Your embedding is length {len(text_embedding)}")
# print (f"Here's a sample: {text_embedding[:5]}...")

persist_directory = 'duckdb'
docsearch = Chroma.from_documents(docs,embeddings,persist_directory=persist_directory)

qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever())

while True: 
    QUERY = input("> ")
    answer = qa.run(QUERY)
    print(answer)
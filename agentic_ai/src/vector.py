import os
from langchain_community.llms import ollama
from langchain.document_loaders import UnstructuredFileLoader
from langchain.chains import retrieval_qa

from langchain.text_splitter import CharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from transformers import AutoTokenizer
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter


embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en")

# loading text data
input_file = "agentic_ai/data/Projects.txt"

with open(input_file, "r") as fl:
    content = fl.read()

# Define chunking method
sections = content.split('##########')


print(f"Total Chunks Created: {len(sections)}")



knowledge_base = Chroma.from_texts(sections, embedding_model, persist_directory="agentic_ai/data/chroma_db")

# retriever = FAISS.load_local(
#     "agentic_ai/data/faiss_index",
#     embeddings_model,
#     allow_dangerous_deserialization=True
# ).as_retriever()


print("Vector DB file saved.")
print(f"embedding {len(knowledge_base._collection.get(include=["embeddings"], limit=1)["embeddings"][0])}")
import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from PyPDF2 import PdfReader
from docx import Document

from config import (
  CHUNK_SIZE,
  CHUNK_OVERLAP,
  VECTORSTORE_DIR,
  HUGGINGFACEHUB_API_TOKEN,
  EMBEDDING_MODEL
)

os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN

def extract_all_texts(folder="downloads"):
  texts = []

  for file in os.listdir(folder):
    path = os.path.join(folder, file)
    if file.endswith(".pdf"):
      reader = PdfReader(path)
      text = "\n".join(page.extract_text() or "" for page in reader.pages)
      texts.append(text)
    elif file.endswith(".docx"):
      doc = Document(path)
      text = "\n".join(p.text for p in doc.paragraphs)
      texts.append(text)
    elif file.endswith(".txt"):
      with open(path, "r", encoding="utf-8") as f:
        texts.append(f.read())
    
    return texts

def chunk_documents(docs):
  splitter = RecursiveCharacterTextSplitter(
      chunk_size=CHUNK_SIZE,
      chunk_overlap=CHUNK_OVERLAP
  )
  chunks = []
  for doc in docs:
      chunks.extend(splitter.split_text(doc))
  return chunks

def get_embeddings(chunks):
  embedder = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
  return embedder.embed_documents(chunks)

def create_vectorstore():
  texts = extract_all_texts()
  chunks = chunk_documents(texts)
  embedder = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
  vectorstore = FAISS.from_texts(chunks, embedder)
  vectorstore.save_local(VECTORSTORE_DIR)

if __name__ == "__main__":
  create_vectorstore()
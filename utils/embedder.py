from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

def chunk_text(text, chunk_size=500, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(text)

def embed_chunks(chunks, db_path="vectorstore/verbalex_db"):
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
    )
    db = FAISS.from_texts(chunks, embedding=embedding_model)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    db.save_local(db_path)
    return db, chunks


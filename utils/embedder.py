# utils/embedder.py

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import os

def chunk_text(text, chunk_size=500, chunk_overlap=100):
    """
    Splits the full text into overlapping chunks.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)

def embed_chunks(chunks, db_path="vectorstore/verbalex_db"):
    """
    Converts chunks to embeddings and saves in FAISS.
    Returns the FAISS database object and the chunks.
    """
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.from_texts(chunks, embedding=embedding_model)

    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    db.save_local(db_path)
    return db, chunks

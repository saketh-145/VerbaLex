# utils/qa_engine.py

from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

def load_vectorstore(db_path="vectorstore/verbalex_db"):
    """
    Loads the FAISS vector DB from local storage.
    """
    return FAISS.load_local(db_path, embeddings=None, allow_dangerous_deserialization=True)

def create_qa_chain(vectorstore, model_name="llama3-8b-8192"):
    """
    Creates a RetrievalQA chain using Groq's LLaMA 3 model and the vectorstore retriever.
    """
    llm = ChatGroq(temperature=0, model_name=model_name)
    retriever = vectorstore.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)
    return qa_chain

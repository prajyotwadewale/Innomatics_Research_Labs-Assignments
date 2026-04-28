import os
import uuid
from langchain_community.vectorstores import Chroma
from embeddings import get_embedding_function

CHROMA_PATH = "chroma_db"

def clear_vector_store():
    """
    Clears the existing vector store by dynamically switching to a new unique directory.
    This safely bypasses Windows file locking issues.
    """
    global CHROMA_PATH
    CHROMA_PATH = f"chroma_db_{uuid.uuid4().hex}"
    print(f"Switched to new vector store path: {CHROMA_PATH}")

def initialize_vector_store(chunks):
    """
    Initialize the Chroma vector store with document chunks and save it to disk.
    """
    embedding_function = get_embedding_function()
    
    print(f"Saving {len(chunks)} chunks to ChromaDB at '{CHROMA_PATH}'...")
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_function,
        persist_directory=CHROMA_PATH
    )
    print("Vector store initialized and persisted.")
    return db

def get_vector_store():
    """
    Load the existing vector store from disk.
    """
    if not os.path.exists(CHROMA_PATH):
        raise RuntimeError("Vector store not found. Please ingest documents first.")
    
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    return db

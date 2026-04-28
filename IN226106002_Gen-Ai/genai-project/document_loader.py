import os
from langchain_community.document_loaders import PyPDFLoader

def load_documents(file_path: str):
    """
    Load a PDF document and extract its content.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Document not found at: {file_path}")
    
    print(f"Loading document: {file_path}")
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    print(f"Successfully loaded {len(docs)} pages.")
    return docs

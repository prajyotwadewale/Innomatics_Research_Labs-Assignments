from langchain_huggingface import HuggingFaceEmbeddings

def get_embedding_function():
    """
    Initialize and return the HuggingFace embedding function.
    Using an open-source model like all-MiniLM-L6-v2 which runs locally.
    """
    print("Initializing embedding function (HuggingFace all-MiniLM-L6-v2)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return embeddings

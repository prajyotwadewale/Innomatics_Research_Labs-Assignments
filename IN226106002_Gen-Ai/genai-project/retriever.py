from vector_store import get_vector_store

def retrieve_relevant_chunks(query: str, k: int = 3):
    """
    Retrieve the top 'k' most relevant document chunks for a given query.
    Returns both the documents and their relevance scores.
    """
    db = get_vector_store()
    
    print(f"Retrieving relevant chunks for query: '{query}'")
    # Using similarity_search_with_score to get confidence/similarity score
    results = db.similarity_search_with_score(query, k=k)
    return results

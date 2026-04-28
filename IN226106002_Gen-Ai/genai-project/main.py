import os
import sys
from dotenv import load_dotenv

# Import modules
from document_loader import load_documents
from chunking import chunk_documents
from vector_store import initialize_vector_store
from graph import build_graph

load_dotenv()

def ingest_document(pdf_path: str):
    """
    Run the ingestion pipeline: Load -> Chunk -> Embed -> Store.
    """
    print("\n--- Starting Ingestion Pipeline ---")
    try:
        docs = load_documents(pdf_path)
        chunks = chunk_documents(docs)
        initialize_vector_store(chunks)
        print("--- Ingestion Complete ---\n")
    except Exception as e:
        print(f"Ingestion failed: {e}")

def run_chat_interface():
    """
    Run the interactive CLI using the LangGraph workflow.
    """
    print("\n--- Starting Customer Support Assistant ---")
    print("Type 'exit' or 'quit' to stop.")
    
    # Check for API key early
    if not os.getenv("GROQ_API_KEY") or os.getenv("GROQ_API_KEY") == "your_groq_api_key_here":
        print("\n[ERROR] GROQ_API_KEY is not set. Please update your .env file.")
        return

    try:
        app = build_graph()
    except Exception as e:
         print(f"[ERROR] Failed to build graph: {e}")
         return
         
    while True:
        try:
            user_query = input("\nUser: ")
        except (KeyboardInterrupt, EOFError):
            break
            
        if user_query.lower() in ['exit', 'quit']:
            break
            
        if not user_query.strip():
            continue
            
        print("\nProcessing...")
        
        # Initial State
        initial_state = {
            "user_query": user_query,
            "retrieved_docs": [],
            "response": "",
            "confidence_score": "",
            "escalation_flag": False,
            "escalation_reason": ""
        }
        
        # Run graph
        try:
            result = app.invoke(initial_state)
            
            # Print Final Output
            print("\n" + "="*50)
            print(f"Assistant: {result.get('response')}")
            print(f"Confidence: {result.get('confidence_score')}")
            print("="*50)
        except Exception as e:
            print(f"\n[ERROR] Workflow failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--ingest":
        pdf_path = sys.argv[2] if len(sys.argv) > 2 else "sample.pdf"
        ingest_document(pdf_path)
    else:
        print("Usage instructions:")
        print("  1. To ingest a PDF: python main.py --ingest [path_to_pdf]")
        print("  2. To start chat : python main.py")
        print("\nStarting chat by default...")
        run_chat_interface()

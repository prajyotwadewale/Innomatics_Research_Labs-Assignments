import os
import streamlit as st
from dotenv import load_dotenv

# Set UI_MODE environment variable so hitl.py knows not to block with input()
os.environ["UI_MODE"] = "true"

from graph import build_graph
from document_loader import load_documents
from chunking import chunk_documents
from vector_store import initialize_vector_store, clear_vector_store

load_dotenv()

# Setup Streamlit page config
st.set_page_config(
    page_title="RAG Customer Support",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 RAG-Based Customer Support Assistant")
st.markdown("Upload your PDF document to the sidebar and ask questions about it!")

# Check for API key
if not os.getenv("GROQ_API_KEY") or os.getenv("GROQ_API_KEY") == "your_groq_api_key_here":
    st.error("⚠️ GROQ_API_KEY is not set. Please update your .env file to run the assistant.")
    st.stop()

# Ensure data directory exists
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Sidebar for file upload
with st.sidebar:
    st.header("Document Upload")
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    
    if uploaded_file is not None:
        file_path = os.path.join(DATA_DIR, uploaded_file.name)
        
        # Only ingest if the file hasn't been uploaded in the current session
        if st.session_state.get("last_uploaded_file") != uploaded_file.name:
            with st.spinner("Processing document..."):
                try:
                    # Save the uploaded file temporarily
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Run Ingestion Pipeline
                    clear_vector_store()
                    docs = load_documents(file_path)
                    chunks = chunk_documents(docs)
                    initialize_vector_store(chunks)
                    
                    st.success("Document ready for querying")
                    
                    # Store file name in session to avoid duplicate ingestion
                    st.session_state["last_uploaded_file"] = uploaded_file.name
                    st.session_state["document_processed"] = True
                    
                    # Clear chat history so the user gets a clean slate
                    st.session_state.messages = []
                    
                    # Rebuild the graph to connect to the updated vector store
                    st.session_state.app = build_graph()
                except Exception as e:
                    st.error(f"Error during ingestion: {e}")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "app" not in st.session_state:
    try:
        st.session_state.app = build_graph()
    except Exception as e:
        st.error(f"Failed to initialize the LangGraph application: {e}")
        st.stop()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if not st.session_state.get("document_processed", False):
    st.info("Please upload a document to start chatting.")
    prompt = st.chat_input("What would you like to know?", disabled=True)
else:
    prompt = st.chat_input("What would you like to know?")

if prompt:
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Thinking..."):
            initial_state = {
                "user_query": prompt,
                "retrieved_docs": [],
                "response": "",
                "confidence_score": "",
                "escalation_flag": False,
                "escalation_reason": ""
            }
            
            try:
                result = st.session_state.app.invoke(initial_state)
                response = result.get("response", "")
                confidence = result.get("confidence_score", "")
                
                if not response or str(response).strip() == "":
                    response = "No relevant information found."
                    confidence = "Low"
                
                final_text = response
                if confidence:
                    final_text += f"\n\n*(Confidence: {confidence})*"
                    
                message_placeholder.markdown(final_text)
                st.session_state.messages.append({"role": "assistant", "content": final_text})
                
            except Exception as e:
                st.error(f"An error occurred: {e}")

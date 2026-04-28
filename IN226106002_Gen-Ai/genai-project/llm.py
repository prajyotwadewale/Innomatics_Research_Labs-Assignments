import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

def get_llm():
    """
    Initialize the Groq LLM.
    Requires GROQ_API_KEY environment variable.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        raise ValueError("GROQ_API_KEY not found or is empty in .env file.")
    
    print("Initializing Groq LLM (llama3-8b-8192)...")
    llm = ChatGroq(
        groq_api_key=api_key, 
        model="llama-3.1-8b-instant", 
        temperature=0.2
    )
    return llm

def evaluate_and_generate_response(query: str, context: str):
    """
    Use the LLM to generate a response based on the context.
    We also ask the LLM to output its confidence in the answer.
    """
    llm = get_llm()
    
    prompt_template = """
You are a helpful customer support assistant. Answer the user's question based ONLY on the provided context.
If the context does not contain the answer, or if you are unsure, say "I don't know" and we will escalate to a human.

If the query contains "list", "all", "show", or "give all", you MUST extract ALL relevant items from the context and format your response as a standard Markdown bulleted list. Use the '-' character for bullets and separate each bullet point with a DOUBLE NEWLINE. NEVER return empty output.

Context:
{context}

Question: {query}

Respond in the exact following format:
Answer: 
[Your answer here]
Confidence: [High/Medium/Low]
"""
    
    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = prompt | llm
    
    response = chain.invoke({"context": context, "query": query})
    return response.content

from typing import TypedDict, List, Any
from langgraph.graph import StateGraph, END
from retriever import retrieve_relevant_chunks
from llm import evaluate_and_generate_response
from hitl import human_in_the_loop

# 1. Define State
class AgentState(TypedDict):
    user_query: str
    retrieved_docs: List[Any]
    response: str
    confidence_score: str
    escalation_flag: bool
    escalation_reason: str

# 2. Nodes
def retrieval_and_processing_node(state: AgentState):
    """
    Node to retrieve documents and generate an initial response using LLM.
    """
    query = state["user_query"]
    query_lower = query.lower()
    
    # Dynamic retrieval logic
    k_val = 8 if any(word in query_lower for word in ["list", "all", "show", "give all"]) else 4
    
    # Retrieve documents
    try:
        results = retrieve_relevant_chunks(query, k=k_val)
    except Exception as e:
        return {
            "retrieved_docs": [],
            "escalation_flag": True,
            "escalation_reason": f"Retrieval failed or vector store missing: {e}"
        }
    
    # Extract docs and check similarity scores
    docs = []
    lowest_distance = float('inf')
    
    for doc, score in results:
        docs.append(doc.page_content)
        if score < lowest_distance:
            lowest_distance = score
            
    if not docs:
         return {
            "retrieved_docs": [],
            "escalation_flag": True,
            "escalation_reason": "No relevant documents found."
        }
        
    context = "\n\n".join(docs)
    
    if not context.strip():
        print("[DEBUG] Context is empty. Skipping LLM call.")
        return {
            "retrieved_docs": [],
            "response": "No relevant information found.",
            "confidence_score": "Low",
            "escalation_flag": True,
            "escalation_reason": "No context extracted from vector store."
        }
        
    print(f"\n[DEBUG] Context length: {len(context)}")
    print(f"[DEBUG] Retrieved chunks: {len(docs)}")
    
    # Call LLM
    try:
        llm_output = evaluate_and_generate_response(query, context)
        print(f"\n[DEBUG] Raw LLM Response:\n{llm_output}\n")
        
        # Parse output for answer and confidence
        lines = llm_output.split('\n')
        answer = ""
        confidence = "Low"
        parsing_answer = False
        
        for line in lines:
            if line.startswith("Confidence:"):
                confidence = line.replace("Confidence:", "", 1).strip()
                parsing_answer = False
            elif line.startswith("Answer:"):
                answer += line.replace("Answer:", "", 1).strip() + "\n"
                parsing_answer = True
            elif parsing_answer:
                answer += line + "\n"
                
        answer = answer.strip()
        
        # Force markdown list formatting if the LLM output bullet characters on the same line
        answer = answer.replace(" • ", "\n\n- ").replace("• ", "- ")
        
        if not answer or answer == "":
            answer = "No relevant information found."
            confidence = "Low"
            
        return {
            "retrieved_docs": docs,
            "response": answer,
            "confidence_score": confidence,
            "escalation_flag": False
        }
    except Exception as e:
         return {
            "retrieved_docs": docs,
            "escalation_flag": True,
            "escalation_reason": f"LLM Processing failed: {e}"
        }

def decision_node(state: AgentState):
    """
    Conditional routing logic based on state flags and confidence.
    Returns the next node to transition to.
    """
    if state.get("escalation_flag"):
        return "hitl_node"
        
    confidence = state.get("confidence_score", "").lower()
    response = state.get("response", "").lower()
    
    # Escalation Rules
    if "low" in confidence or "i don't know" in response:
        state["escalation_reason"] = "LLM indicated low confidence or could not find answer."
        return "hitl_node"
        
    return "output_node"

def hitl_node(state: AgentState):
    """
    Node to handle human-in-the-loop.
    """
    reason = state.get("escalation_reason", "Unknown reason")
    query = state["user_query"]
    
    human_answer = human_in_the_loop(query, reason)
    
    return {
        "response": f"[Human Agent] {human_answer}",
        "confidence_score": "Human-Verified",
        "escalation_flag": True
    }

def output_node(state: AgentState):
    """
    Node to formulate the final output.
    """
    return {"response": state["response"]}


# 3. Build Graph
def build_graph():
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("processing_node", retrieval_and_processing_node)
    workflow.add_node("hitl_node", hitl_node)
    workflow.add_node("output_node", output_node)
    
    # Add edges
    workflow.set_entry_point("processing_node")
    
    # Conditional edges from processing to either hitl or output
    workflow.add_conditional_edges(
        "processing_node",
        decision_node,
        {
            "hitl_node": "hitl_node",
            "output_node": "output_node"
        }
    )
    
    workflow.add_edge("hitl_node", END)
    workflow.add_edge("output_node", END)
    
    # Compile
    app = workflow.compile()
    return app

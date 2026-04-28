import os

def human_in_the_loop(query: str, reason: str):
    """
    Simulate a human-in-the-loop escalation.
    """
    print(f"\n[ESCALATION TRIGGERED] Reason: {reason}")
    print(f"User Query: {query}")
    print("Routing to human agent...")
    print("-" * 50)
    
    if os.getenv("UI_MODE") == "true":
        return "This query requires human escalation and has been routed to a human agent. They will follow up with you shortly."
    
    # Simulate a human agent responding manually via CLI
    human_response = input("Human Agent (please provide an answer): ")
    return human_response

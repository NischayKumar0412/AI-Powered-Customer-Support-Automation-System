from state import SupportState
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from rag import retrieve_context
import json

llm = ChatOllama(model="llama3.1:latest", temperature=0)

def intent_classifier_node(state: SupportState) -> SupportState:
    query = state["query"]
    prompt = f"""
    You are an intent classifier for a customer support system.
    Categorize the following customer query into exactly one of these departments:
    - Sales
    - Technical
    - Billing
    - Account
    
    If it's about pricing, plans, or product information, choose Sales.
    If it's about app errors, installation, or configuration, choose Technical.
    If it's about invoices, refunds, or payment issues, choose Billing.
    If it's about password reset, profile updates, or account activation, choose Account.
    If the user is asking about previous issues or just saying hello, you can choose 'Memory' or 'General'.
    
    Return ONLY the department name as a plain string.
    
    Query: {query}
    """
    response = llm.invoke(prompt)
    intent = response.content.strip()
    
    # Handle minor variations
    if "sales" in intent.lower(): intent = "Sales"
    elif "technical" in intent.lower(): intent = "Technical"
    elif "billing" in intent.lower(): intent = "Billing"
    elif "account" in intent.lower(): intent = "Account"
    elif "memory" in intent.lower() or "previous" in intent.lower(): intent = "Memory"
    else: intent = "General"
    
    return {"intent": intent}

def rag_node(state: SupportState) -> SupportState:
    query = state["query"]
    context = retrieve_context(query)
    return {"retrieved_context": context}

def base_agent(state: SupportState, department: str) -> SupportState:
    query = state["query"]
    context = state.get("retrieved_context", "")
    
    prompt = f"""
    You are a helpful {department} support agent.
    Draft a response to the customer's query using the provided context if relevant.
    
    Context: {context}
    
    Customer Query: {query}
    """
    response = llm.invoke(prompt)
    draft = response.content.strip()
    
    # Check for high-risk requests that need approval
    risk_prompt = f"""
    Analyze the customer query and determine if it falls into any of these high-risk categories:
    - Refund requests
    - Subscription cancellation
    - Account closure requests
    - Compensation requests
    - Escalation to management
    
    Respond with 'YES' if it is a high-risk request, and 'NO' otherwise.
    
    Customer Query: {query}
    """
    risk_response = llm.invoke(risk_prompt)
    requires_approval = "yes" in risk_response.content.strip().lower()
    
    return {"draft_response": draft, "requires_approval": requires_approval}

def sales_agent_node(state: SupportState) -> SupportState:
    return base_agent(state, "Sales")

def technical_agent_node(state: SupportState) -> SupportState:
    return base_agent(state, "Technical Support")

def billing_agent_node(state: SupportState) -> SupportState:
    return base_agent(state, "Billing")

def account_agent_node(state: SupportState) -> SupportState:
    return base_agent(state, "Account")

def supervisor_node(state: SupportState) -> SupportState:
    draft = state.get("draft_response", "")
    query = state["query"]
    approval_status = state.get("approval_status")
    
    if state.get("requires_approval") and approval_status == "Rejected":
        final_response = "I'm sorry, but your request has been reviewed and denied by our management team."
        return {"final_response": final_response}
        
    prompt = f"""
    You are a Customer Support Supervisor.
    Review and improve the following draft response to the customer.
    Ensure the tone is professional, empathetic, and accurate.
    If the draft says an action was taken, ensure the language reflects that it will be processed.
    
    Customer Query: {query}
    Draft Response: {draft}
    
    Return only the improved final response.
    """
    response = llm.invoke(prompt)
    return {"final_response": response.content.strip()}
    
def memory_recall_node(state: SupportState) -> SupportState:
    messages = state.get("messages", [])
    prompt = f"""
    The customer is asking about their previous interactions.
    Review the conversation history and summarize what their previous issue was.
    
    Conversation History:
    {messages}
    
    Customer Query: {state["query"]}
    """
    response = llm.invoke(prompt)
    return {"final_response": response.content.strip(), "requires_approval": False}

def human_approval_node(state: SupportState) -> SupportState:
    # In a real system, this would pause the graph.
    # We will handle the actual pausing in the graph execution by using 'interrupt_before'
    # This node just serves as a placeholder if we need it, but usually interrupt is on the node itself.
    # Let's just return nothing here; the state will be updated externally.
    return {}

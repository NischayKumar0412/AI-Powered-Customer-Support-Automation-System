from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from state import SupportState
import nodes
import sqlite3

def route_intent(state: SupportState):
    intent = state.get("intent")
    if intent == "Sales":
        return "sales_agent"
    elif intent == "Technical":
        return "technical_agent"
    elif intent == "Billing":
        return "billing_agent"
    elif intent == "Account":
        return "account_agent"
    elif intent == "Memory":
        return "memory_recall"
    else:
        # Default fallback
        return "sales_agent"

def check_approval(state: SupportState):
    if state.get("requires_approval"):
        return "human_approval"
    return "supervisor"

def build_graph():
    workflow = StateGraph(SupportState)
    
    # Add nodes
    workflow.add_node("intent_classifier", nodes.intent_classifier_node)
    workflow.add_node("rag_node", nodes.rag_node)
    workflow.add_node("sales_agent", nodes.sales_agent_node)
    workflow.add_node("technical_agent", nodes.technical_agent_node)
    workflow.add_node("billing_agent", nodes.billing_agent_node)
    workflow.add_node("account_agent", nodes.account_agent_node)
    workflow.add_node("memory_recall", nodes.memory_recall_node)
    workflow.add_node("human_approval", nodes.human_approval_node)
    workflow.add_node("supervisor", nodes.supervisor_node)
    
    # Define edges
    workflow.add_edge(START, "intent_classifier")
    
    # If memory recall, skip RAG for simplicity, or we can go to RAG.
    # Let's go to RAG for everything except memory. Wait, memory recall doesn't need RAG.
    # But RAG is harmless. Let's just do Intent -> RAG.
    workflow.add_edge("intent_classifier", "rag_node")
    
    workflow.add_conditional_edges("rag_node", route_intent)
    
    # Agents to approval check
    for agent in ["sales_agent", "technical_agent", "billing_agent", "account_agent"]:
        workflow.add_conditional_edges(agent, check_approval)
        
    workflow.add_edge("memory_recall", END) # Memory recall doesn't need supervisor or approval usually
    
    workflow.add_edge("human_approval", "supervisor")
    workflow.add_edge("supervisor", END)
    
    # Memory
    conn = sqlite3.connect("memory.db", check_same_thread=False)
    memory = SqliteSaver(conn)
    
    app = workflow.compile(
        checkpointer=memory,
        interrupt_before=["human_approval"]
    )
    
    return app

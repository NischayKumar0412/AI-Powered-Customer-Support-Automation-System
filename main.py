import os
from dotenv import load_dotenv
from graph import build_graph
from rag import init_vector_store
from langchain_core.messages import HumanMessage, AIMessage
import time

load_dotenv()

def print_separator(title):
    print(f"\n{'='*50}\n{title}\n{'='*50}")

def run_demonstration():
    # Initialize RAG vector store
    print("Initializing Vector Store...")
    init_vector_store()
    
    # Build LangGraph workflow
    print("Building LangGraph...")
    app = build_graph()
    
    try:
        # Generate the diagram
        with open("workflow_diagram.png", "wb") as f:
            f.write(app.get_graph().draw_mermaid_png())
        print("Generated workflow diagram (workflow_diagram.png)")
    except Exception as e:
        print(f"Could not generate workflow diagram: {e}")

    # Set up thread config for memory
    thread_id = "customer_123"
    config = {"configurable": {"thread_id": thread_id}}
    
    queries = [
        "What are the pricing plans available for your software?",
        "I forgot my account password.",
        "My application crashes whenever I upload a file.",
        "I need a refund for my annual subscription.",
        "What was my previous support issue?"
    ]
    
    for i, query in enumerate(queries, 1):
        print_separator(f"Query {i}: {query}")
        
        # Add message to history manually or let state manage it.
        # Since our state handles 'messages' via Annotated[list, operator.add],
        # we can pass it as a list with one item.
        initial_state = {
            "customer_id": thread_id,
            "query": query,
            "messages": [{"role": "user", "content": query}]
        }
        
        # Run graph
        for event in app.stream(initial_state, config, stream_mode="values"):
            pass # Just consume the stream
            
        state = app.get_state(config)
        
        print(f"Intent classified: {state.values.get('intent')}")
        
        # Check if paused for human approval
        if state.next and state.next[0] == "human_approval":
            print("\n*** HUMAN-IN-THE-LOOP REQUIRED ***")
            print("The request requires human approval.")
            print(f"Draft Response so far: {state.values.get('draft_response')}")
            
            # Simulate human approval
            print("\nSupervisor action: Approving the request...")
            
            # Update state with approval status
            app.update_state(
                config,
                {"approval_status": "Approved"}
            )
            
            # Continue execution
            for event in app.stream(None, config, stream_mode="values"):
                pass
            
            state = app.get_state(config)
            
        final_response = state.values.get("final_response")
        print(f"\nFinal Response to Customer:\n{final_response}")
        
        # Update our 'messages' with the final response
        app.update_state(
            config,
            {"messages": [{"role": "assistant", "content": final_response}]}
        )
        
        time.sleep(2) # Pause for readability

if __name__ == "__main__":
    run_demonstration()

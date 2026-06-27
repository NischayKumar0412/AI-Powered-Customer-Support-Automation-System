# AI-Powered Customer Support Automation System

This is a LangGraph-based customer support automation system.
**Note:** This project has been updated to run entirely locally using **Ollama** .

## Project Structure
- `main.py`: Entry point and demonstration script.
- `graph.py`: Defines the LangGraph workflow and conditional routing.
- `nodes.py`: Contains the individual nodes (Intent Classifier, RAG, Agents, Supervisor).
- `rag.py`: Initializes and queries the Chroma vector store from the knowledge base using local embeddings.
- `state.py`: Defines the `SupportState` TypedDict for LangGraph.
- `knowledge_base/`: Contains mock markdown documents for RAG.

## Setup Instructions
1. Ensure you have Python 3.9+ installed, as well as the [Ollama Desktop App](https://ollama.com/).
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows use: venv\Scripts\activate
   # On Mac/Linux use: source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install langchain langgraph langgraph-checkpoint-sqlite langchain-ollama langchain-chroma python-dotenv langchain-community
   ```
4. Pull the required local AI models via Ollama:
   ```bash
   ollama pull llama3.1
   ollama pull nomic-embed-text
   ```
   
*(No OpenAI API key is required!)*

## Run Instructions
Ensure your Ollama app is running in the background, then execute the demonstration script:
```bash
python main.py
```
This will:
- Automatically generate a `workflow_diagram.png` visualization of the graph.
- Initialize the local SQLite memory database.
- Embed documents locally and process 5 demonstration queries.
- Demonstrate routing, RAG retrieval, Human-in-the-loop pausing, and Memory recall.

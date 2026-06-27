# AI-Powered Customer Support Automation System

This is a LangGraph-based customer support automation system built for Assignment 2.

## Project Structure
- `main.py`: Entry point and demonstration script.
- `graph.py`: Defines the LangGraph workflow and conditional routing.
- `nodes.py`: Contains the individual nodes (Intent Classifier, RAG, Agents, Supervisor).
- `rag.py`: Initializes and queries the Chroma vector store from the knowledge base.
- `state.py`: Defines the `SupportState` TypedDict for LangGraph.
- `knowledge_base/`: Contains mock markdown documents for RAG.

## Setup Instructions
1. Ensure you have Python 3.9+ installed.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies (if not already installed by the setup script):
   ```bash
   pip install langchain langgraph langchain-openai langchain-chroma python-dotenv langchain-community
   ```
4. Configure your API key:
   - Copy `.env.example` to `.env` (or just edit the `.env` file).
   - Add your OpenAI API key: `OPENAI_API_KEY=your-api-key`
   
## Run Instructions
Execute the demonstration script:
```bash
python main.py
```
This will:
- Initialize the SQLite memory database.
- Process 5 demonstration queries.
- Demonstrate routing, RAG retrieval, Human-in-the-loop, and Memory recall.
- Generate a `workflow_diagram.png` of the graph.

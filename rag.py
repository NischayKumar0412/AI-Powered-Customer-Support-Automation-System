import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

# Initialize the vector store as a global variable
vector_store = None

def init_vector_store():
    global vector_store
    if vector_store is not None:
        return
        
    # Load documents
    loader = DirectoryLoader('./knowledge_base', glob="**/*.md", loader_cls=TextLoader)
    documents = loader.load()
    
    # Split text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = text_splitter.split_documents(documents)
    
    # Create vector store
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vector_store = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory="./chroma_db")

def retrieve_context(query: str, k: int = 3) -> str:
    if vector_store is None:
        init_vector_store()
        
    docs = vector_store.similarity_search(query, k=k)
    context = "\n\n".join([doc.page_content for doc in docs])
    return context

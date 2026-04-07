from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

CHROMA_PATH = "chroma_db"

def inspect():
    if not os.path.exists(CHROMA_PATH):
        print("Chroma DB not found.")
        return

    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vectorstore = Chroma(
        persist_directory=CHROMA_PATH, 
        embedding_function=embeddings
    )
    
    # Get all docs (limit to 1)
    # LangChain's Chroma wrapper doesn't have a direct 'get' method that exposes everything easily 
    # without a query, but we can access the underlying client.
    
    print("Inspecting underlying Chroma collection...")
    # Access logic may vary by version, trying standard approach
    try:
        collection = vectorstore._collection
        data = collection.get(limit=5)
        print("Metadata examples:")
        for m in data['metadatas']:
            print(m)
    except Exception as e:
        print(f"Error accessing collection: {e}")

if __name__ == "__main__":
    inspect()

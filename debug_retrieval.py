from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

CHROMA_PATH = "chroma_db"

def test_filters():
    if not os.path.exists(CHROMA_PATH):
        print("Chroma DB not found.")
        return

    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vectorstore = Chroma(
        persist_directory=CHROMA_PATH, 
        embedding_function=embeddings
    )
    
    query = "Inflation"
    
    filters_to_test = [
        ("Single Field (Year)", {"year": 2025}),
        ("Single Field (Country)", {"country_code": "US"}),
        ("Implicit AND", {"year": 2025, "country_code": "US"}),
        ("Explicit AND", {"$and": [{"year": 2025}, {"country_code": "US"}]})
    ]
    
    with open("debug_output.txt", "w") as f:
        f.write(f"Testing retrieval for query: '{query}'\n\n")
        
        for name, flt in filters_to_test:
            f.write(f"--- Testing: {name} ---\n")
            f.write(f"Filter: {flt}\n")
            try:
                results = vectorstore.similarity_search(query, k=1, filter=flt)
                f.write(f"Success! Found {len(results)} docs.\n")
                if results:
                    f.write(f"Metadata: {results[0].metadata}\n")
            except Exception as e:
                f.write(f"FAILED: {e}\n")
            f.write("\n")
    print("Done. Check debug_output.txt")

if __name__ == "__main__":
    test_filters()

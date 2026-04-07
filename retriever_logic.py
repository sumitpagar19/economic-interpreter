from langchain_core.retrievers import BaseRetriever
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from typing import List, Any
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
import os
from dotenv import load_dotenv

load_dotenv()

CHROMA_PATH = "chroma_db"

class EconomicNewsRetriever(BaseRetriever):
    vectorstore: Chroma
    year: int
    country_code: str
    k: int = 5

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        """
        Sync implementation for getting relevant documents.
        Applies metadata filtering for Year and Country Code.
        """
        # Construct filter
        filter_conditions = []
        if self.year:
            filter_conditions.append({"year": self.year})
        if self.country_code and self.country_code != 'Unknown':
            filter_conditions.append({"country_code": self.country_code})
        
        if len(filter_conditions) > 1:
            final_filter = {"$and": filter_conditions}
        elif len(filter_conditions) == 1:
            final_filter = filter_conditions[0]
        else:
            final_filter = None

        print(f"Retrieving news for query: '{query}' with filter: {final_filter}")
        
        results = self.vectorstore.similarity_search(
            query,
            k=self.k,
            filter=final_filter
        )
        return results

def get_retriever(year: int, country_code: str, k: int = 5):
    """
    Factory function to get a configured retriever instance.
    """
    if not os.path.exists(CHROMA_PATH):
        raise FileNotFoundError(f"Chroma DB not found at {CHROMA_PATH}. Run processor.py first.")

    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vectorstore = Chroma(
        persist_directory=CHROMA_PATH, 
        embedding_function=embeddings
    )
    
    return EconomicNewsRetriever(
        vectorstore=vectorstore, 
        year=year, 
        country_code=country_code, 
        k=k
    )

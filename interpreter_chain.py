from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from retriever_logic import get_retriever
from dotenv import load_dotenv
import os
import time

load_dotenv()

PROMPT_TEMPLATE = """
You are an Economic Interpreter for the general public.
Your goal is to explain a significant economic shift in a simple, story-like manner.

**Context:**
- Country: {country}
- Year: {year}
- Indicator: {indicator_name}
- Raw Data: The value changed by {delta:.2f}% (YoY).

**Correlated News Events:**
{news_context}

**Instructions:**
1. Analyze the news events to find a likely cause or effect related to the economic data.
2. Explain the relationship in a narrative form.
3. Avoid technical jargon.
4. If the news doesn't seem directly relevant, state that the specific cause might be external but highlight the general atmosphere of that year.
5. Focus on the human impact where possible.

**Story:**
"""

def get_interpreter_chain():
    """
    Creates the LangChain pipeline.
    """
    model = ChatGoogleGenerativeAI(
        model="models/gemini-2.5-flash",
        temperature=0.2
    )
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    parser = StrOutputParser()
    
    chain = prompt | model | parser
    return chain

def generate_story(country, year, indicator_name, delta, country_code):
    """
    Orchestrates the retrieval and generation with retry logic.
    """
    print(f"Generating story for {country} ({year})...")
    
    # 1. Retrieve News
    try:
        retriever = get_retriever(year=year, country_code=country_code, k=5)
        # We pass a generic query to find major events in that context
        query = f"Significant economic or political events in {country} in {year} related to {indicator_name}"
        docs = retriever.invoke(query)
        
        news_context = "\n".join([f"- {d.page_content}" for d in docs])
        if not news_context:
            news_context = "No specific news events found for this period in the database."
            
    except Exception as e:
        print(f"Retrieval Error: {e}")
        news_context = "Could not retrieve news data."

    # 2. Generate Narrative with Retry Logic
    chain = get_interpreter_chain()
    max_retries = 3
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            response = chain.invoke({
                "country": country,
                "year": year,
                "indicator_name": indicator_name,
                "delta": delta,
                "news_context": news_context
            })
            return response
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)
                    print(f"Rate limit hit. Retrying in {wait_time}s... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                else:
                    print(f"Max retries exceeded. Please enable billing in Google Cloud Console.")
                    raise
            else:
                raise

if __name__ == "__main__":
    # Test Run
    try:
        story = generate_story(
            country="United States", 
            year=2025, 
            indicator_name="Inflation", 
            delta=3.5,
            country_code="US"
        )
        print("\n--- Generated Story ---\n")
        print(story)
    except Exception as e:
        print(f"Error: {e}")

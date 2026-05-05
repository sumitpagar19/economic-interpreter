# Economic Interpreter

A Streamlit app that combines World Development Indicators (WDI) time-series data with historical news (GDELT) to generate concise, human-friendly narratives explaining notable year-to-year economic shifts.

---

## What this project does
- Loads cleaned WDI data and shows interactive charts.
- Indexes cleaned GDELT news events in a persistent Chroma vector store (embeddings via Google Generative AI).
- Retrieves contextually relevant news for a selected country & year and uses a generative model to produce a short narrative explaining the observed change.

---

## Repository layout (important files)
- `app.py` — Streamlit front-end (UI, charting, user interaction).
- `processor.py` — Data loaders and vector store builder (`load_wdi_data()`, `create_news_vector_store()`).
- `preprocess_gdelt.py` — Preprocess raw GDELT exports into `cleaned_data/news_cleaned.csv`.
- `retriever_logic.py` — `EconomicNewsRetriever` and `get_retriever()` (Chroma-based retriever with metadata filters).
- `interpreter_chain.py` — Prompt template and LLM invocation (`generate_story()`).
- `inspect_vectorstore.py`, `debug_retrieval.py`, `debug_models.py` — utilities to inspect and debug the index and API access.
- `cleaned_data/` — cleaned CSVs used by the app (not committed if `.gitignore` is present).
- `chroma_db/` — Chroma DB persistence (ignored by `.gitignore`).

---

## Requirements
Python 3.10+ (recommended). Install dependencies in `requirements.txt`:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## Environment variables
Place a `.env` file in the project root with at least the following variables:

- `GEMINI_API_KEY` — API key for Google Generative AI (used for both embeddings and generation via the installed packages).

Note: The repo currently includes `NEWS_API_KEY` in examples, but the codebase does not use it. Do NOT commit `.env`; this repo already includes `.env` in `.gitignore`.

Security reminder: If any secret was committed earlier, rotate it immediately (see "Security & removing secrets" below).

---

## Typical workflow
1. (Optional) Preprocess raw GDELT files into a cleaned CSV:

```bash
python preprocess_gdelt.py
# outputs cleaned_data/news_cleaned.csv
```

2. Build the vector store (embeddings + Chroma persistence):

```bash
python processor.py
# or import and call create_news_vector_store() from a REPL
```

By default `create_news_vector_store()` samples a small number of rows for faster dev loops; remove the `.head(50)` sample in `processor.py` to index the full dataset.

3. Run the Streamlit app:

```bash
streamlit run app.py
# or use run_app.bat on Windows
```

4. In the UI, select a country and indicator, choose a year, and press **Explain this Shift** to generate a narrative.

---

## How retrieval & generation work (pipeline)
- `app.py` loads WDI via `processor.load_wdi_data()` and renders UI.
- On user request, `app.py` calls `generate_story(country, year, indicator_name, delta, country_code)` from `interpreter_chain.py`.
- `generate_story()` obtains a `retriever` via `get_retriever(year, country_code)` in `retriever_logic.py`.
- The retriever applies metadata filters (`year`, `country_code`) and performs a similarity search against the Chroma vector store.
- Retrieved news snippets are concatenated into `news_context`, then passed to a prompt template and sent to the generative model (via LangChain wrappers).
- The model returns a short story-like explanation.

---

## Troubleshooting & tips
- If you see no news results:
  - Confirm `chroma_db/` exists and is populated.
  - Confirm `cleaned_data/news_cleaned.csv` was indexed (increase sampling or re-run `processor.create_news_vector_store()`).
  - Region selections (e.g., "South Asia") may not map to single `country_code` metadata values; retrieval filters use `country_code` stored in the document metadata.

- To get more context into the narrative:
  - Rebuild the vector store without `.head(50)` in `processor.py`.
  - Increase `k` in `get_retriever()` to return more docs.

- If LLM calls fail with rate limits: the code retries with exponential backoff (see `interpreter_chain.py`). Consider enabling billing or using a higher quota model.

---

## Security & removing secrets from git history
Adding `.env` to `.gitignore` prevents future commits but does not remove secrets already committed. If you have committed secrets, rotate them immediately in the provider console and remove the file from the repository history.

Quick cleanup steps (local):

```bash
# remove from index so future commits won't include .env
git rm --cached .env
git commit -m "Remove .env from repository"
git push
```

For permanent removal from history use the BFG or `git filter-repo` (requires force-push and coordination with collaborators). See the project owner notes for full commands.

---

## Next improvements (suggested)
- Index the full `news_cleaned.csv` by removing `.head(50)` in `processor.create_news_vector_store()`.
- Support region -> multiple country_code mapping so regional selections retrieve documents from all relevant countries.
- Add a small test harness to verify retrieval for a given country/year pair (`debug_retrieval.py` already helps with this).
- Improve grounding by adding source citations in generated narratives (include `SOURCEURL` in `page_content` and modify prompt to request citations).

---

## Where to look for more
- `processor.py` — vector store creation and data loading.
- `interpreter_chain.py` — prompt template and generation logic.
- `retriever_logic.py` — retriever filter logic.

---

If you want, I can: (a) expand the README with a sequence diagram and exact command examples for BFG/git-filter-repo cleanup, or (b) update `processor.py` to index the full dataset and re-run indexing here. Which would you like next?
# Full Project Context
The project involves creating a Generative AI system designed to bridge the understanding gap between complex economic data and the general public. While indicators like Inflation, GDP, and Unemployment rates are publicly available through various data portals, the underlying reasons for their fluctuations—such as geopolitical conflicts, government policy changes, or global supply chain shifts—are often buried in dense financial reports or fragmented news cycles. This system acts as an "Economic Interpreter" that translates raw numerical trends into human-centric stories.

At a high level, the system functions by correlating historical and real-time economic time-series data with relevant global news events and headlines. When the system detects or is asked about a specific economic change (e.g., a sudden spike in inflation), it identifies significant global and regional events from news archives during that exact period. Using Large Language Models (LLMs), it synthesizes this information to provide a simple, jargon-free explanation of cause and effect. The final output provides a clear trend visualization paired with bulleted "reasoning points" derived from the news.

Limitations and assumptions include a reliance on the availability of consistent annual or monthly economic reporting, which may have lags compared to real-time news. The system assumes that major economic shifts are generally reflected in documented news events and focuses on showing logical correlations rather than providing clinical financial causation or investment advice.

# Required Datasets
1. **World Development Indicators (WDI) - World Bank**: This is the core dataset for establishing numerical "ground truth." It provides over 60 years of historical trends for GDP, Inflation, Debt, and social indicators for all countries.
2. **GDELT Project (Global Database of Events, Language, and Tone)**: An open-source database that monitors global news, broadcast, and moving images in real-time. This is used to retrieve historical "event data" that matches the dates of economic fluctuations found in the WDI.
3. **NewsAPI or Open News Archives**: Supplemental publicly available news feeds and historical repositories used to provide the specific article text and headlines that the AI processes to generate its simple-language explanations.

# Tech Stack
*   **GenAI / LLM Integration**: OpenAI GPT-4o, Anthropic Claude 3.5 Sonnet, or Google Gemini 1.5 Pro to perform the synthesis of news data and numerical trends into simplified English.
*   **Data Processing**: Python with the Pandas and NumPy libraries for cleaning, filtering, and aligning numerical datasets with temporal news data.
*   **Backend**: Python (FastAPI or Flask) to manage the logic between the data retrieval systems and the AI interface.
*   **Frontend / UI**: Streamlit for rapid dashboard development or React for a custom, modern user interface that features interactive trend graphs and concise text panels.
*   **Integration Framework**: LangChain or LlamaIndex to coordinate the Retrieval-Augmented Generation (RAG) pipeline that connects the numerical data with the text-based news snippets.
*   **Data Visualization**: Plotly, Matplotlib, or D3.js to generate simple, high-visibility graphs for non-technical users.

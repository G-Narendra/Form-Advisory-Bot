# Project 7: Real-Time Farm Advisory Bot 🚜

## 🎯 Problem Statement
UAE farmers face challenges in managing irrigation and diagnosing crop diseases in the arid climate. They need immediate, localized advice. Waiting for long AI response generation times ruins the user experience in the field.

## 🏗️ Architecture
This system utilizes **RAG + Real-Time Streaming**:
- **RAG Knowledge Base**: Uses Hugging Face's `argilla/farming` dataset embedded into **Pinecone** for deep agricultural knowledge.
- **Context Awareness**: Pulls real-time live weather using **OpenWeatherMap API** to adjust advice (e.g., stopping irrigation if humidity is high or rain is expected).
- **Streaming UI**: Uses Gemini 2.5 Flash and Streamlit's `st.write_stream` to yield tokens to the screen the millisecond they are generated.

## 🚀 Setup & Run

```bash
# 1. Install Dependencies
pip install -r requirements.txt

# 2. Add your keys to .env
# OPENWEATHERMAP_API_KEY=your_key
# PINECONE_API_KEY=your_key
# GEMINI_API_KEY=your_key

# 3. Build the Vector Database (Run Once)
python scripts/build_knowledge.py

# 4. Start the Application
streamlit run app.py
```

## 🧠 Tech Stack
- **Vector DB**: Pinecone Serverless
- **Data Source**: Hugging Face Datasets (`argilla/farming`)
- **LLM**: Gemini 2.5 Flash (Streaming Mode)
- **APIs**: OpenWeatherMap
- **Framework**: Streamlit
import os
import sys
import streamlit as st
from dotenv import load_dotenv

# Setup environment
base_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(base_dir, '.env'))
sys.path.append(base_dir)

from src.core.bot import stream_advisory_response, get_current_weather

def main():
    st.set_page_config(
        page_title="Real-Time Farm Advisory Bot",
        page_icon="🚜",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "👋 Hello! I am your Real-Time Farm Advisory Bot. How can I help you with your crops today?"}
        ]

    # Sidebar for Context
    with st.sidebar:
        st.header("📍 Farm Context")
        location = st.selectbox("Select Location:", ["Al Ain, AE", "Fujairah, AE", "Dubai, AE", "Abu Dhabi, AE"])
        
        st.subheader("⛅ Real-Time Weather")
        weather_info = get_current_weather(location)
        st.info(weather_info)
        
        st.divider()
        st.markdown("### Suggested Queries:")
        if st.button("My tomatoes have yellow spots on leaves"):
            st.session_state.preset_query = "My tomatoes have yellow spots on leaves. What should I do?"
        if st.button("When to water dates in current heat?"):
            st.session_state.preset_query = f"Given the current weather ({weather_info}), how often should I water my date palms?"
            
        st.divider()
        pinecone_key = os.getenv("PINECONE_API_KEY")
        if not pinecone_key or pinecone_key == "your_pinecone_api_key_here":
            st.error("⚠️ Pinecone API Key missing. RAG is disabled. Please add it to .env")
        else:
            st.success("✅ Connected to Pinecone Knowledge Base")

    # Main Chat Interface
    st.title("🚜 Real-Time Farm Advisory Bot")
    st.caption("Powered by RAG, OpenWeatherMap, and Gemini 2.5 Flash Streaming")

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle Input (preset or text input)
    prompt = None
    if "preset_query" in st.session_state:
        prompt = st.session_state.preset_query
        del st.session_state.preset_query
    else:
        prompt = st.chat_input("Ask about irrigation, pests, crops, or fertilizers...")

    if prompt:
        # Display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Stream response
        with st.chat_message("assistant"):
            # st.write_stream yields chunks as they are generated for real-time UX
            response = st.write_stream(stream_advisory_response(prompt, location))
            
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()

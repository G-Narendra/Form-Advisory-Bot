"""
Build Agricultural Knowledge Base in Pinecone using Hugging Face dataset.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

base_dir = Path(__file__).parent.parent
sys.path.append(str(base_dir))
load_dotenv(base_dir / ".env")

from datasets import load_dataset
from pinecone import Pinecone, ServerlessSpec
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore

def main():
    pinecone_key = os.getenv("PINECONE_API_KEY")
    if not pinecone_key or pinecone_key == "your_pinecone_api_key_here":
        print("ERROR: Please set a valid PINECONE_API_KEY in the .env file.")
        sys.exit(1)

    print("Loading Argilla/farming dataset from Hugging Face...")
    # Taking top 200 entries to fit within free tier limits and speed up setup
    dataset = load_dataset("argilla/farming", split="train[:200]")

    print(f"Loaded {len(dataset)} documents. Connecting to Pinecone...")
    pc = Pinecone(api_key=pinecone_key)
    index_name = os.getenv("PINECONE_INDEX", "farm-advisory")

    if index_name not in pc.list_indexes().names():
        print(f"Creating Pinecone index: {index_name}")
        pc.create_index(
            name=index_name,
            dimension=768, # Google embeddings dimension
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    print("Embedding and uploading to Pinecone... This may take a moment.")
    
    texts = []
    metadatas = []
    
    for row in dataset:
        # Combine instruction and response for rich context
        instruction = row.get("instruction", "")
        response = row.get("response", "")
        text = f"Question: {instruction}\nAnswer: {response}"
        
        texts.append(text)
        metadatas.append({
            "source": "argilla/farming",
            "instruction": instruction
        })
    
    # Upload in batches
    vector_store = PineconeVectorStore.from_texts(
        texts=texts,
        embedding=embeddings,
        index_name=index_name,
        metadatas=metadatas
    )

    print(f"Successfully loaded {len(texts)} agricultural documents into Pinecone index '{index_name}'!")


if __name__ == "__main__":
    main()

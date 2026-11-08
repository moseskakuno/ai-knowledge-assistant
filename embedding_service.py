import os
import streamlit as st

from openai import OpenAI
from dotenv import load_dotenv


# Load local environment variables
load_dotenv()

# Get API key from local .env or Streamlit Cloud Secrets
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY not found. "
        "Configure it in .env or Streamlit Cloud Secrets."
    )

# Make API key available to other OpenAI clients
os.environ["OPENAI_API_KEY"] = api_key

client = OpenAI(api_key=api_key)

MODEL = "text-embedding-3-small"


def create_embedding(text):
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    text = text.replace("\n", " ")

    response = client.embeddings.create(
        model=MODEL,
        input=text
    )

    return response.data[0].embedding


def create_embeddings(texts):
    if not texts:
        return []

    clean_texts = [
        text.replace("\n", " ")
        for text in texts
        if text and text.strip()
    ]

    if not clean_texts:
        return []

    response = client.embeddings.create(
        model=MODEL,
        input=clean_texts
    )

    return [
        item.embedding
        for item in sorted(
            response.data,
            key=lambda item: item.index
        )
    ]
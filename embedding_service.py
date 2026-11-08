
import os

from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

client = OpenAI(api_key=api_key)

MODEL = "text-embedding-3-small"


def create_embedding(text):
    """
    Convert a single text into an embedding vector.
    """

    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    text = text.replace("\n", " ")

    response = client.embeddings.create(
        model=MODEL,
        input=text
    )

    return response.data[0].embedding


def create_embeddings(texts):
    """
    Convert multiple texts into embedding vectors.
    """

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
        for item in sorted(response.data, key=lambda item: item.index)
    ]

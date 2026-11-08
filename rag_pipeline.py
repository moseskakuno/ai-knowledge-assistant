
from openai import OpenAI

from embedding_service import create_embedding
from vector_store import search_chunks


# OpenAI client
client = OpenAI()

# Chat model
CHAT_MODEL = "gpt-6-luna"


def answer_question(question, n_results=3):
    """
    Answer a question using relevant document chunks.
    """

    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    # Step 1: Create embedding for the question
    question_embedding = create_embedding(question)

    # Step 2: Search for relevant document chunks
    results = search_chunks(
        question_embedding,
        n_results=n_results
    )

    if not results:
        return {
            "answer": "No relevant documents found.",
            "sources": []
        }

    # Step 3: Prepare context and sources
    context_parts = []
    sources = []

    for result in results:
        metadata = result["metadata"]

        context_parts.append(
            f"""
            Source: {metadata['source']}
            Page: {metadata['page']}
            Content: {result['text']}
            """
        )

        sources.append({
            "source": metadata["source"],
            "page": metadata["page"],
            "text": result["text"]
        })

    context = "\n".join(context_parts)

    # Step 4: Generate an answer with the AI model
    response = client.responses.create(
        model=CHAT_MODEL,
        instructions="""
        You are an AI Knowledge Assistant.

        Answer questions using only the supplied context.

        If the answer cannot be found in the context,
        clearly say that the documents do not contain
        enough information.

        Do not invent facts.

        Answer in the same language as the question.

        Cite your sources using the document name
        and page number.
        """,
        input=f"""
        Context:
        {context}

        Question:
        {question}
        """
    )

    return {
        "answer": response.output_text,
        "sources": sources
    }

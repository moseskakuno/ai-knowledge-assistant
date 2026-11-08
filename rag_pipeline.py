
from openai import OpenAI

from embedding_service import create_embedding
from vector_store import search_chunks


# OpenAI client
client = OpenAI()

# Chat model
CHAT_MODEL = "gpt-6-luna"


def answer_question(question, n_results=5):
    """
    Answer questions using relevant chunks
    from all uploaded PDF documents.
    """

    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    # Step 1: Create embedding for the question
    question_embedding = create_embedding(question)

    # Step 2: Search across all documents in ChromaDB
    results = search_chunks(
        question_embedding,
        n_results=n_results
    )

    if not results:
        return {
            "answer": "No relevant documents found.",
            "sources": []
        }

    # Step 3: Prepare context and source information
    context_parts = []
    sources = []

    for result in results:

        metadata = result["metadata"]

        source_info = {
            "source": metadata.get("source", "Unknown"),
            "page": metadata.get("page", "Unknown"),
            "text": result["text"],
            "distance": result["distance"]
        }

        # Avoid duplicate source passages
        if not any(
            existing["source"] == source_info["source"]
            and existing["page"] == source_info["page"]
            and existing["text"] == source_info["text"]
            for existing in sources
        ):
            sources.append(source_info)

        context_parts.append(
            f"""
            Document: {source_info['source']}
            Page: {source_info['page']}
            Content: {source_info['text']}
            """
        )

    context = "\n".join(context_parts)

    # Step 4: Generate answer using retrieved context
    response = client.responses.create(
        model=CHAT_MODEL,
        instructions="""
        You are an AI Knowledge Assistant.

        Answer questions using only the supplied document context.

        The context may contain information from multiple PDF documents.

        Compare and combine information from different documents
        when relevant.

        If the answer cannot be found in the context,
        clearly explain that the documents do not contain
        enough information.

        Do not invent facts.

        Answer in the same language as the question.

        Cite your sources using the document name
        and page number.
        """,
        input=f"""
        Document Context:

        {context}

        User Question:

        {question}
        """
    )

    # Step 5: Return answer and sources
    return {
        "answer": response.output_text,
        "sources": sources
    }

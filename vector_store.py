
import chromadb
import uuid

# Initialize persistent ChromaDB client
client = chromadb.PersistentClient(
    path=".chroma"
)

# Create or load the knowledge collection
collection = client.get_or_create_collection(
    name="knowledge_base",
    metadata={"hnsw:space": "cosine"}
)


def add_chunks(chunks, embeddings, source="unknown"):
    """
    Store text chunks and their embeddings in ChromaDB.
    """

    if len(chunks) != len(embeddings):
        raise ValueError(
            "Number of chunks and embeddings must match."
        )

    if not chunks:
        return []

    ids = [
        str(uuid.uuid4())
        for _ in chunks
    ]

    documents = [
        chunk["text"]
        for chunk in chunks
    ]

    metadatas = [
        {
            "page": int(chunk["page"]),
            "chunk_index": int(chunk["chunk_index"]),
            "source": source
        }
        for chunk in chunks
    ]

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return ids


def search_chunks(query_embedding, n_results=3):
    """
    Search for the most relevant text chunks.
    """

    total_chunks = collection.count()

    if total_chunks == 0:
        return []

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(n_results, total_chunks),
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    matches = []

    for i in range(len(results["ids"][0])):
        matches.append({
            "id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]
        })

    return matches

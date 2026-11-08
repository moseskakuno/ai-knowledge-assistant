
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


def document_exists(file_hash):
    """
    Check whether a document with this file hash
    already exists in ChromaDB.
    """
    if not file_hash:
        return False

    results = collection.get(
        where={"file_hash": file_hash},
        limit=1
    )

    return len(results["ids"]) > 0


def add_chunks(chunks, embeddings, source="unknown", file_hash=None):
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
            "source": source,
            "file_hash": file_hash or ""
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


def get_documents():
    """
    Return all stored documents and their chunk counts.
    """
    results = collection.get(
        include=["metadatas"]
    )

    documents = {}

    for metadata in results["metadatas"]:
        source = metadata.get("source", "Unknown")
        file_hash = metadata.get("file_hash", "")

        key = (source, file_hash)

        if key not in documents:
            documents[key] = {
                "source": source,
                "file_hash": file_hash,
                "chunks": 0
            }

        documents[key]["chunks"] += 1

    return list(documents.values())


def delete_document(source, file_hash=None):
    """
    Delete a document and all its chunks from ChromaDB.
    """
    if file_hash:
        collection.delete(
            where={"file_hash": file_hash}
        )
    else:
        collection.delete(
            where={"source": source}
        )

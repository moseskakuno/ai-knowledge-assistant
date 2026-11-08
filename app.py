
import streamlit as st
import hashlib

from document_processor import extract_text_from_pdf
from text_chunker import split_text_into_chunks
from embedding_service import create_embeddings

from rag_pipeline import answer_question

from vector_store import (
    add_chunks,
    document_exists,
    get_documents,
    delete_document
)

def calculate_file_hash(uploaded_file):
    """
    Calculate SHA-256 hash of an uploaded file.
    """
    file_content = uploaded_file.getvalue()
    return hashlib.sha256(file_content).hexdigest()


# Page configuration
st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="📚",
    layout="wide"
)


# Initialize session state
if "processed_files" not in st.session_state:
    st.session_state.processed_files = set()


# Application title

st.title("📚 AI Knowledge Assistant")

st.write(
    "Your personal AI-powered document knowledge platform."
)

# Dashboard metrics
documents = get_documents()

total_documents = len(documents)

total_chunks = sum(
    document["chunks"]
    for document in documents
)

st.markdown("---")

st.subheader("📊 Dashboard Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Documents",
        value=total_documents,
        help="Number of uploaded PDF documents"
    )

with col2:
    st.metric(
        label="Total Text Chunks",
        value=total_chunks,
        help="Number of stored document chunks"
    )

with col3:
    st.metric(
        label="Knowledge Base",
        value="Active" if total_documents > 0 else "Empty",
        help="Current document database status"
    )

st.markdown("---")



# PDF upload section
st.subheader("Upload your PDF documents")

uploaded_files = st.file_uploader(
    "Choose PDF files",
    type=["pdf"],
    accept_multiple_files=True
)


if uploaded_files:

    st.success(
        f"{len(uploaded_files)} PDF document(s) uploaded successfully!"
    )

    for file in uploaded_files:

        st.write(f"📄 {file.name}")

        # Step 1: Calculate SHA-256 hash
        file_hash = calculate_file_hash(file)

        # Step 2: Check for duplicate documents
        if document_exists(file_hash):
            st.warning(
                f"{file.name} has already been uploaded."
            )
            continue

        # Step 3: Process only new files
        if file.name not in st.session_state.processed_files:

            try:

                # Extract text from PDF
                pages = extract_text_from_pdf(file)

                if not pages:
                    st.warning(
                        f"No text could be extracted from {file.name}."
                    )
                    continue

                st.success(
                    f"Successfully extracted {len(pages)} pages!"
                )

                # Split text into chunks
                chunks = split_text_into_chunks(
                    pages,
                    chunk_size=800,
                    overlap=150
                )

                st.write(
                    f"Created {len(chunks)} text chunks."
                )

                if not chunks:
                    st.warning(
                        f"No text chunks were created for {file.name}."
                    )
                    continue

                # Create embeddings
                texts = [
                    chunk["text"] for chunk in chunks
                ]

                embeddings = create_embeddings(texts)

                # Store chunks in ChromaDB
                add_chunks(
                    chunks,
                    embeddings,
                    source=file.name,
                    file_hash=file_hash
                )

                # Mark file as processed
                st.session_state.processed_files.add(file.name)

                st.success(
                    f"Successfully stored {len(chunks)} chunks in ChromaDB!"
                )

                # Display extracted text
                for page in pages:
                    with st.expander(
                        f"Page {page['page']}"
                    ):
                        st.write(page["text"])

            except Exception as e:
                st.error(
                    f"Error processing PDF: {e}"
                )


# Document management section
st.markdown("---")

st.subheader("📂 Document Management")

documents = get_documents()

if documents:

    for document in documents:

        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            st.write(f"📄 **{document['source']}**")

        with col2:            
            chunk_count = document["chunks"]

            chunk_label = "chunk" if chunk_count == 1 else "chunks"

            st.write(
                f"{chunk_count} {chunk_label}"
            )

        with col3:
            if st.button(
                "🗑️ Delete",
                key=f"delete_{document['source']}_{document['file_hash']}"
            ):

                delete_document(
                    source=document["source"],
                    file_hash=document["file_hash"] or None
                )

                st.success(
                    f"{document['source']} deleted successfully!"
                )

                st.rerun()

else:

    st.info("No documents have been uploaded yet.")


st.markdown("---")


# Question and answer section
st.subheader("Ask your documents")

question = st.text_input(
    "Enter your question:"
)


if st.button("Ask AI"):

    if question.strip():

        try:

            with st.spinner(
                "AI is searching your documents..."
            ):

                result = answer_question(question)

            st.subheader("Answer")
            st.write(result["answer"])

            st.subheader("Sources")

            if result["sources"]:

                for index, source in enumerate(
                    result["sources"],
                    start=1
                ):

                    with st.expander(
                        f"📄 Source {index}: {source['source']} "
                        f"(Page {source['page']})"
                    ):

                        st.write("**Retrieved text:**")

                        st.write(source["text"])

                        st.caption(
                            f"Search distance: {source['distance']:.4f}"
                        )

            else:

                st.info("No sources were found.")
        except Exception as e:

            st.error(
                f"Error generating answer: {e}"
            )

    else:

        st.warning(
            "Please enter your question first."
        )

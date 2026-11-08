
import streamlit as st

from document_processor import extract_text_from_pdf
from text_chunker import split_text_into_chunks
from embedding_service import create_embeddings
from vector_store import add_chunks
from rag_pipeline import answer_question


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
    "Welcome to your AI Knowledge Assistant!"
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

        if file.name not in st.session_state.processed_files:

            try:
                # Step 1: Extract text from PDF
                pages = extract_text_from_pdf(file)

                st.success(
                    f"Successfully extracted {len(pages)} pages!"
                )

                # Step 2: Split text into chunks
                chunks = split_text_into_chunks(
                    pages,
                    chunk_size=800,
                    overlap=150
                )

                st.write(
                    f"Created {len(chunks)} text chunks."
                )

                # Step 3: Create embeddings
                texts = [
                    chunk["text"] for chunk in chunks
                ]

                embeddings = create_embeddings(texts)

                # Step 4: Store chunks in ChromaDB
                add_chunks(
                    chunks,
                    embeddings,
                    source=file.name
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

        else:
            st.info(
                f"{file.name} has already been processed."
            )


st.markdown("---")


# Question and answer section
st.subheader("Ask your documents")

question = st.text_input(
    "Enter your question:"
)

if st.button("Ask AI"):

    if question.strip():

        try:
            with st.spinner("AI is searching your documents..."):

                result = answer_question(question)

            st.subheader("Answer")
            st.write(result["answer"])

            st.subheader("Sources")

            for source in result["sources"]:
                st.write(
                    f"📄 {source['source']} "
                    f"(Page {source['page']})"
                )

        except Exception as e:
            st.error(
                f"Error generating answer: {e}"
            )

    else:
        st.warning(
            "Please enter a question first."
        )

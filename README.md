# 📚 AI Knowledge Assistant

An AI-powered knowledge assistant that allows users to upload multiple PDF documents and ask questions about their content. The application uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information from uploaded documents and generate context-aware answers with source references.

The project demonstrates how Generative AI, semantic search, and vector databases can be combined to build an interactive document knowledge platform.

## 🚀 Features

- **PDF Upload:** Upload one or multiple PDF documents.
- **Text Extraction:** Extract text from PDF files using PyPDF.
- **Text Chunking:** Split extracted text into smaller chunks while preserving original page numbers.
- **Embeddings:** Generate text embeddings using OpenAI's `text-embedding-3-small` model.
- **Vector Database:** Store and retrieve document chunks using ChromaDB with persistent local storage.
- **Semantic Search:** Find relevant document passages based on user questions.
- **Multi-Document RAG:** Search across multiple uploaded PDFs and combine relevant information from different documents.
- **AI-Powered Answers:** Generate context-aware answers using the OpenAI API.
- **Source References:** Display document names, page numbers, retrieved text passages, and search distances.
- **Duplicate Detection:** Use SHA-256 file hashing to identify documents that have already been uploaded, including files with different names but identical content.
- **Document Management:** View uploaded documents, check their stored chunk counts, and delete documents from the knowledge base.
- **Dashboard Overview:** Display key metrics, including total documents, total text chunks, and the current knowledge base status.
- **Interactive Interface:** Access all features through a Streamlit web application.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Interactive web application interface |
| OpenAI API | Text embeddings and AI-generated answers |
| ChromaDB | Persistent vector database |
| PyPDF | PDF text extraction |
| python-dotenv | Environment variable management |
| hashlib | SHA-256 document hashing and duplicate detection |

## 🧠 How It Works

The application follows a Retrieval-Augmented Generation (RAG) workflow:

1. **Upload:** The user uploads one or multiple PDF documents.
2. **Duplicate Check:** Each uploaded PDF is assigned a SHA-256 hash to identify previously stored documents.
3. **Extract:** Text is extracted from each PDF while preserving page information.
4. **Chunk:** The extracted text is divided into smaller text segments with overlapping content.
5. **Embed:** OpenAI converts each text segment into a numerical vector representation.
6. **Store:** The vectors, text passages, and metadata are stored in ChromaDB.
7. **Retrieve:** When the user asks a question, the application performs semantic search across the stored documents.
8. **Generate:** Relevant document passages are sent to the AI model as context.
9. **Answer:** The AI generates an answer based on the retrieved information.
10. **Display Sources:** The application displays the answer together with its supporting document passages and page references.

## 📂 Project Structure

```text
ai-knowledge-assistant/
│
├── app.py                  # Streamlit application and dashboard
├── document_processor.py   # PDF text extraction
├── text_chunker.py         # Text chunking logic
├── embedding_service.py    # OpenAI embedding generation
├── vector_store.py         # ChromaDB operations and document management
├── rag_pipeline.py         # RAG retrieval and answer generation
│
├── requirements.txt        # Python dependencies
├── .env                    # API key (not committed to Git)
├── .gitignore              # Files excluded from Git
├── README.md               # Project documentation
│
├── .chroma/                # Local persistent vector database (generated)
└── venv/                   # Python virtual environment (generated)
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/moseskakuno/ai-knowledge-assistant.git
cd ai-knowledge-assistant
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure your OpenAI API key

Create a `.env` file in the project root directory:

```env
OPENAI_API_KEY=your_openai_api_key
```

Replace `your_openai_api_key` with your own API key.

**Important:** Never upload your `.env` file or expose your API key publicly.

### 6. Run the application

```bash
streamlit run app.py
```

The application will be available in your browser at:

```text
http://localhost:8501
```

## 💡 Example Use Cases

### 1. Invoice Analysis

Upload an invoice PDF and ask:

> What is the total gross amount of this invoice?

The assistant retrieves relevant information and provides an answer with references to the original document and page number.

### 2. Multi-Document Comparison

Upload multiple invoices and ask:

> Compare the invoice amounts and identify any discrepancies.

The assistant searches across the uploaded documents and combines relevant information to generate an answer.

### 3. Document Knowledge Search

Upload technical documentation or reports and ask:

> What are the main findings described in these documents?

The assistant retrieves relevant passages from the knowledge base and generates a context-aware response.

## 📊 Dashboard and Document Management

The application includes a dashboard that provides an overview of the document knowledge base.

**Dashboard metrics:**

- Total number of uploaded documents.
- Total number of stored text chunks.
- Current knowledge base status (Active or Empty).

**Document management capabilities:**

- View all stored PDF documents.
- Display the number of text chunks per document.
- Delete individual documents and their associated chunks from ChromaDB.
- Prevent duplicate uploads using SHA-256 file hashing.

## 🔐 Security

- API credentials are stored in environment variables.
- The `.env` file is excluded from Git using `.gitignore`.
- Virtual environments and local database files are excluded from Git.
- API keys should never be committed to the repository.

## ⚠️ Current Limitations

- The application currently supports PDF documents only.
- Text extraction quality depends on the PDF structure. Scanned PDFs may require OCR.
- Answers depend on the information available in the uploaded documents.
- The current ChromaDB setup uses local persistent storage. Database files remain on the local machine and are not automatically synchronized to the cloud.
- The application currently does not include user authentication or multi-user access control.

## 🔮 Future Improvements

- Support for Word and plain-text documents.
- OCR support for scanned PDFs.
- Chat history and conversational memory.
- Improved source citations with text highlighting.
- Advanced document filtering and search options.
- Cloud-based vector database integration.
- User authentication and access control.
- Deployment with Streamlit Community Cloud.

## 👨‍💻 Author

**Moses Ochieng Akuno**

GitHub: [https://github.com/moseskakuno/ai-knowledge-assistant](https://github.com/moseskakuno/ai-knowledge-assistant)

A portfolio project demonstrating practical applications of:

- Generative AI
- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Vector Databases
- Document Processing
- Python Application Development

---

*Built with Python, Streamlit, OpenAI, and ChromaDB.*
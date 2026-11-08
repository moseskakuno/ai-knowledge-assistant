# 📚 AI Knowledge Assistant

An AI-powered knowledge assistant that allows users to upload PDF documents and ask questions about their content. The application uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information from uploaded documents and generate context-aware answers with source references.

## 🚀 Features

- **PDF Upload:** Upload one or multiple PDF documents.
- **Text Extraction:** Extract text from PDF files using PyPDF.
- **Text Chunking:** Split extracted text into smaller chunks while preserving page numbers.
- **Embeddings:** Generate text embeddings using OpenAI's `text-embedding-3-small` model.
- **Vector Database:** Store and retrieve document chunks using ChromaDB.
- **Semantic Search:** Find relevant document passages based on user questions.
- **AI-Powered Answers:** Generate answers using the OpenAI API.
- **Source References:** Display the document name and page number for retrieved information.
- **Interactive Interface:** Use the application through a Streamlit web interface.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application interface |
| OpenAI API | Embeddings and AI-generated answers |
| ChromaDB | Vector database |
| PyPDF | PDF text extraction |
| python-dotenv | Environment variable management |

## 🧠 How It Works

The application follows a Retrieval-Augmented Generation (RAG) workflow:

1. **Upload:** The user uploads one or more PDF documents.
2. **Extract:** Text is extracted from each PDF.
3. **Chunk:** The extracted text is divided into smaller text segments.
4. **Embed:** OpenAI converts each text segment into a numerical vector representation.
5. **Store:** The vectors and associated metadata are stored in ChromaDB.
6. **Retrieve:** When the user asks a question, the application searches for the most relevant document chunks.
7. **Generate:** The retrieved content is sent to the AI model as context.
8. **Answer:** The AI generates an answer based on the retrieved information and displays its sources.

## 📂 Project Structure

```text
ai-knowledge-assistant/
│
├── app.py                  # Streamlit application
├── document_processor.py   # PDF text extraction
├── text_chunker.py         # Text chunking logic
├── embedding_service.py    # OpenAI embedding generation
├── vector_store.py         # ChromaDB operations
├── rag_pipeline.py         # RAG retrieval and answer generation
│
├── requirements.txt        # Python dependencies
├── .env                    # API key (not committed to Git)
├── .gitignore              # Files excluded from Git
└── README.md               # Project documentation
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

The application will open in your browser.

## 💡 Example Use Case

Upload an invoice or another PDF document and ask:

> What information does this invoice contain?

The AI assistant retrieves relevant information from the document and generates an answer with references to the original PDF and page number.

## 🔐 Security

- API credentials are stored in environment variables.
- The `.env` file is excluded from Git using `.gitignore`.
- API keys should never be committed to the repository.

## ⚠️ Current Limitations

- The application currently supports PDF documents.
- The quality of text extraction depends on the PDF structure. Scanned PDFs may require OCR.
- Answers depend on the information available in the uploaded documents.
- The current ChromaDB setup uses local storage. Data persistence depends on the runtime environment.

## 🔮 Future Improvements

- Support for Word and text documents.
- OCR support for scanned PDFs.
- Chat history and conversational memory.
- Document management and deletion.
- Improved source citations with text highlighting.
- Persistent cloud-based vector database.
- User authentication and access control.
- Deployment with Streamlit Community Cloud.

## 👨‍💻 Author

**Moses Ochieng Akuno** — https://github.com/moseskakuno/ai-knowledge-assistant: 

A portfolio project demonstrating practical applications of:

- Generative AI
- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Vector Databases
- Python Application Development

---

*Built with Python, Streamlit, OpenAI, and ChromaDB.*
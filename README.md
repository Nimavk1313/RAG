# RAG Chat Assistant

A complete Retrieval-Augmented Generation (RAG) system with chat interface powered by Cerebras models, BERT-based semantic chunking, and FAISS vector database.

## 🚀 Quick Start

### Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```
*Note: First run downloads BERT models (~100MB). This is normal!*

2. **Configure API key** in `.env`:
```
CEREBRAS_API_KEY=your_api_key_here
```
Get your key at: https://cloud.cerebras.ai/

3. **Test connection:**
```bash
python check_api.py
```

4. **Launch app:**
```bash
streamlit run app.py
```

The app opens at `http://localhost:8501` 🎉

📖 **New to the system?** Read [QUICK_START.md](QUICK_START.md) for a detailed walkthrough!

## ⚠️ Troubleshooting Cloudflare Errors

If you see a **Cloudflare blocking error**, this typically means:

1. **Invalid API Key** - Your API key may be incorrect or expired
   - Get a new key from [Cerebras Cloud](https://cloud.cerebras.ai/)
   - Update your `.env` file with the new key
   - Restart the application

2. **Network Issues** - Your IP may be blocked or there are connectivity problems
   - Try a different network
   - Disable VPN if using one
   - Contact Cerebras support

**Use the "🧪 Test Connection" button in the sidebar** to diagnose issues before chatting.

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions.

## 📁 Project Structure

```
NEW RAG/
├── app.py                              # Main chat interface (home page)
├── pages/
│   ├── 1_📄_Document_Processing.py      # Document upload & processing
│   ├── 2_📚_Document_Library.py         # Browse processed documents  
│   ├── 3_🎯_RAG_Chat.py                 # RAG chat with context retrieval
│   └── 4_🗄️_Vector_Database.py         # FAISS vector DB management
├── src/
│   ├── processing/
│   │   ├── document_loader.py           # Load PDF, DOCX, TXT files
│   │   ├── semantic_chunker.py          # BERT-based chunking
│   │   └── document_processor.py        # Processing orchestrator
│   └── retrieval/
│       ├── vector_store.py              # FAISS vector store wrapper
│       └── vector_db_manager.py         # Collection management
├── data/
│   ├── documents/                       # Uploaded documents
│   ├── processed/                       # Processed documents (JSON)
│   └── vector_db/                       # FAISS vector database
├── check_api.py                         # API connection testing
├── .env                                 # Environment variables
├── requirements.txt                     # Python dependencies
├── README.md                           # This file
├── QUICK_START.md                      # Quick start guide
├── FEATURES.md                         # Chat features documentation
├── DOCUMENT_PROCESSING.md              # Document processing guide
├── VECTOR_DATABASE.md                  # FAISS vector DB guide
├── TROUBLESHOOTING.md                  # Troubleshooting guide
└── .gitignore                          # Git ignore rules
```

## 🔮 Future RAG Components (Planned Structure)

```
NEW RAG/
├── app.py
├── .env
├── requirements.txt
├── config/
│   └── config.yaml     # Configuration settings
├── src/
│   ├── llm/
│   │   └── cerebras_client.py    # Cerebras API wrapper
│   ├── retrieval/
│   │   ├── embeddings.py         # Embedding generation
│   │   ├── vector_store.py       # Vector database operations
│   │   └── retriever.py          # Document retrieval logic
│   ├── processing/
│   │   ├── document_loader.py    # Load various document formats
│   │   └── text_splitter.py      # Chunk documents
│   └── utils/
│       └── helpers.py             # Utility functions
├── data/
│   ├── documents/      # Source documents
│   └── vector_db/      # Vector database storage
└── notebooks/          # Jupyter notebooks for experimentation
```

## 🎯 Features

### 💬 Chat Interface (Main Page)
- ✅ **Real-time streaming chat** with multiple Cerebras models
- ✅ **12+ Models** - Llama, Qwen, Gemma, Mistral, GPT-OSS
- ✅ **Conversation history** - Maintains context during chat
- ✅ **Advanced Settings** - Temperature, top-p, max tokens
- ✅ **Model switching** - Change models mid-conversation
- ✅ **Connection testing** - Verify API before chatting

### 📄 Document Processing (New!)
- ✅ **Multi-format support** - PDF, DOCX, TXT, CSV
- ✅ **BERT-based semantic chunking** - 3 chunking methods
- ✅ **Multiple BERT models** - Fast to high-quality options
- ✅ **Configurable parameters** - Chunk size, similarity threshold
- ✅ **Real-time processing** - Progress tracking
- ✅ **Semantic search** - Find relevant chunks by meaning
- ✅ **Chunk viewer** - Browse and explore chunks
- ✅ **Export results** - Download processed documents

### 📚 Document Library (New!)
- ✅ **Browse all documents** - View processing history
- ✅ **Filter & search** - Find documents quickly
- ✅ **Statistics dashboard** - Chunk analytics
- ✅ **Preview chunks** - View sample content
- ✅ **Document management** - Download or delete

### Available Chat Models
- **Llama**: 4 Scout 17B, 3.3 70B, 3.1 (8B/70B)
- **Qwen**: 3 235B (A22B), 3 32B, 2.5 (7B/32B)
- **Gemma**: 2 9B
- **Mistral**: 7B
- **Other**: GPT OSS 120B

### Available BERT Models
- **all-MiniLM-L6-v2** - Fast, 384 dimensions (Default)
- **all-mpnet-base-v2** - High quality, 768 dimensions
- **paraphrase-multilingual** - Multilingual support

📖 **Documentation:**
- [FEATURES.md](FEATURES.md) - Chat features & model comparisons
- [DOCUMENT_PROCESSING.md](DOCUMENT_PROCESSING.md) - Complete processing guide

### 🎯 RAG System (NEW!)
- ✅ **FAISS vector database** - Fast similarity search
- ✅ **RAG chat interface** - Chat with context from documents
- ✅ **Context retrieval** - Automatic relevant chunk retrieval
- ✅ **Source attribution** - Shows which chunks were used
- ✅ **Collection management** - Organize documents in collections
- ✅ **Multiple index types** - Flat, IVF, HNSW for different scales
- ✅ **Vector DB viewer** - Manage and explore collections

### 🔮 Coming Soon
- 🌐 Multi-language document support
- 📸 OCR for scanned documents
- 🔄 Hybrid search (vector + keyword)
- 📊 Advanced analytics and insights
- 🔗 Multiple vector DB backends (Pinecone, Chroma)

## 🎨 Usage Guide

### 1️⃣ Chat with AI Models

1. Start the app: `streamlit run app.py`
2. Select a Cerebras model from the sidebar dropdown
3. Adjust temperature/parameters if needed (optional)
4. Type your message and press Enter
5. Watch the AI respond in real-time!

**Tips:**
- Use "Test Connection" button to verify API
- Lower temperature (0.2-0.4) for factual responses
- Higher temperature (0.7-0.9) for creative responses

### 2️⃣ Process Documents

1. Navigate to **📄 Document Processing** page (sidebar)
2. Configure BERT model and chunking parameters
3. Click "Initialize Processor" (first time only)
4. Upload your document (PDF, DOCX, or TXT)
5. Click "Process Document"
6. View chunks, search content, export results

**Recommended Settings:**
- **Method**: Semantic (best for RAG)
- **BERT Model**: all-MiniLM-L6-v2 (fast)
- **Similarity**: 0.5 (balanced)
- **Max Chunk**: 1000 characters

### 3️⃣ Browse Document Library

1. Navigate to **📚 Document Library** page
2. Browse all processed documents
3. Filter by chunking method
4. Search by filename
5. View chunks, statistics, and download results

## ⚙️ Configuration Options

### Chat Settings

| Parameter | Range | Default | Purpose |
|-----------|-------|---------|---------|
| Model | 12 options | Qwen 3 235B | Which AI model to use |
| Temperature | 0.0 - 1.0 | 0.7 | Creativity vs focus |
| Top P | 0.0 - 1.0 | 0.8 | Response diversity |
| Max Tokens | 100 - 20000 | 20000 | Response length limit |

### Document Processing Settings

| Parameter | Range | Default | Purpose |
|-----------|-------|---------|---------|
| BERT Model | 3 options | MiniLM | Embedding quality vs speed |
| Chunking Method | 3 methods | Semantic | How to split text |
| Similarity | 0.0 - 1.0 | 0.5 | Chunk similarity threshold |
| Max Chunk Size | 200 - 2000 | 1000 | Maximum chunk characters |
| Min Chunk Size | 50 - 500 | 100 | Minimum chunk characters |

## 🛠️ Technology Stack

### Core Technologies
- **Frontend**: Streamlit (Multi-page app)
- **LLM Provider**: Cerebras Cloud SDK
- **Models**: 12+ Cerebras models (Llama, Qwen, Gemma, Mistral, GPT-OSS)

### Document Processing
- **Text Extraction**: PyPDF2, python-docx
- **Embeddings**: Sentence-Transformers (BERT models)
- **Chunking**: Custom semantic chunker with cosine similarity
- **Storage**: JSON format with embeddings

### Vector Database
- **FAISS**: Facebook AI Similarity Search
- **Index Types**: Flat (exact), IVF, HNSW (approximate)
- **Distance Metrics**: L2 (Euclidean), IP (cosine)
- **Collections**: Multiple isolated vector stores
- **Persistence**: Save/load to disk

### Python Libraries
- **transformers**: HuggingFace transformers
- **torch**: PyTorch for BERT
- **sentence-transformers**: Semantic embeddings
- **scikit-learn**: Similarity calculations
- **numpy, pandas**: Data processing

### Future Stack
- **Vector DB**: Chroma/Pinecone/FAISS
- **Advanced RAG**: LangChain/LlamaIndex
- **OCR**: Tesseract for scanned documents

## 📚 Documentation

- **[QUICK_START.md](QUICK_START.md)** - Get started in 5 minutes
- **[FEATURES.md](FEATURES.md)** - Chat features and model comparisons
- **[DOCUMENT_PROCESSING.md](DOCUMENT_PROCESSING.md)** - Complete document processing guide
- **[VECTOR_DATABASE.md](VECTOR_DATABASE.md)** - FAISS vector database guide
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - What was built
- **[NEXT_STEPS.md](NEXT_STEPS.md)** - What to do next

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone repository
git clone <your-fork-url>
cd "NEW RAG"

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env  # Edit with your API key

# Run app
streamlit run app.py
```

## 🐛 Known Issues

- **API Key Issues**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **BERT Model Download**: First run requires internet connection
- **Memory Usage**: Large documents (>100 pages) need 2GB+ RAM

## 🗺️ Roadmap

### Phase 1: Foundation ✅ (Completed)
- ✅ Multi-model chat interface
- ✅ Document upload and processing
- ✅ BERT-based semantic chunking
- ✅ Document library and management

### Phase 2: RAG Integration ✅ (Completed!)
- ✅ FAISS vector database integration
- ✅ RAG-enhanced chat responses
- ✅ Context retrieval from documents
- ✅ Source attribution
- ✅ Collection management
- ✅ Vector DB viewer

### Phase 3: Advanced Features 🔮 (Planned)
- 📋 Multi-document Q&A
- 📋 Conversation memory across sessions
- 📋 Advanced filtering and search
- 📋 Custom RAG strategies
- 📋 API endpoints for external use

### Phase 4: Production Ready 🔮 (Future)
- 📋 User authentication
- 📋 Document collaboration
- 📋 Cloud deployment
- 📋 Performance optimization
- 📋 Monitoring and analytics

## 📈 Performance

### Chat Performance
- **Response time**: 1-3 seconds (depends on model)
- **Streaming**: Real-time token-by-token
- **Concurrent users**: Limited by API rate limits

### Document Processing
- **Processing speed**: ~1 second per page
- **BERT loading**: ~10 seconds (first time only)
- **Memory usage**: ~500MB (MiniLM), ~1.5GB (MPNet)

### Recommended Hardware
- **CPU**: 4+ cores
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 1GB for models, more for documents
- **Internet**: Required for API and model downloads

## 📞 Support

- **Issues**: Open an issue on GitHub
- **Questions**: Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Cerebras API**: support@cerebras.ai

## 📝 License

This project is open source and available for personal and commercial use.

---

**Made with ❤️ using Cerebras AI and Streamlit**

⭐ Star this repository if you find it helpful!


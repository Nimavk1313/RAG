# 🚀 Quick Start Guide

Get up and running with the RAG Chat Assistant in 5 minutes!

## ⚡ Super Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up your API key (edit .env file)
# Add: CEREBRAS_API_KEY=your_key_here

# 3. Test connection
python check_api.py

# 4. Launch the app
streamlit run app.py
```

That's it! The app will open in your browser at `http://localhost:8501`

## 📝 Detailed Setup

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

**What gets installed:**
- Streamlit (web interface)
- Cerebras SDK (AI models)
- PyPDF2, python-docx (document loading)
- Transformers, sentence-transformers (BERT models)
- NumPy, pandas, scikit-learn (data processing)

**Note:** First run will download BERT models (~100MB). This is normal!

### Step 2: Configure API Key

Edit the `.env` file:

```
CEREBRAS_API_KEY=your_actual_api_key_here
```

**Get your API key:**
1. Visit https://cloud.cerebras.ai/
2. Sign up or log in
3. Navigate to API Keys section
4. Copy your key
5. Paste into `.env` file

### Step 3: Test Everything

Run the connection test:

```bash
python check_api.py
```

**Expected output:**
```
🔍 Checking Cerebras API Setup...
✅ .env file found
✅ API Key found: csk-xyz...
✅ Connection successful!
🎉 Your setup is ready!
```

If you see ❌ errors, check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### Step 4: Launch Application

```bash
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`

**See:**
- 💬 Chat interface (main page)
- 📄 Document Processing (left sidebar)
- 📚 Document Library (left sidebar)

## 🎯 First Time Usage

### Try the Chat (1 minute)

1. **Select a model** in the sidebar (default is fine)
2. **Type a message**: "Explain quantum computing in simple terms"
3. **Watch it stream** the response in real-time!

**Example prompts to try:**
- "Write a Python function to calculate fibonacci numbers"
- "Explain the difference between AI and machine learning"
- "Create a haiku about coding"

### Process a Document (2 minutes)

1. **Go to "📄 Document Processing"** (sidebar)
2. **Click "Initialize Processor"** (first time only - takes ~10 seconds)
3. **Upload a document** (PDF, DOCX, or TXT)
4. **Click "Process Document"**
5. **View the chunks** and statistics!

**Don't have a document?** Create a simple test file:

```bash
# Windows PowerShell
echo "Artificial intelligence is transforming technology. Machine learning enables computers to learn from data. Deep learning uses neural networks with multiple layers." > test.txt
```

Upload this `test.txt` file!

### Browse Your Documents (30 seconds)

1. **Go to "📚 Document Library"** (sidebar)
2. **See your processed document** listed
3. **Click to expand** and view chunks
4. **Download** or **delete** as needed

## 🎨 Interface Overview

```
┌─────────────────────────────────────────────────────┐
│  🤖 RAG Chat Assistant          [Sidebar Menu] ☰   │
├─────────────────────────────────────────────────────┤
│                                                     │
│  💬 Chat Interface                                  │
│  ┌───────────────────────────────────────────────┐ │
│  │ User: Hello!                                  │ │
│  │ AI: Hi! How can I help you today?            │ │
│  └───────────────────────────────────────────────┘ │
│  [Type your message here...] [Send]               │
│                                                     │
└─────────────────────────────────────────────────────┘

Sidebar Navigation:
├── 💬 RAG Chat Assistant (Home)
├── 📄 Document Processing
└── 📚 Document Library
```

## 💡 Pro Tips

### Chat Tips
- **Test Connection** before important chats
- **Switch models** for different tasks (fast vs quality)
- **Adjust temperature**:
  - 0.2-0.4 for factual/code
  - 0.7-0.9 for creative writing
- **Clear history** when changing topics

### Document Processing Tips
- **Use semantic chunking** for best RAG results
- **Keep chunks 500-1000 chars** (default is perfect)
- **Process documents before** you need them
- **Search chunks** to test semantic matching
- **Export processed docs** for backup

### Performance Tips
- **First BERT load** takes ~10 seconds (one-time)
- **Processing speed**: ~1 second per page
- **Large PDFs** (100+ pages) take 1-2 minutes
- **Use MiniLM** for speed, **MPNet** for quality

## 🚨 Common Issues

### "Cloudflare blocking detected"
→ Your API key is invalid. Get a new one from https://cloud.cerebras.ai/

### "Model not found" / "Failed to download"
→ First run needs internet to download BERT model. Wait patiently!

### "Out of memory"
→ Close other apps, or use smaller chunk sizes

### "File upload failed"
→ Check file format (PDF, DOCX, TXT only) and size (< 50MB)

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more help!

## 📚 Next Steps

**Learn More:**
- [FEATURES.md](FEATURES.md) - All chat features and models
- [DOCUMENT_PROCESSING.md](DOCUMENT_PROCESSING.md) - Deep dive into processing
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Fix common issues

**Try Advanced Features:**
- Change BERT models for different languages
- Experiment with chunking methods
- Search within documents semantically
- Export and analyze processed data

**Coming Soon:**
- RAG-enhanced chat (chat with your documents!)
- Vector database integration
- Multi-document Q&A
- Source citations

## 🎉 You're Ready!

You now have a powerful RAG system running locally!

**What you can do:**
- ✅ Chat with 12+ AI models
- ✅ Process and chunk documents
- ✅ Search documents semantically
- ✅ Build towards full RAG system

**Questions?** Check the documentation or create an issue!

Happy chatting! 🚀


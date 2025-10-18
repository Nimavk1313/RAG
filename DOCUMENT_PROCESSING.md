# 📄 Document Processing System

Complete guide to the BERT-based document processing system for RAG.

## 🎯 Overview

The document processing system transforms raw documents into semantically meaningful chunks using BERT embeddings. This prepares documents for efficient retrieval in RAG (Retrieval-Augmented Generation) applications.

## 🏗️ Architecture

```
Document Processing Pipeline:
┌─────────────┐     ┌─────────────┐     ┌──────────────┐
│   Document  │────▶│  Document   │────▶│   Semantic   │
│   Upload    │     │   Loader    │     │   Chunker    │
└─────────────┘     └─────────────┘     └──────────────┘
                                               │
                                               ▼
┌─────────────┐     ┌─────────────┐     ┌──────────────┐
│   Storage   │◀────│  Processor  │◀────│    BERT      │
│  (JSON)     │     │ Orchestrator│     │  Embeddings  │
└─────────────┘     └─────────────┘     └──────────────┘
```

## 📦 Components

### 1. Document Loader (`document_loader.py`)

Handles loading various document formats:

**Supported Formats:**
- 📕 PDF (.pdf)
- 📘 Word Documents (.docx, .doc)
- 📄 Text Files (.txt)
- 📊 CSV Files (.csv)

**Features:**
- Automatic format detection
- Text extraction with error handling
- Metadata collection (file size, word count, etc.)
- UTF-8 and Latin-1 encoding support
- CSV structured data extraction (columns and rows)

**Usage:**
```python
from src.processing.document_loader import DocumentLoader

loader = DocumentLoader()

# Load PDF
doc_data = loader.load_file("document.pdf")
print(doc_data['text'])

# Load CSV
csv_data = loader.load_file("data.csv")
# CSV is converted to structured text:
# Row 1:
# Column1: Value1
# Column2: Value2
print(csv_data['text'])
```

### 2. Semantic Chunker (`semantic_chunker.py`)

Uses BERT embeddings to create semantically meaningful chunks.

**BERT Models Available:**
- `all-MiniLM-L6-v2` (Fast, 384 dimensions) ⭐ Default
- `all-mpnet-base-v2` (High quality, 768 dimensions)
- `paraphrase-multilingual-MiniLM-L12-v2` (Multilingual support)

**Chunking Methods:**

#### 1️⃣ Semantic Chunking (Recommended)
Groups text based on semantic similarity using BERT embeddings.

**How it works:**
1. Split text into sentences
2. Generate BERT embeddings for each sentence
3. Calculate cosine similarity between consecutive sentences
4. Group similar sentences together (above threshold)
5. Respect max/min chunk size limits

**Parameters:**
- `similarity_threshold` (0.0-1.0): Higher = more similar chunks (default: 0.5)
- `max_chunk_size`: Maximum characters per chunk (default: 1000)
- `min_chunk_size`: Minimum characters per chunk (default: 100)

**Best for:**
- Documents with varying topics
- RAG applications requiring precise semantic search
- Content with clear semantic boundaries

#### 2️⃣ Sentence Chunking
Groups complete sentences while respecting max chunk size.

**Best for:**
- Maintaining sentence integrity
- Documents where sentence boundaries are important
- General-purpose chunking

#### 3️⃣ Fixed-Size Chunking
Creates chunks of approximately equal size.

**Best for:**
- Uniform chunk distribution
- Simple processing pipelines
- Testing and benchmarking

**Usage:**
```python
from src.processing.semantic_chunker import SemanticChunker

chunker = SemanticChunker(
    model_name='all-MiniLM-L6-v2',
    similarity_threshold=0.5,
    max_chunk_size=1000,
    min_chunk_size=100
)

chunks = chunker.chunk_text(text, method='semantic')
```

### 3. Document Processor (`document_processor.py`)

Orchestrates the entire processing pipeline.

**Features:**
- End-to-end document processing
- Automatic storage of processed documents
- Document search and retrieval
- Statistics and analytics
- Semantic search within documents

**Usage:**
```python
from src.processing.document_processor import DocumentProcessor

processor = DocumentProcessor()

# Process a document
result = processor.process_document(
    "path/to/document.pdf",
    chunking_method="semantic"
)

# Search chunks
results = processor.search_chunks(result, "your query", top_k=5)

# Get statistics
stats = processor.get_document_stats(result)
```

## 🖥️ Web Interface

### Page 1: Document Processing

**Location:** `pages/1_📄_Document_Processing.py`

**Features:**
- 📤 Drag-and-drop file upload
- ⚙️ Configurable BERT model selection
- ✂️ Multiple chunking methods
- 📊 Real-time processing statistics
- 🔍 Semantic search within processed documents
- 📥 Export results (JSON)
- 📄 Chunk viewer with pagination

**Workflow:**
1. Configure processing parameters in sidebar
2. Initialize BERT model (first time only)
3. Upload document (PDF, DOCX, or TXT)
4. Click "Process Document"
5. View chunks and statistics
6. Download results or search chunks

### Page 2: Document Library

**Location:** `pages/2_📚_Document_Library.py`

**Features:**
- 📚 Browse all processed documents
- 🔍 Search by filename
- 🗂️ Filter by chunking method
- 📊 Document statistics
- 👁️ Preview chunks
- 📥 Download documents
- 🗑️ Delete documents

## 📊 Output Format

Processed documents are saved as JSON files in `data/processed/` with the following structure:

```json
{
  "metadata": {
    "filename": "example.pdf",
    "file_path": "data/documents/example.pdf",
    "file_type": ".pdf",
    "file_size": 102400,
    "processed_at": "2024-01-15T10:30:00",
    "chunking_method": "semantic",
    "total_chunks": 25,
    "total_words": 5000,
    "total_chars": 30000
  },
  "chunks": [
    {
      "chunk_id": 0,
      "text": "This is the first chunk...",
      "embedding": [0.123, -0.456, ...],
      "sentence_count": 3,
      "char_count": 250,
      "word_count": 45
    },
    ...
  ]
}
```

## 🎛️ Configuration Guide

### Choosing Chunking Method

| Use Case | Recommended Method | Reasoning |
|----------|-------------------|-----------|
| General RAG | Semantic | Best semantic coherence |
| Q&A Systems | Semantic | Precise context matching |
| Summarization | Sentence | Maintains sentence boundaries |
| Embedding Storage | Fixed | Consistent sizes |
| Testing | Fixed | Predictable output |

### Tuning Parameters

**Similarity Threshold:**
- **0.3-0.4**: More chunks, very fine-grained
- **0.5-0.6**: Balanced (recommended)
- **0.7-0.8**: Fewer, larger chunks

**Chunk Size:**
- **Small (200-500)**: More granular, slower retrieval
- **Medium (500-1000)**: Balanced (recommended)
- **Large (1000-2000)**: Less granular, faster retrieval

**BERT Model:**
- **MiniLM**: Fast, good for most use cases ⭐
- **MPNet**: Better quality, 2x slower
- **Multilingual**: Non-English content

## 🚀 Performance

### Processing Speed

| Document Size | Method | MiniLM | MPNet |
|--------------|--------|--------|-------|
| 10 pages | Semantic | ~10s | ~20s |
| 50 pages | Semantic | ~45s | ~90s |
| 100 pages | Semantic | ~90s | ~180s |

*Tested on CPU. GPU acceleration significantly faster.*

### Memory Usage

| BERT Model | RAM Usage |
|------------|-----------|
| MiniLM | ~500 MB |
| MPNet | ~1.5 GB |
| Multilingual | ~1 GB |

## 🔍 Search Capabilities

The system supports semantic search within processed documents:

```python
# Search for relevant chunks
results = processor.search_chunks(
    processed_doc,
    query="machine learning concepts",
    top_k=5
)

# Results include similarity scores
for result in results:
    print(f"Similarity: {result['similarity']:.3f}")
    print(f"Text: {result['text']}")
```

## 💡 Best Practices

### 1. Document Preparation
- ✅ Clean, well-formatted documents work best
- ✅ Remove unnecessary headers/footers
- ✅ Ensure proper text encoding
- ❌ Avoid scanned PDFs (OCR required first)

### 2. Chunking Strategy
- Start with semantic chunking (default settings)
- Adjust similarity threshold based on results
- Keep chunks between 500-1000 characters
- Test with sample documents first

### 3. Storage Management
- Processed files include large embeddings
- One 100-page document ≈ 5-10 MB JSON
- Regularly clean old processed files
- Consider compression for long-term storage

### 4. BERT Model Selection
- Use MiniLM for development/testing
- Switch to MPNet for production (better quality)
- Use multilingual for non-English content
- Model loaded once and cached

## 🔧 Troubleshooting

### Issue: "Model download taking too long"
**Solution:** First run downloads BERT model (~100MB). Subsequent runs use cached model.

### Issue: "Out of memory error"
**Solution:** 
- Use smaller chunks (reduce max_chunk_size)
- Use MiniLM instead of MPNet
- Process smaller documents
- Close other applications

### Issue: "Too many/few chunks"
**Solution:**
- Too many: Increase similarity threshold or max chunk size
- Too few: Decrease similarity threshold or max chunk size

### Issue: "Poor semantic grouping"
**Solution:**
- Try different BERT model (MPNet for better quality)
- Adjust similarity threshold
- Consider sentence chunking for structured docs

### Issue: "PDF text extraction failed"
**Solution:**
- Ensure PDF has selectable text (not scanned image)
- Try different PDF library
- Convert to DOCX or TXT first

## 📈 Future Enhancements

Planned features:
- 🔮 Vector database integration (Chroma, Pinecone)
- 🌐 Multi-language support
- 📊 Advanced analytics dashboard
- 🤖 Automatic parameter tuning
- 🔗 Chunk relationship mapping
- 📸 OCR for scanned documents
- 🎯 Custom chunking strategies
- ⚡ GPU acceleration support

## 📚 References

- **Sentence Transformers**: https://www.sbert.net/
- **BERT Paper**: https://arxiv.org/abs/1810.04805
- **Semantic Search**: https://www.pinecone.io/learn/semantic-search/

## 🤝 Contributing

To add new features:
1. Add functionality to appropriate module
2. Update tests
3. Update documentation
4. Submit pull request

## 📄 License

Part of the RAG Chat Assistant project.


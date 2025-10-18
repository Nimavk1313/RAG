

# 🗄️ FAISS Vector Database Guide

Complete guide to the FAISS vector database integration for RAG.

## 🎯 Overview

The FAISS (Facebook AI Similarity Search) vector database stores document embeddings for fast similarity search. This enables efficient retrieval of relevant context for RAG (Retrieval-Augmented Generation) applications.

## 🏗️ Architecture

```
RAG System with FAISS:
┌─────────────┐     ┌──────────────┐     ┌───────────────┐
│  Document   │────▶│ BERT Semantic │────▶│  Embeddings   │
│  Processing │     │   Chunking    │     │  (384/768-dim)│
└─────────────┘     └──────────────┘     └───────────────┘
                                                   │
                                                   ▼
┌─────────────┐     ┌──────────────┐     ┌───────────────┐
│   User      │────▶│  Query       │────▶│  FAISS Index  │
│   Query     │     │  Embedding   │     │  (Similarity) │
└─────────────┘     └──────────────┘     └───────────────┘
                                                   │
                                                   ▼
┌─────────────┐     ┌──────────────┐     ┌───────────────┐
│  Cerebras   │◀────│  Augmented   │◀────│  Top-K        │
│  LLM        │     │  Prompt      │     │  Chunks       │
└─────────────┘     └──────────────┘     └───────────────┘
```

## 📦 Components

### 1. Vector Store (`vector_store.py`)

Core FAISS wrapper handling vector operations.

**Features:**
- Multiple index types (Flat, IVF, HNSW)
- L2 and Inner Product (cosine) similarity
- Metadata storage with vectors
- Save/load to disk
- Document grouping and filtering

**Usage:**
```python
from src.retrieval.vector_store import FAISSVectorStore

# Create store
store = FAISSVectorStore(
    dimension=384,  # MiniLM dimension
    index_type="Flat",  # Exact search
    metric="L2"  # Euclidean distance
)

# Add vectors
embeddings = model.encode(texts)  # shape: (n, 384)
metadata = [{"text": t, "doc_id": "doc1"} for t in texts]
store.add_vectors(embeddings, metadata, doc_id="doc1")

# Search
query_emb = model.encode(["your query"])
results = store.search(query_emb, k=5)

# Save
store.save("data/vector_db/my_collection")
```

### 2. Vector DB Manager (`vector_db_manager.py`)

Manages multiple FAISS collections.

**Features:**
- Create/delete collections
- List all collections
- Load/save collections
- Add documents to collections
- Search across collections
- Statistics and monitoring

**Usage:**
```python
from src.retrieval.vector_db_manager import VectorDBManager

manager = VectorDBManager()

# Create collection
collection = manager.create_collection(
    name="my_docs",
    dimension=384,
    description="My document collection"
)

# Add document
manager.add_document(
    collection_name="my_docs",
    doc_id="example.pdf",
    chunks=processed_chunks  # from document processor
)

# Search
results = manager.search(
    collection_name="my_docs",
    query_embedding=query_vector,
    k=5
)

# Save
manager.save_collection("my_docs")
```

## 🚀 FAISS Index Types

### 1. **Flat** (Default - Recommended for Start)
- **Type**: Exact search, brute force
- **Speed**: Slowest
- **Accuracy**: 100% (exact)
- **Best for**: < 10K vectors, when accuracy is critical
- **Memory**: Highest

**When to use:**
- Small to medium collections
- Need perfect accuracy
- Development and testing

### 2. **IVF** (Inverted File Index)
- **Type**: Approximate search with clustering
- **Speed**: Fast
- **Accuracy**: 95-99% (configurable)
- **Best for**: 10K - 1M vectors
- **Memory**: Medium

**When to use:**
- Large collections
- Can sacrifice small accuracy for speed
- Production with many documents

### 3. **HNSW** (Hierarchical Navigable Small World)
- **Type**: Graph-based approximate search
- **Speed**: Fastest
- **Accuracy**: 95-99%
- **Best for**: Very large collections (> 100K vectors)
- **Memory**: Higher (stores graph)

**When to use:**
- Very large collections
- Need very fast search
- Production with high throughput

## 🎛️ Configuration Guide

### Choosing Index Type

| Collection Size | Recommended Index | Why |
|----------------|-------------------|-----|
| < 1,000 vectors | Flat | Fast enough, perfect accuracy |
| 1K - 10K | Flat | Still manageable, exact search |
| 10K - 100K | IVF | Good balance speed/accuracy |
| 100K - 1M | IVF or HNSW | HNSW for speed, IVF for memory |
| > 1M | HNSW | Best for very large scale |

### Distance Metrics

**L2 (Euclidean Distance):**
- Default choice
- Measures geometric distance
- Good for general use
- Lower distance = more similar

**Inner Product (IP):**
- For cosine similarity (with normalized vectors)
- Better for text embeddings
- Higher score = more similar
- Use when vectors are normalized

**Recommendation:** Use L2 for simplicity, IP for slightly better text search.

### Dimension Selection

| BERT Model | Dimension | Speed | Quality |
|-----------|-----------|-------|---------|
| all-MiniLM-L6-v2 | 384 | Fast | Good |
| all-mpnet-base-v2 | 768 | Medium | Better |
| bert-base-uncased | 768 | Medium | Good |

**Tip:** Dimension must match the BERT model used for chunking!

## 📊 Collection Management

### Creating Collections

```python
# Via code
manager.create_collection(
    name="research_papers",
    dimension=384,
    index_type="Flat",
    metric="L2",
    description="Academic research papers"
)

# Via UI
# 1. Go to Vector Database page
# 2. Click "Create Collection" in sidebar
# 3. Enter name and settings
# 4. Click "Create"
```

### Adding Documents

Documents are automatically added when processing:

1. Go to **Document Processing** page
2. Check "Add to FAISS Vector Database"
3. Select collection (or create new)
4. Process document
5. Chunks are automatically embedded and stored

### Searching Collections

```python
# Search entire collection
results = manager.search(
    collection_name="research_papers",
    query_embedding=query_vector,
    k=5  # top 5 results
)

# Search within specific document
results = manager.search(
    collection_name="research_papers",
    query_embedding=query_vector,
    k=5,
    filter_doc_id="paper1.pdf"
)
```

## 🎯 RAG Chat Usage

The RAG Chat page automatically:

1. **Encodes your query** with BERT
2. **Searches vector database** for relevant chunks
3. **Retrieves top-K most similar** chunks
4. **Augments the prompt** with retrieved context
5. **Generates response** using Cerebras LLM
6. **Shows sources** used for the answer

### RAG Chat Flow

```
User Query → BERT Encoding → FAISS Search → Top-K Chunks
     ↓
Context + Query → Augmented Prompt → Cerebras LLM → Answer + Sources
```

### Example Interaction

**User:** "What is machine learning?"

**System Process:**
1. Encodes query to vector
2. Searches vector DB, finds 3 relevant chunks:
   - Chunk from "AI_basics.pdf" (similarity: 0.89)
   - Chunk from "ML_intro.txt" (similarity: 0.85)
   - Chunk from "DL_guide.pdf" (similarity: 0.78)
3. Adds chunks as context to prompt
4. LLM generates answer based on context
5. Shows answer + sources

**Response:** "Based on the documents, machine learning is... [Context 1 indicates...]"

## 💾 Storage and Persistence

### File Structure

```
data/vector_db/
├── collections.json          # Collection metadata
├── my_collection/
│   ├── index.faiss          # FAISS index file
│   ├── metadata.pkl         # Chunk metadata
│   └── stats.json           # Collection statistics
└── another_collection/
    ├── index.faiss
    ├── metadata.pkl
    └── stats.json
```

### Saving Collections

```python
# Manual save
manager.save_collection("my_collection")

# Automatic save
# Collections are automatically saved after adding documents
# via the Document Processing page
```

### Loading Collections

```python
# Auto-load (lazy loading)
collection = manager.get_collection("my_collection")  # Loads from disk if needed

# Manual load
collection = FAISSVectorStore.load("data/vector_db/my_collection")
```

## 📈 Performance

### Search Speed

| Index Type | Collection Size | Search Time (ms) |
|-----------|----------------|------------------|
| Flat | 1K vectors | < 1 ms |
| Flat | 10K vectors | < 10 ms |
| Flat | 100K vectors | ~100 ms |
| IVF | 100K vectors | ~5-10 ms |
| HNSW | 1M vectors | ~1-5 ms |

*Tested on CPU, GPU significantly faster*

### Memory Usage

**Index Memory:**
- Flat: `dimension × num_vectors × 4 bytes`
- Example: 100K vectors × 384 dim = ~150 MB

**Metadata Memory:**
- ~1-2 KB per chunk (text + metadata)
- Example: 100K chunks = ~100-200 MB

**Total for 100K vectors (384-dim):**
- Index: ~150 MB
- Metadata: ~150 MB
- Total: ~300 MB

### Scalability

| Scale | Vectors | Documents | Index Size | Recommended Setup |
|-------|---------|-----------|-----------|-------------------|
| Small | < 10K | < 100 | < 50 MB | Flat, single machine |
| Medium | 10K-100K | 100-1K | 50-500 MB | IVF, single machine |
| Large | 100K-1M | 1K-10K | 500MB-5GB | HNSW, powerful machine |
| Very Large | > 1M | > 10K | > 5 GB | Distributed FAISS |

## 🛠️ Best Practices

### 1. Collection Organization

**By Domain:**
```
- technical_docs
- research_papers
- company_policies
- customer_support
```

**By Project:**
```
- project_alpha
- project_beta
- general_knowledge
```

### 2. Naming Conventions

- Use lowercase with underscores: `my_collection`
- Be descriptive: `research_papers_2024`
- Avoid special characters

### 3. Document IDs

- Use unique, descriptive IDs
- Include file extension: `report.pdf`
- Add metadata: `2024_Q1_report.pdf`

### 4. Index Type Selection

Start with Flat, upgrade when needed:
```
1. Flat (< 10K vectors) - Start here
2. IVF (10K-100K) - Upgrade for speed
3. HNSW (> 100K) - For very large scale
```

### 5. Search Parameters

**Top-K Selection:**
- Too few (k=1-2): Might miss context
- Sweet spot (k=3-5): Good balance
- Too many (k>10): Noise, slower

**Recommendation:** Start with k=3-5

### 6. Regular Maintenance

- Save collections after updates
- Monitor collection sizes
- Archive old documents
- Rebuild indices periodically

## 🔍 Troubleshooting

### Issue: "Index dimension mismatch"
**Solution:** BERT model dimension must match collection dimension
- MiniLM: 384
- MPNet/BERT-base: 768

### Issue: "Collection not found"
**Solution:** 
- Check spelling
- Ensure collection was saved
- Check `data/vector_db/collections.json`

### Issue: "Out of memory"
**Solution:**
- Use IVF instead of Flat
- Reduce max_chunk_size
- Process fewer documents
- Increase system RAM

### Issue: "Search is slow"
**Solution:**
- Upgrade to IVF or HNSW
- Reduce collection size
- Use faster hardware
- Consider GPU

### Issue: "Poor search results"
**Solution:**
- Ensure BERT model matches at query and index time
- Try different chunking method
- Adjust chunk size
- Check embedding quality

## 📚 Advanced Features

### 1. Filtering by Document

```python
# Only search within specific document
results = manager.search(
    collection_name="my_collection",
    query_embedding=query_vector,
    k=5,
    filter_doc_id="specific_doc.pdf"
)
```

### 2. Batch Processing

```python
# Process multiple documents
for file in document_files:
    result = processor.process_document(file)
    manager.add_document(
        collection_name="bulk_import",
        doc_id=file.name,
        chunks=result['chunks']
    )
```

### 3. Collection Statistics

```python
stats = manager.get_collection_stats("my_collection")
print(f"Vectors: {stats['total_vectors']}")
print(f"Documents: {stats['total_documents']}")
```

### 4. Document Removal

```python
# Mark document as deleted
collection = manager.get_collection("my_collection")
collection.remove_document("old_doc.pdf")
manager.save_collection("my_collection")
```

*Note: FAISS doesn't support true deletion, vectors are marked as deleted*

## 🎓 Learning Resources

- **FAISS Documentation**: https://github.com/facebookresearch/faiss
- **FAISS Tutorial**: https://github.com/facebookresearch/faiss/wiki/Getting-started
- **Sentence Transformers**: https://www.sbert.net/
- **RAG Paper**: https://arxiv.org/abs/2005.11401

## 🔗 Integration with Other Components

### With Document Processing
```
Document Processing → Chunks with Embeddings → FAISS Storage
```

### With RAG Chat
```
User Query → BERT Encoding → FAISS Search → Context Retrieval → LLM Response
```

### With Document Library
```
Document Library → View Documents → Link to Vector DB → Show Embeddings
```

## 📈 Roadmap

### Current Features ✅
- FAISS vector storage
- Multiple index types
- Collection management
- Document filtering
- Save/load persistence

### Coming Soon 🔮
- GPU acceleration
- Distributed FAISS for massive scale
- Advanced filtering (metadata, date, etc.)
- Vector compression for smaller storage
- Incremental index updates
- Approximate nearest neighbor tuning

## 💡 Tips for Success

1. **Start Small**: Begin with Flat index and 1-2 documents
2. **Test Queries**: Try various queries to tune k parameter
3. **Monitor Performance**: Track search times and adjust
4. **Regular Backups**: Save collections frequently
5. **Clean Data**: Better chunking = better retrieval
6. **Experiment**: Try different BERT models and settings

---

**🎉 You now have a production-ready FAISS vector database for RAG!**



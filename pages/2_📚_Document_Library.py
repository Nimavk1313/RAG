"""
Document Library Page
View and manage all processed documents
"""
import streamlit as st
import sys
from pathlib import Path
import json
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.processing.document_processor import DocumentProcessor

# Page configuration
st.set_page_config(
    page_title="Document Library",
    page_icon="📚",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .doc-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .metric-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📚 Document Library")
st.markdown("Browse and manage all your processed documents")

# Initialize processor
@st.cache_resource
def get_processor():
    return DocumentProcessor()

processor = get_processor()

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filters")
    
    chunking_methods = st.multiselect(
        "Chunking Method:",
        ["semantic", "sentence", "fixed"],
        default=["semantic", "sentence", "fixed"]
    )
    
    st.divider()
    
    st.subheader("🔄 Actions")
    if st.button("♻️ Refresh Library"):
        st.cache_resource.clear()
        st.rerun()

# Get all processed documents
processed_docs = processor.list_processed_documents()

# Filter by chunking method
filtered_docs = [
    doc for doc in processed_docs 
    if doc['chunking_method'] in chunking_methods
]

# Display statistics
st.header("📊 Library Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Documents", len(processed_docs))
with col2:
    total_chunks = sum(doc['total_chunks'] for doc in processed_docs)
    st.metric("Total Chunks", f"{total_chunks:,}")
with col3:
    if filtered_docs:
        avg_chunks = sum(doc['total_chunks'] for doc in filtered_docs) / len(filtered_docs)
        st.metric("Avg Chunks per Doc", f"{avg_chunks:.0f}")
    else:
        st.metric("Avg Chunks per Doc", "N/A")

st.divider()

# Display documents
if not filtered_docs:
    st.info("📭 No processed documents found. Process some documents first!")
    if st.button("➡️ Go to Document Processing"):
        st.switch_page("pages/1_📄_Document_Processing.py")
else:
    st.header(f"📄 Documents ({len(filtered_docs)})")
    
    # Search bar
    search_query = st.text_input(
        "🔍 Search documents by filename",
        placeholder="Type to search..."
    )
    
    if search_query:
        filtered_docs = [
            doc for doc in filtered_docs 
            if search_query.lower() in doc['filename'].lower()
        ]
    
    # Sort options
    col1, col2 = st.columns([3, 1])
    with col2:
        sort_by = st.selectbox(
            "Sort by:",
            ["Date (Newest)", "Date (Oldest)", "Filename", "Chunks"]
        )
    
    # Apply sorting
    if sort_by == "Date (Newest)":
        filtered_docs.sort(key=lambda x: x['processed_at'], reverse=True)
    elif sort_by == "Date (Oldest)":
        filtered_docs.sort(key=lambda x: x['processed_at'])
    elif sort_by == "Filename":
        filtered_docs.sort(key=lambda x: x['filename'])
    elif sort_by == "Chunks":
        filtered_docs.sort(key=lambda x: x['total_chunks'], reverse=True)
    
    # Display documents
    for i, doc_info in enumerate(filtered_docs):
        with st.expander(f"📄 {doc_info['filename']} - {doc_info['total_chunks']} chunks"):
            # Load full document
            try:
                full_doc = processor.load_processed_document(doc_info['file_path'])
                metadata = full_doc['metadata']
                chunks = full_doc['chunks']
                
                # Document details
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("### 📋 Document Information")
                    st.markdown(f"**Filename:** {metadata['filename']}")
                    st.markdown(f"**File Type:** {metadata['file_type']}")
                    st.markdown(f"**File Size:** {metadata['file_size'] / 1024:.2f} KB")
                    st.markdown(f"**Chunking Method:** {metadata['chunking_method']}")
                    
                    # Parse and format date
                    try:
                        processed_time = datetime.fromisoformat(metadata['processed_at'])
                        formatted_time = processed_time.strftime("%Y-%m-%d %H:%M:%S")
                        st.markdown(f"**Processed:** {formatted_time}")
                    except:
                        st.markdown(f"**Processed:** {metadata['processed_at']}")
                
                with col2:
                    st.markdown("### 📊 Statistics")
                    st.metric("Total Chunks", metadata['total_chunks'])
                    st.metric("Total Words", f"{metadata['total_words']:,}")
                    st.metric("Total Chars", f"{metadata['total_chars']:,}")
                
                st.divider()
                
                # Chunk statistics
                stats = processor.get_document_stats(full_doc)
                
                st.markdown("### 📈 Chunk Statistics")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Min Size", f"{stats['min_chunk_size']} chars")
                with col2:
                    st.metric("Avg Size", f"{stats['avg_chunk_size']:.0f} chars")
                with col3:
                    st.metric("Max Size", f"{stats['max_chunk_size']} chars")
                
                st.divider()
                
                # Sample chunks
                st.markdown("### 📝 Sample Chunks")
                
                num_samples = min(3, len(chunks))
                st.caption(f"Showing first {num_samples} chunks (of {len(chunks)} total)")
                
                for j in range(num_samples):
                    chunk = chunks[j]
                    with st.container():
                        st.markdown(f"**Chunk {j+1}** ({chunk['word_count']} words)")
                        st.text_area(
                            "Chunk text",
                            value=chunk['text'][:300] + "..." if len(chunk['text']) > 300 else chunk['text'],
                            height=100,
                            key=f"doc_{i}_chunk_{j}",
                            label_visibility="collapsed"
                        )
                
                st.divider()
                
                # Actions
                st.markdown("### 🔧 Actions")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # Download button
                    doc_json = json.dumps(full_doc, indent=2)
                    st.download_button(
                        "📥 Download Full Document",
                        data=doc_json,
                        file_name=f"{metadata['filename']}_processed.json",
                        mime="application/json",
                        key=f"download_doc_{i}"
                    )
                
                with col2:
                    # View all chunks button
                    if st.button("👁️ View All Chunks", key=f"view_chunks_{i}"):
                        st.session_state[f"show_all_chunks_{i}"] = True
                
                with col3:
                    # Delete button
                    if st.button("🗑️ Delete Document", key=f"delete_{i}"):
                        try:
                            Path(doc_info['file_path']).unlink()
                            st.success("✅ Document deleted!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error deleting: {str(e)}")
                
                # Show all chunks if requested
                if st.session_state.get(f"show_all_chunks_{i}", False):
                    st.markdown("### 📚 All Chunks")
                    
                    for j, chunk in enumerate(chunks):
                        with st.expander(f"Chunk {j+1} ({chunk['word_count']} words)"):
                            st.text_area(
                                "Full chunk text",
                                value=chunk['text'],
                                height=200,
                                key=f"doc_{i}_full_chunk_{j}"
                            )
                            
                            st.caption(f"Characters: {chunk['char_count']} | Sentences: {chunk['sentence_count']}")
                    
                    if st.button("🔼 Hide All Chunks", key=f"hide_chunks_{i}"):
                        st.session_state[f"show_all_chunks_{i}"] = False
                        st.rerun()
            
            except Exception as e:
                st.error(f"❌ Error loading document: {str(e)}")

# Footer
st.divider()
st.caption("💡 Documents are stored in `data/processed/` directory")



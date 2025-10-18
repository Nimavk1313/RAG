"""
Document Processing Page
Upload and process documents with BERT-based semantic chunking
"""
import streamlit as st
import os
import sys
from pathlib import Path
import json
import time

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.processing.document_processor import DocumentProcessor
from src.retrieval.vector_db_manager import VectorDBManager

# Page configuration
st.set_page_config(
    page_title="Document Processing",
    page_icon="📄",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .upload-box {
        border: 2px dashed #4CAF50;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background-color: #f8f9fa;
    }
    .chunk-box {
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: #f9f9f9;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'processor' not in st.session_state:
    st.session_state.processor = None
    st.session_state.processed_doc = None
    st.session_state.processing_status = None
    st.session_state.vector_db_manager = VectorDBManager()
    st.session_state.add_to_vector_db = True

# Title
st.title("📄 Document Processing System")
st.markdown("Upload documents and process them using **BERT-based semantic chunking**")

# Sidebar - Processing Configuration
with st.sidebar:
    st.header("⚙️ Processing Configuration")
    
    st.subheader("🤖 BERT Model")
    bert_model = st.selectbox(
        "Select BERT Model:",
        [
            "all-MiniLM-L6-v2",  # Fast, good quality
            "all-mpnet-base-v2",  # Better quality, slower
            "paraphrase-multilingual-MiniLM-L12-v2",  # Multilingual
        ],
        help="Sentence transformer model for embeddings"
    )
    
    st.subheader("✂️ Chunking Method")
    chunking_method = st.radio(
        "Choose chunking strategy:",
        ["semantic", "sentence", "fixed"],
        help="""
        - Semantic: Groups text by semantic similarity (recommended)
        - Sentence: Groups sentences respecting max size
        - Fixed: Fixed-size chunks
        """
    )
    
    st.subheader("📏 Chunk Parameters")
    
    similarity_threshold = st.slider(
        "Semantic Similarity Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.05,
        help="Higher = more similar chunks"
    )
    
    max_chunk_size = st.number_input(
        "Max Chunk Size (characters)",
        min_value=200,
        max_value=2000,
        value=1000,
        step=100
    )
    
    min_chunk_size = st.number_input(
        "Min Chunk Size (characters)",
        min_value=50,
        max_value=500,
        value=100,
        step=50
    )
    
    st.divider()
    
    st.subheader("🗄️ Vector Database")
    
    # Add to vector DB option
    st.session_state.add_to_vector_db = st.checkbox(
        "Add to FAISS Vector Database",
        value=st.session_state.add_to_vector_db,
        help="Automatically add processed chunks to vector database for RAG"
    )
    
    # Collection selection
    if st.session_state.add_to_vector_db:
        collections = st.session_state.vector_db_manager.list_collections()
        collection_names = [c['name'] for c in collections]
        
        if not collection_names:
            collection_names = ["default"]
        
        selected_collection = st.selectbox(
            "Collection:",
            options=collection_names,
            help="Select or create a collection"
        )
        
        # Create new collection option
        with st.expander("➕ Create New Collection"):
            new_collection_name = st.text_input("Collection Name")
            new_collection_desc = st.text_input("Description (optional)")
            
            if st.button("Create Collection"):
                if new_collection_name:
                    try:
                        # Get dimension based on BERT model
                        dimension = 384 if "MiniLM" in bert_model else 768
                        
                        st.session_state.vector_db_manager.create_collection(
                            name=new_collection_name,
                            dimension=dimension,
                            description=new_collection_desc
                        )
                        st.success(f"✅ Created collection: {new_collection_name}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                else:
                    st.warning("⚠️ Please enter a collection name")
    
    st.divider()
    
    # Initialize processor button
    if st.button("🔧 Initialize Processor"):
        with st.spinner("Initializing BERT model..."):
            try:
                st.session_state.processor = DocumentProcessor(
                    bert_model=bert_model,
                    similarity_threshold=similarity_threshold,
                    max_chunk_size=max_chunk_size,
                    min_chunk_size=min_chunk_size
                )
                st.success("✅ Processor initialized!")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📤 Upload Document")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a document file",
        type=['pdf', 'docx', 'txt', 'doc', 'csv'],
        help="Supported formats: PDF, DOCX, TXT, CSV"
    )
    
    if uploaded_file is not None:
        # Display file info
        file_details = {
            "Filename": uploaded_file.name,
            "File Type": uploaded_file.type,
            "File Size": f"{uploaded_file.size / 1024:.2f} KB"
        }
        
        st.json(file_details)
        
        # Save uploaded file
        upload_dir = Path("data/documents")
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_path = upload_dir / uploaded_file.name
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"✅ File saved to {file_path}")
        
        # Process button
        if st.button("🚀 Process Document", type="primary"):
            if st.session_state.processor is None:
                st.warning("⚠️ Please initialize the processor first (sidebar)")
            else:
                # Process document
                with st.spinner("Processing document..."):
                    try:
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        status_text.text("📖 Loading document...")
                        progress_bar.progress(25)
                        time.sleep(0.5)
                        
                        status_text.text("✂️ Chunking text...")
                        progress_bar.progress(50)
                        
                        result = st.session_state.processor.process_document(
                            str(file_path),
                            chunking_method=chunking_method
                        )
                        
                        status_text.text("💾 Saving results...")
                        progress_bar.progress(75)
                        
                        # Add to vector database if enabled
                        if st.session_state.add_to_vector_db:
                            try:
                                status_text.text("🗄️ Adding to vector database...")
                                
                                # Ensure collection exists
                                collection = st.session_state.vector_db_manager.get_collection(
                                    selected_collection,
                                    auto_load=True
                                )
                                
                                if collection is None:
                                    # Create default collection
                                    dimension = 384 if "MiniLM" in bert_model else 768
                                    st.session_state.vector_db_manager.create_collection(
                                        name=selected_collection,
                                        dimension=dimension,
                                        description="Default collection"
                                    )
                                
                                # Add document to vector DB
                                doc_id = uploaded_file.name
                                st.session_state.vector_db_manager.add_document(
                                    collection_name=selected_collection,
                                    doc_id=doc_id,
                                    chunks=result['chunks']
                                )
                                
                                # Save collection
                                st.session_state.vector_db_manager.save_collection(selected_collection)
                                
                                st.info(f"✅ Added to vector database: {selected_collection}")
                                
                            except Exception as e:
                                st.warning(f"⚠️ Vector DB error: {str(e)}")
                        
                        time.sleep(0.5)
                        
                        st.session_state.processed_doc = result
                        
                        progress_bar.progress(100)
                        status_text.text("✅ Processing complete!")
                        
                        st.balloons()
                        st.success(f"🎉 Successfully created {len(result['chunks'])} chunks!")
                        
                    except Exception as e:
                        st.error(f"❌ Error processing document: {str(e)}")
                        st.exception(e)

with col2:
    st.subheader("📊 Processing Status")
    
    if st.session_state.processor is not None:
        st.success("✅ Processor Ready")
        st.info(f"🤖 Model: {bert_model}")
        st.info(f"✂️ Method: {chunking_method}")
    else:
        st.warning("⚠️ Processor Not Initialized")
        st.info("👈 Configure and initialize in sidebar")
    
    st.divider()
    
    st.subheader("📈 Supported Formats")
    st.markdown("""
    - 📕 PDF (.pdf)
    - 📘 Word (.docx, .doc)
    - 📄 Text (.txt)
    - 📊 CSV (.csv)
    """)

# Display processed results
if st.session_state.processed_doc is not None:
    st.divider()
    st.header("📊 Processing Results")
    
    doc = st.session_state.processed_doc
    metadata = doc['metadata']
    chunks = doc['chunks']
    
    # Statistics
    st.subheader("📈 Document Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Chunks", metadata['total_chunks'])
    with col2:
        st.metric("Total Words", f"{metadata['total_words']:,}")
    with col3:
        st.metric("Total Characters", f"{metadata['total_chars']:,}")
    with col4:
        avg_chunk_size = metadata['total_chars'] / metadata['total_chunks']
        st.metric("Avg Chunk Size", f"{avg_chunk_size:.0f}")
    
    # Chunk statistics
    if st.session_state.processor:
        stats = st.session_state.processor.get_document_stats(doc)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Min Chunk Size", f"{stats['min_chunk_size']} chars")
        with col2:
            st.metric("Avg Chunk Size", f"{stats['avg_chunk_size']:.0f} chars")
        with col3:
            st.metric("Max Chunk Size", f"{stats['max_chunk_size']} chars")
    
    st.divider()
    
    # Chunk viewer
    st.subheader("📝 Chunk Viewer")
    
    # Search functionality
    search_query = st.text_input(
        "🔍 Search chunks (semantic search)",
        placeholder="Enter search query..."
    )
    
    if search_query and st.session_state.processor:
        st.info("🔍 Searching with semantic similarity...")
        search_results = st.session_state.processor.search_chunks(
            doc, search_query, top_k=5
        )
        
        st.success(f"Found {len(search_results)} relevant chunks")
        
        for i, chunk in enumerate(search_results):
            with st.expander(f"🎯 Result {i+1} - Similarity: {chunk['similarity']:.3f}"):
                st.markdown(f"**Chunk ID:** {chunk['chunk_id']}")
                st.markdown(f"**Word Count:** {chunk['word_count']}")
                st.markdown(f"**Character Count:** {chunk['char_count']}")
                st.markdown("**Text:**")
                st.text_area(
                    "Chunk text",
                    value=chunk['text'],
                    height=150,
                    key=f"search_chunk_{i}",
                    label_visibility="collapsed"
                )
    else:
        # Display all chunks
        st.info(f"Displaying all {len(chunks)} chunks")
        
        # Pagination
        chunks_per_page = 5
        total_pages = (len(chunks) + chunks_per_page - 1) // chunks_per_page
        
        page = st.number_input(
            "Page",
            min_value=1,
            max_value=total_pages,
            value=1,
            step=1
        )
        
        start_idx = (page - 1) * chunks_per_page
        end_idx = min(start_idx + chunks_per_page, len(chunks))
        
        st.caption(f"Showing chunks {start_idx + 1} to {end_idx} of {len(chunks)}")
        
        for i in range(start_idx, end_idx):
            chunk = chunks[i]
            with st.expander(f"📄 Chunk {i + 1} ({chunk['word_count']} words, {chunk['char_count']} chars)"):
                st.markdown(f"**Chunk ID:** {chunk['chunk_id']}")
                st.markdown(f"**Sentences:** {chunk['sentence_count']}")
                st.markdown("**Text:**")
                st.text_area(
                    "Chunk text",
                    value=chunk['text'],
                    height=150,
                    key=f"chunk_{i}",
                    label_visibility="collapsed"
                )
                
                # Download chunk button
                chunk_json = json.dumps(chunk, indent=2)
                st.download_button(
                    "📥 Download Chunk",
                    data=chunk_json,
                    file_name=f"chunk_{i+1}.json",
                    mime="application/json",
                    key=f"download_{i}"
                )
    
    st.divider()
    
    # Download processed document
    st.subheader("💾 Export Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Download full processed document
        doc_json = json.dumps(doc, indent=2)
        st.download_button(
            "📥 Download Full Document (JSON)",
            data=doc_json,
            file_name=f"{metadata['filename']}_processed.json",
            mime="application/json",
            help="Download all chunks with embeddings"
        )
    
    with col2:
        # Download metadata only
        metadata_json = json.dumps(metadata, indent=2)
        st.download_button(
            "📥 Download Metadata Only",
            data=metadata_json,
            file_name=f"{metadata['filename']}_metadata.json",
            mime="application/json",
            help="Download document metadata without chunks"
        )

# Footer
st.divider()
st.caption("💡 Tip: Use semantic chunking for better RAG performance")



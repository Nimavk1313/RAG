"""
Vector Database Management
View and manage FAISS vector database collections
"""
import streamlit as st
import sys
from pathlib import Path
import json

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.retrieval.vector_db_manager import VectorDBManager

# Page configuration
st.set_page_config(
    page_title="Vector Database",
    page_icon="🗄️",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .collection-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🗄️ Vector Database Management")
st.markdown("Manage your FAISS vector database collections")

# Initialize vector DB manager
if 'vector_db_manager' not in st.session_state:
    st.session_state.vector_db_manager = VectorDBManager()

manager = st.session_state.vector_db_manager

# Sidebar
with st.sidebar:
    st.header("🔧 Actions")
    
    # Create new collection
    with st.expander("➕ Create Collection"):
        new_name = st.text_input("Collection Name")
        new_desc = st.text_area("Description")
        
        col1, col2 = st.columns(2)
        with col1:
            dimension = st.selectbox(
                "Dimension",
                options=[384, 768, 1024],
                index=0,
                help="384: MiniLM, 768: MPNet/BERT-base"
            )
        
        with col2:
            index_type = st.selectbox(
                "Index Type",
                options=["Flat", "IVF", "HNSW"],
                help="Flat: Exact, IVF: Fast approximate, HNSW: Fastest"
            )
        
        if st.button("Create"):
            if new_name:
                try:
                    manager.create_collection(
                        name=new_name,
                        dimension=dimension,
                        index_type=index_type,
                        description=new_desc
                    )
                    st.success(f"✅ Created: {new_name}")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("Please enter a name")
    
    st.divider()
    
    if st.button("🔄 Refresh"):
        st.cache_resource.clear()
        st.rerun()

# Get all collections
collections = manager.list_collections()

# Statistics overview
st.header("📊 Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Collections", len(collections))

with col2:
    total_docs = sum(c['total_documents'] for c in collections)
    st.metric("Total Documents", f"{total_docs:,}")

with col3:
    total_vectors = sum(c['total_vectors'] for c in collections)
    st.metric("Total Vectors", f"{total_vectors:,}")

st.divider()

# Collections list
if not collections:
    st.info("📭 No collections found. Create one or process documents to get started!")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Process Documents"):
            st.switch_page("pages/1_📄_Document_Processing.py")
    with col2:
        if st.button("🎯 Start RAG Chat"):
            st.switch_page("pages/3_🎯_RAG_Chat.py")
else:
    st.header(f"📚 Collections ({len(collections)})")
    
    # Collection tabs
    for i, collection_info in enumerate(collections):
        with st.expander(f"🗄️ {collection_info['name']} - {collection_info['total_vectors']} vectors"):
            # Collection details
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("### 📋 Information")
                st.markdown(f"**Name:** {collection_info['name']}")
                st.markdown(f"**Description:** {collection_info.get('description', 'No description')}")
                st.markdown(f"**Index Type:** {collection_info['index_type']}")
                st.markdown(f"**Dimension:** {collection_info['dimension']}")
                st.markdown(f"**Status:** {'🟢 Loaded' if collection_info['loaded'] else '⚪ On Disk'}")
                
                # Format dates
                try:
                    from datetime import datetime
                    created = datetime.fromisoformat(collection_info['created_at'])
                    updated = datetime.fromisoformat(collection_info['last_updated'])
                    st.markdown(f"**Created:** {created.strftime('%Y-%m-%d %H:%M')}")
                    st.markdown(f"**Last Updated:** {updated.strftime('%Y-%m-%d %H:%M')}")
                except:
                    st.markdown(f"**Created:** {collection_info['created_at']}")
                    st.markdown(f"**Last Updated:** {collection_info['last_updated']}")
            
            with col2:
                st.markdown("### 📊 Statistics")
                st.metric("Documents", collection_info['total_documents'])
                st.metric("Vectors", collection_info['total_vectors'])
                
                if collection_info['total_vectors'] > 0:
                    avg_per_doc = collection_info['total_vectors'] / max(collection_info['total_documents'], 1)
                    st.metric("Avg Chunks/Doc", f"{avg_per_doc:.1f}")
            
            st.divider()
            
            # Load collection details
            try:
                collection = manager.get_collection(collection_info['name'])
                
                if collection:
                    st.markdown("### 📄 Documents in Collection")
                    
                    documents = collection.list_documents()
                    
                    if documents:
                        st.info(f"Found {len(documents)} documents")
                        
                        # Display documents
                        for doc_id in documents:
                            with st.container():
                                doc_chunks = collection.get_document_chunks(doc_id)
                                
                                col1, col2, col3 = st.columns([3, 1, 1])
                                
                                with col1:
                                    st.markdown(f"**📄 {doc_id}**")
                                
                                with col2:
                                    st.caption(f"{len(doc_chunks)} chunks")
                                
                                with col3:
                                    if st.button("🔍 View", key=f"view_{collection_info['name']}_{doc_id}"):
                                        st.session_state[f"show_chunks_{collection_info['name']}_{doc_id}"] = True
                                
                                # Show chunks if requested
                                if st.session_state.get(f"show_chunks_{collection_info['name']}_{doc_id}", False):
                                    st.markdown("**Sample Chunks:**")
                                    
                                    # Show first 3 chunks
                                    for j, chunk in enumerate(doc_chunks[:3]):
                                        st.text_area(
                                            f"Chunk {j+1}",
                                            value=chunk['text'][:200] + "..." if len(chunk['text']) > 200 else chunk['text'],
                                            height=100,
                                            key=f"chunk_{collection_info['name']}_{doc_id}_{j}"
                                        )
                                    
                                    if len(doc_chunks) > 3:
                                        st.caption(f"... and {len(doc_chunks) - 3} more chunks")
                                    
                                    if st.button("🔼 Hide", key=f"hide_{collection_info['name']}_{doc_id}"):
                                        st.session_state[f"show_chunks_{collection_info['name']}_{doc_id}"] = False
                                        st.rerun()
                    else:
                        st.warning("No documents in this collection")
            
            except Exception as e:
                st.error(f"Error loading collection: {str(e)}")
            
            st.divider()
            
            # Actions
            st.markdown("### 🔧 Actions")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("🔄 Reload", key=f"reload_{i}"):
                    try:
                        manager.get_collection(collection_info['name'], auto_load=True)
                        st.success("✅ Reloaded!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            
            with col2:
                if st.button("💾 Save", key=f"save_{i}"):
                    try:
                        manager.save_collection(collection_info['name'])
                        st.success("✅ Saved!")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            
            with col3:
                # Export collection info
                export_data = {
                    'collection_info': collection_info,
                    'documents': collection.list_documents() if collection else []
                }
                
                st.download_button(
                    "📥 Export Info",
                    data=json.dumps(export_data, indent=2),
                    file_name=f"{collection_info['name']}_info.json",
                    mime="application/json",
                    key=f"export_{i}"
                )
            
            with col4:
                if st.button("🗑️ Delete", key=f"delete_{i}", type="secondary"):
                    if st.session_state.get(f"confirm_delete_{i}", False):
                        try:
                            manager.delete_collection(collection_info['name'])
                            st.success("✅ Deleted!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                    else:
                        st.session_state[f"confirm_delete_{i}"] = True
                        st.warning("⚠️ Click again to confirm deletion")

# Footer
st.divider()
st.caption("💡 FAISS Vector Database - Fast similarity search for RAG")



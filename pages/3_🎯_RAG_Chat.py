"""
RAG Chat Interface
Chat with AI using context retrieved from vector database
"""
import streamlit as st
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.retrieval.vector_db_manager import VectorDBManager
from src.processing.semantic_chunker import SemanticChunker
from cerebras.cloud.sdk import Cerebras
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="RAG Chat",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .context-box {
        background-color: #f0f8ff;
        border-left: 4px solid #4CAF50;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .source-badge {
        display: inline-block;
        background: #4CAF50;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 12px;
        font-size: 0.8rem;
        margin: 0.2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Cerebras client
@st.cache_resource
def get_cerebras_client():
    api_key = os.environ.get("CEREBRAS_API_KEY")
    if not api_key:
        st.error("⚠️ CEREBRAS_API_KEY not found!")
        st.stop()
    return Cerebras(api_key=api_key)

try:
    client = get_cerebras_client()
except Exception as e:
    st.error(f"Failed to initialize Cerebras: {str(e)}")
    st.stop()

# Initialize session state
if 'rag_messages' not in st.session_state:
    st.session_state.rag_messages = []

if 'vector_db_manager' not in st.session_state:
    st.session_state.vector_db_manager = VectorDBManager()

if 'bert_model' not in st.session_state:
    st.session_state.bert_model = None

if 'selected_rag_model' not in st.session_state:
    st.session_state.selected_rag_model = "Qwen 3 235B (A22B)"

if 'rag_temperature' not in st.session_state:
    st.session_state.rag_temperature = 0.7

if 'top_k_chunks' not in st.session_state:
    st.session_state.top_k_chunks = 5

if 'min_similarity' not in st.session_state:
    st.session_state.min_similarity = 0.3

if 'use_reranking' not in st.session_state:
    st.session_state.use_reranking = True

# Available models
CEREBRAS_MODELS = {
    "Llama 4 Scout 17B": "llama-4-scout-17b-16e-instruct",
    "Llama 3.3 70B": "llama-3.3-70b",
    "Llama 3.1 8B": "llama3.1-8b",
    "Llama 3.1 70B": "llama3.1-70b",
    "Qwen 3 235B (A22B)": "qwen-3-235b-a22b-instruct-2507",
    "Qwen 3 32B": "qwen-3-32b",
    "Qwen 2.5 7B": "qwen2.5-7b-instruct",
    "Qwen 2.5 32B": "qwen2.5-32b-instruct",
    "Gemma 2 9B": "gemma2-9b-it",
    "Mistral 7B": "mistral-7b-instruct-v0.2",
    "GPT OSS 120B": "gpt-oss-120b",
}

# Title
st.title("🎯 RAG Chat")
st.markdown("Chat with AI using context from your documents")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ RAG Configuration")
    
    # Vector database selection
    st.subheader("🗄️ Vector Database")
    
    collections = st.session_state.vector_db_manager.list_collections()
    
    if not collections:
        st.warning("⚠️ No collections found!")
        st.info("📄 Process documents first to create collections")
        if st.button("➡️ Go to Document Processing"):
            st.switch_page("pages/1_📄_Document_Processing.py")
        st.stop()
    
    collection_names = [c['name'] for c in collections]
    selected_collection = st.selectbox(
        "Select Collection:",
        options=collection_names,
        help="Choose which document collection to use for context"
    )
    
    # Display collection stats
    if selected_collection:
        collection_info = next((c for c in collections if c['name'] == selected_collection), None)
        if collection_info:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Documents", collection_info['total_documents'])
            with col2:
                st.metric("Chunks", collection_info['total_vectors'])
    
    st.divider()
    
    # Retrieval settings
    st.subheader("🔍 Retrieval Settings")
    
    st.session_state.top_k_chunks = st.slider(
        "Top K Chunks",
        min_value=1,
        max_value=10,
        value=st.session_state.top_k_chunks,
        help="Number of relevant chunks to retrieve (more = more context)"
    )
    
    st.session_state.min_similarity = st.slider(
        "Min Similarity Threshold",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.min_similarity,
        step=0.05,
        help="Filter out chunks below this similarity (higher = more strict)"
    )
    
    st.session_state.use_reranking = st.checkbox(
        "Use Reranking",
        value=st.session_state.use_reranking,
        help="Rerank chunks by relevance to question (recommended)"
    )
    
    filter_by_doc = st.checkbox(
        "Filter by specific document",
        value=False,
        help="Only search within a specific document"
    )
    
    selected_doc = None
    if filter_by_doc:
        # Get list of documents in collection
        try:
            collection = st.session_state.vector_db_manager.get_collection(selected_collection)
            if collection:
                docs = collection.list_documents()
                if docs:
                    selected_doc = st.selectbox("Document:", docs)
                else:
                    st.warning("No documents in collection")
        except Exception as e:
            st.error(f"Error loading documents: {str(e)}")
    
    st.divider()
    
    # Model selection
    st.subheader("🤖 Model Settings")
    
    model_choice = st.selectbox(
        "Cerebras Model:",
        options=list(CEREBRAS_MODELS.keys()),
        index=list(CEREBRAS_MODELS.keys()).index(st.session_state.selected_rag_model),
    )
    
    if model_choice != st.session_state.selected_rag_model:
        st.session_state.selected_rag_model = model_choice
    
    st.session_state.rag_temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.rag_temperature,
        step=0.1
    )
    
    st.divider()
    
    # Actions
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.rag_messages = []
        st.rerun()

# Initialize BERT model for query embedding
@st.cache_resource
def get_bert_model(model_name="all-MiniLM-L6-v2"):
    return SemanticChunker(model_name=model_name)

if st.session_state.bert_model is None:
    with st.spinner("Loading BERT model for query embedding..."):
        st.session_state.bert_model = get_bert_model()

# Display chat history
for message in st.session_state.rag_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Display sources if available
        if "sources" in message and message["sources"]:
            with st.expander(f"📚 View Sources ({len(message['sources'])} chunks used)", expanded=False):
                for i, source in enumerate(message['sources']):
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            if 'doc_id' in source:
                                st.markdown(f"**📄 {source['doc_id']}**")
                        with col2:
                            # Show rerank score if available
                            score = source.get('rerank_score', source['similarity'])
                            st.caption(f"Relevance: {score:.1%}")
                        
                        st.text_area(
                            f"Context {i+1}",
                            value=source['text'],
                            height=120,
                            key=f"source_{message.get('msg_id', 0)}_{i}",
                            label_visibility="collapsed"
                        )
                        
                        if i < len(message['sources']) - 1:
                            st.divider()

# Chat input
if prompt := st.chat_input("Ask a question about your documents..."):
    # Add user message
    st.session_state.rag_messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        sources_placeholder = st.empty()
        
        try:
            # 1. Retrieve relevant context
            with st.spinner("🔍 Searching for relevant context..."):
                # Encode query with BERT
                query_embedding = st.session_state.bert_model.model.encode(prompt)
                
                # Search vector database (get more for reranking)
                initial_k = st.session_state.top_k_chunks * 2 if st.session_state.use_reranking else st.session_state.top_k_chunks
                results = st.session_state.vector_db_manager.search(
                    collection_name=selected_collection,
                    query_embedding=query_embedding.tolist(),
                    k=initial_k,
                    filter_doc_id=selected_doc
                )
                
                # Filter by minimum similarity
                results = [r for r in results if r['similarity'] >= st.session_state.min_similarity]
                
                # Rerank results if enabled
                if st.session_state.use_reranking and len(results) > st.session_state.top_k_chunks:
                    # Calculate relevance scores based on query-chunk similarity
                    for result in results:
                        # Simple reranking: combine vector similarity with text overlap
                        text_lower = result['text'].lower()
                        query_lower = prompt.lower()
                        query_words = set(query_lower.split())
                        chunk_words = set(text_lower.split())
                        
                        # Jaccard similarity for word overlap
                        if query_words and chunk_words:
                            overlap = len(query_words & chunk_words) / len(query_words | chunk_words)
                        else:
                            overlap = 0
                        
                        # Combined score: 70% vector similarity + 30% word overlap
                        result['rerank_score'] = 0.7 * result['similarity'] + 0.3 * overlap
                    
                    # Sort by rerank score and take top K
                    results.sort(key=lambda x: x.get('rerank_score', x['similarity']), reverse=True)
                    results = results[:st.session_state.top_k_chunks]
                
                # Limit to top K if not reranking
                elif len(results) > st.session_state.top_k_chunks:
                    results = results[:st.session_state.top_k_chunks]
            
            # 2. Build context from retrieved chunks
            if results:
                context_parts = []
                for i, result in enumerate(results):
                    # Add source information with context
                    doc_name = result.get('doc_id', 'Unknown')
                    similarity = result.get('rerank_score', result['similarity'])
                    context_parts.append(
                        f"[Source {i+1} from {doc_name} - Relevance: {similarity:.2f}]:\n{result['text']}"
                    )
                
                context = "\n\n---\n\n".join(context_parts)
                
                # Display retrieved context
                with sources_placeholder.expander(f"📚 Retrieved Context ({len(results)} chunks)", expanded=False):
                    for i, result in enumerate(results):
                        with st.container():
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                if 'doc_id' in result:
                                    st.markdown(f"**📄 {result['doc_id']}**")
                        with col2:
                            # Show rerank score if available
                            score = result.get('rerank_score', result['similarity'])
                            st.caption(f"Relevance: {score:.1%}")
                            
                            st.text_area(
                                f"Context {i+1}",
                                value=result['text'],
                                height=120,
                                key=f"retrieved_{i}",
                                label_visibility="collapsed"
                            )
                            
                            if i < len(results) - 1:
                                st.divider()
            else:
                context = "No relevant context found in the documents."
                st.warning("⚠️ No relevant context found. Answering without document context.")
            
            # 3. Build augmented prompt with better instructions
            system_prompt = f"""You are a helpful AI assistant that answers questions based ONLY on the provided context from documents.

CONTEXT FROM DOCUMENTS:
{context}

CRITICAL INSTRUCTIONS:
1. Answer ONLY using information from the context above
2. If the context doesn't contain the answer, clearly state: "The provided documents don't contain information about this topic."
3. Be accurate and precise - don't make up or infer information not in the context
4. Answer naturally without mentioning "Source 1", "Context", or document names in your response
5. If you use specific information, state it as fact (e.g., "According to the information provided..." or just state it directly)
6. Be comprehensive but concise
7. If multiple pieces of context support your answer, synthesize them into a coherent response
8. Do not add your own knowledge - stick strictly to the provided context

Remember: Your credibility depends on accuracy. Only use information from the context above."""
            
            # 4. Generate response with streaming
            full_response = ""
            
            stream = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Question: {prompt}\n\nPlease answer based on the provided context."}
                ],
                model=CEREBRAS_MODELS[st.session_state.selected_rag_model],
                stream=True,
                max_completion_tokens=2000,
                temperature=st.session_state.rag_temperature,
                top_p=0.9,  # Slightly lower for more focused responses
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
            # Save message with sources
            msg_id = len(st.session_state.rag_messages)
            st.session_state.rag_messages.append({
                "role": "assistant",
                "content": full_response,
                "sources": results if results else [],
                "msg_id": msg_id
            })
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            message_placeholder.markdown(error_msg)
            st.session_state.rag_messages.append({
                "role": "assistant",
                "content": error_msg
            })

# Information box at bottom
if not st.session_state.rag_messages:
    st.info("""
    💡 **RAG Chat with Enhanced Precision:**
    
    1. **Question Encoding** - Your question is converted to a vector using BERT
    2. **Smart Retrieval** - Top relevant chunks retrieved from FAISS database
    3. **Reranking** (if enabled) - Chunks reordered by relevance to your specific question
    4. **Filtering** - Only chunks above similarity threshold are used
    5. **Precise Generation** - AI answers ONLY from provided context
    6. **Source Attribution** - View exact chunks used below each response
    
    **Tips for best results:**
    - Increase Top-K for more comprehensive answers
    - Increase Min Similarity for more focused answers
    - Lower temperature (0.3-0.5) for factual questions
    - Enable reranking for better context selection
    """)



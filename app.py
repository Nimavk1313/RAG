import os
import streamlit as st
from cerebras.cloud.sdk import Cerebras
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Cerebras client
@st.cache_resource
def get_cerebras_client():
    cerebras_api_key = os.environ.get("CEREBRAS_API_KEY")
    if not cerebras_api_key:
        st.error("⚠️ CEREBRAS_API_KEY not found in environment variables!")
        st.stop()
    return Cerebras(api_key=cerebras_api_key)

try:
    client = get_cerebras_client()
except Exception as e:
    st.error(f"Failed to initialize Cerebras client: {str(e)}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="RAG Chat Assistant",
    page_icon="🤖",
    layout="wide"
)

# Available Cerebras models
CEREBRAS_MODELS = {
    # Llama Models
    "Llama 4 Scout 17B": "llama-4-scout-17b-16e-instruct",
    "Llama 3.3 70B": "llama-3.3-70b",
    "Llama 3.1 8B": "llama3.1-8b",
    "Llama 3.1 70B": "llama3.1-70b",
    
    # Qwen Models
    "Qwen 3 235B (A22B)": "qwen-3-235b-a22b-instruct-2507",
    "Qwen 3 32B": "qwen-3-32b",
    "Qwen 2.5 7B": "qwen2.5-7b-instruct",
    "Qwen 2.5 32B": "qwen2.5-32b-instruct",
    
    # Gemma Models
    "Gemma 2 9B": "gemma2-9b-it",
    
    # Mistral Models
    "Mistral 7B": "mistral-7b-instruct-v0.2",
    
    # Other Models
    "GPT OSS 120B": "gpt-oss-120b",
}

# Custom CSS for better UI
st.markdown("""
    <style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .main {
        max-width: 1200px;
        margin: 0 auto;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🤖 RAG Chat Assistant")
st.markdown("### 💬 Chat Interface")

# Welcome message for first-time users
if 'first_visit' not in st.session_state:
    st.session_state.first_visit = True

if st.session_state.first_visit:
    st.info("""
    👋 **Welcome to the RAG Chat Assistant!**
    
    This is a multi-page application:
    - **💬 This page**: Chat with multiple Cerebras models
    - **📄 Document Processing**: Upload and process documents with BERT-based semantic chunking
    - **📚 Document Library**: Browse and manage processed documents
    
    👈 Use the sidebar to navigate between pages!
    """)
    
    if st.button("Got it!"):
        st.session_state.first_visit = False
        st.rerun()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "Qwen 3 235B (A22B)"  # Default model

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7

if "top_p" not in st.session_state:
    st.session_state.top_p = 0.8

if "max_tokens" not in st.session_state:
    st.session_state.max_tokens = 20000

# Display current model in caption
st.caption(f"Powered by Cerebras • {st.session_state.selected_model}")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response with streaming
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Prepare messages for API
        api_messages = [
            {"role": "system", "content": "You are a helpful AI assistant. Provide clear, accurate, and concise responses."}
        ]
        api_messages.extend([
            {"role": m["role"], "content": m["content"]} 
            for m in st.session_state.messages
        ])
        
        # Stream response from Cerebras
        try:
            # Get the model ID from the selected model name
            selected_model_id = CEREBRAS_MODELS[st.session_state.selected_model]
            
            stream = client.chat.completions.create(
                messages=api_messages,
                model=selected_model_id,
                stream=True,
                max_completion_tokens=st.session_state.max_tokens,
                temperature=st.session_state.temperature,
                top_p=st.session_state.top_p
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            error_message = str(e)
            
            # Check for Cloudflare blocking
            if "cloudflare" in error_message.lower() or "<!DOCTYPE html>" in error_message:
                st.error("🚫 **Cloudflare Blocking Detected**")
                st.warning("""
                **Possible Solutions:**
                1. ⚠️ **Check API Key**: Your API key might be invalid or expired
                2. 🔄 **Try Again**: Wait a few moments and retry
                3. 🌐 **Network Issues**: Check your internet connection or try a different network
                4. 🔑 **Get New API Key**: Visit [Cerebras Cloud](https://cloud.cerebras.ai/) to verify or regenerate your API key
                5. 📧 **Contact Support**: Reach out to Cerebras support if the issue persists
                
                **Current API Key (first 10 chars):** `{}`
                """.format(os.environ.get("CEREBRAS_API_KEY", "")[:10] + "..."))
                full_response = "⚠️ Unable to connect to Cerebras API due to Cloudflare protection. Please check the error details above."
            else:
                st.error(f"❌ **Error:** {error_message[:200]}")
                full_response = "Sorry, I encountered an error. Please try again."
            
            message_placeholder.markdown(full_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Sidebar for settings and future RAG features
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Model Selection
    st.subheader("🤖 Model Selection")
    
    model_choice = st.selectbox(
        "Choose Model:",
        options=list(CEREBRAS_MODELS.keys()),
        index=list(CEREBRAS_MODELS.keys()).index(st.session_state.selected_model),
        help="Select which Cerebras model to use for chat"
    )
    
    # Update selected model if changed
    if model_choice != st.session_state.selected_model:
        st.session_state.selected_model = model_choice
        st.success(f"✅ Switched to {model_choice}")
        st.rerun()
    
    # Display model ID
    st.caption(f"Model ID: `{CEREBRAS_MODELS[st.session_state.selected_model]}`")
    
    # Advanced settings in expander
    with st.expander("⚙️ Advanced Settings"):
        st.session_state.temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.temperature,
            step=0.1,
            help="Controls randomness. Lower = more focused, Higher = more creative"
        )
        
        st.session_state.top_p = st.slider(
            "Top P",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.top_p,
            step=0.1,
            help="Controls diversity. Lower = more focused, Higher = more diverse"
        )
        
        st.session_state.max_tokens = st.number_input(
            "Max Tokens",
            min_value=100,
            max_value=20000,
            value=st.session_state.max_tokens,
            step=500,
            help="Maximum length of the response"
        )
    
    st.divider()
    
    # API Connection Test
    st.subheader("🔌 API Connection")
    
    current_api_key = os.environ.get("CEREBRAS_API_KEY", "")
    if current_api_key:
        st.success(f"✅ API Key: {current_api_key[:10]}...")
    else:
        st.error("❌ No API Key Found")
    
    if st.button("🧪 Test Connection"):
        with st.spinner(f"Testing connection with {st.session_state.selected_model}..."):
            try:
                test_model_id = CEREBRAS_MODELS[st.session_state.selected_model]
                test_stream = client.chat.completions.create(
                    messages=[{"role": "user", "content": "Hi"}],
                    model=test_model_id,
                    stream=True,
                    max_completion_tokens=10
                )
                # Try to get first chunk
                for chunk in test_stream:
                    st.success(f"✅ Connection successful with {st.session_state.selected_model}!")
                    break
            except Exception as e:
                error_msg = str(e)
                if "cloudflare" in error_msg.lower() or "<!DOCTYPE html>" in error_msg:
                    st.error("🚫 Cloudflare blocking detected")
                    st.info("Check your API key at [Cerebras Cloud](https://cloud.cerebras.ai/)")
                else:
                    st.error(f"❌ Connection failed: {error_msg[:100]}")
    
    st.divider()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    st.subheader("📊 Chat Stats")
    st.metric("Messages", len(st.session_state.messages))
    
    # Display current settings
    st.caption(f"🌡️ Temp: {st.session_state.temperature} | 🎲 Top-P: {st.session_state.top_p} | 📏 Max: {st.session_state.max_tokens}")
    
    st.divider()
    
    st.subheader("📄 Document System")
    st.info("Process and manage your documents")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Process Docs", use_container_width=True):
            st.switch_page("pages/1_📄_Document_Processing.py")
    with col2:
        if st.button("📚 Library", use_container_width=True):
            st.switch_page("pages/2_📚_Document_Library.py")
    
    st.divider()
    
    st.subheader("🎯 RAG System")
    st.info("RAG chat with FAISS vector database")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎯 RAG Chat", use_container_width=True):
            st.switch_page("pages/3_🎯_RAG_Chat.py")
    with col2:
        if st.button("🗄️ Vector DB", use_container_width=True):
            st.switch_page("pages/4_🗄️_Vector_Database.py")
    
    st.divider()
    
    st.caption("Complete RAG system with FAISS vector database")


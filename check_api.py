"""
Quick script to test your Cerebras API connection
Run this before starting the Streamlit app to verify your setup
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("🔍 Checking Cerebras API Setup...\n")

# Check if .env file exists
if os.path.exists(".env"):
    print("✅ .env file found")
else:
    print("❌ .env file not found - please create it with your API key")
    exit(1)

# Check if API key is set
api_key = os.environ.get("CEREBRAS_API_KEY")
if api_key:
    print(f"✅ API Key found: {api_key[:10]}...{api_key[-5:]}")
    print(f"   Length: {len(api_key)} characters")
else:
    print("❌ CEREBRAS_API_KEY not found in .env file")
    exit(1)

# Test connection
print("\n🧪 Testing connection to Cerebras API...")
try:
    from cerebras.cloud.sdk import Cerebras
    
    client = Cerebras(api_key=api_key)
    
    # Try a simple completion
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": "Say 'Connection successful!' and nothing else."}],
        model="qwen-3-235b-a22b-instruct-2507",
        stream=False,
        max_completion_tokens=50
    )
    
    print("✅ Connection successful!")
    print(f"   Response: {response.choices[0].message.content}")
    
    print("\n📋 Available Cerebras Models:")
    print("   • Llama 4 Scout 17B")
    print("   • Llama 3.3 70B, Llama 3.1 8B/70B")
    print("   • Qwen 3 235B (A22B) - Default")
    print("   • Qwen 3 32B, Qwen 2.5 7B/32B")
    print("   • Gemma 2 9B")
    print("   • Mistral 7B")
    print("   • GPT OSS 120B")
    
    print("\n🎉 Your setup is ready! You can now run: streamlit run app.py")
    
except ImportError:
    print("❌ Cerebras SDK not installed")
    print("   Run: pip install -r requirements.txt")
    exit(1)
except Exception as e:
    error_msg = str(e)
    print(f"❌ Connection failed!")
    
    if "cloudflare" in error_msg.lower() or "<!DOCTYPE html>" in error_msg:
        print("\n🚫 Cloudflare blocking detected!")
        print("   Possible issues:")
        print("   1. Invalid or expired API key")
        print("   2. Your IP address is blocked")
        print("   3. Network/firewall issues")
        print("\n   Solutions:")
        print("   • Get a new API key from: https://cloud.cerebras.ai/")
        print("   • Try a different network or disable VPN")
        print("   • Contact Cerebras support if issue persists")
    else:
        print(f"   Error: {error_msg[:200]}")
    
    print("\n📖 See TROUBLESHOOTING.md for more help")
    exit(1)


# Feature Documentation

## 🤖 Multi-Model Support

The RAG Chat Assistant now supports **12+ different Cerebras models**, allowing you to choose the best model for your specific use case.

### How to Use

1. **Select Model**: Use the dropdown in the sidebar under "🤖 Model Selection"
2. **View Model ID**: The actual API model ID is displayed below the selector
3. **Switch Anytime**: Change models mid-conversation (new model applies to future messages)
4. **Test Connection**: Use the "🧪 Test Connection" button to verify the selected model works

### Available Models

#### 🦙 Llama Models

| Model Name | Model ID | Best For |
|------------|----------|----------|
| Llama 4 Scout 17B | `llama-4-scout-17b-16e-instruct` | Latest Llama, balanced performance |
| Llama 3.3 70B | `llama-3.3-70b` | Large tasks, complex reasoning |
| Llama 3.1 8B | `llama3.1-8b` | Fast responses, simple tasks |
| Llama 3.1 70B | `llama3.1-70b` | Advanced reasoning, detailed responses |

#### 🎯 Qwen Models

| Model Name | Model ID | Best For |
|------------|----------|----------|
| Qwen 3 235B (A22B) | `qwen-3-235b-a22b-instruct-2507` | **Default** - Most capable, multilingual |
| Qwen 3 32B | `qwen-3-32b` | Balanced performance and speed |
| Qwen 2.5 7B | `qwen2.5-7b-instruct` | Fast, efficient for most tasks |
| Qwen 2.5 32B | `qwen2.5-32b-instruct` | Advanced tasks, good reasoning |

#### 💎 Other Models

| Model Name | Model ID | Best For |
|------------|----------|----------|
| Gemma 2 9B | `gemma2-9b-it` | Google's efficient model |
| Mistral 7B | `mistral-7b-instruct-v0.2` | Fast, good for general use |
| GPT OSS 120B | `gpt-oss-120b` | Large open-source GPT variant |

### Model Selection Tips

**For Quick Tasks**: Use smaller models (7B-17B)
- Mistral 7B
- Qwen 2.5 7B
- Llama 3.1 8B

**For Complex Reasoning**: Use larger models (70B+)
- Qwen 3 235B (A22B) ⭐ Recommended
- Llama 3.3 70B
- GPT OSS 120B

**For Balanced Use**: Medium models (17B-32B)
- Llama 4 Scout 17B
- Qwen 3 32B
- Qwen 2.5 32B

## ⚙️ Advanced Parameters

### Temperature

**Range**: 0.0 - 1.0 | **Default**: 0.7

Controls the randomness of responses:
- **0.0 - 0.3**: Very focused, deterministic (ideal for factual Q&A, code)
- **0.4 - 0.7**: Balanced creativity (good for general chat)
- **0.8 - 1.0**: More creative, varied (good for brainstorming, creative writing)

**Example Use Cases**:
- Code generation: 0.2
- General chat: 0.7
- Creative writing: 0.9

### Top P (Nucleus Sampling)

**Range**: 0.0 - 1.0 | **Default**: 0.8

Controls diversity by limiting token selection:
- **0.1 - 0.5**: Very focused, less diverse
- **0.6 - 0.9**: Balanced diversity
- **0.95 - 1.0**: Maximum diversity

**Tip**: Use lower top_p with higher temperature for controlled creativity.

### Max Tokens

**Range**: 100 - 20,000 | **Default**: 20,000

Maximum length of the response:
- **100-500**: Short, concise answers
- **500-2000**: Normal conversation responses
- **2000-10000**: Detailed explanations, long-form content
- **10000-20000**: Very long responses, essays, extensive code

**Note**: Longer max tokens don't mean longer responses, just a higher limit.

## 🔌 Connection Testing

The "🧪 Test Connection" button allows you to verify your API key and model availability:

1. Click the button in the sidebar
2. The app will send a minimal test request using your selected model
3. If successful, you'll see: "✅ Connection successful with [Model Name]!"
4. If it fails, you'll see specific error messages with solutions

**When to Use**:
- After changing your API key
- Before starting an important conversation
- When switching to a new model you haven't used before
- If you're experiencing connectivity issues

## 📊 Session State

Your settings are preserved during your chat session:
- Selected model
- Temperature setting
- Top P setting
- Max tokens setting
- Conversation history

**Note**: Settings reset when you close/refresh the browser tab.

## 🎨 UI Features

### Dynamic Model Display
The current model is always displayed in the app header:
> Powered by Cerebras • [Model Name]

### Current Settings Display
View your active parameters at a glance in the Chat Stats section:
> 🌡️ Temp: 0.7 | 🎲 Top-P: 0.8 | 📏 Max: 20000

### Model ID Visibility
The actual API model ID is shown below the model selector for transparency and debugging.

## 🚀 Performance Considerations

**Smaller Models (7B-17B)**:
- ⚡ Faster response times
- 💰 Lower cost (if applicable)
- 📊 Suitable for most tasks

**Larger Models (70B+)**:
- 🧠 Better reasoning
- 📚 More knowledge
- 🎯 Higher accuracy
- ⏱️ Slightly slower

## 💡 Best Practices

1. **Start with the default** (Qwen 3 235B) - it's the most capable
2. **Switch to smaller models** if you need faster responses
3. **Adjust temperature based on task**:
   - Factual tasks: Lower (0.2-0.4)
   - Creative tasks: Higher (0.7-0.9)
4. **Test your configuration** before important chats
5. **Clear chat history** when switching between very different tasks

## 🔮 Future Enhancements

Planned features for model selection:
- Model comparison mode (side-by-side responses)
- Per-model statistics (response times, tokens used)
- Favorite models quick-access
- Model recommendations based on query type
- Custom model presets (save temperature/top_p combinations)


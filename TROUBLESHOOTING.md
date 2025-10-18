# Troubleshooting Guide

## 🚫 Cloudflare Blocking Error

If you see a Cloudflare blocking error with HTML content, this means your request is being blocked before reaching the Cerebras API.

### Common Causes:

1. **Invalid or Expired API Key**
   - The API key in your `.env` file might be incorrect or expired
   - Solution: Get a new API key from [Cerebras Cloud](https://cloud.cerebras.ai/)

2. **IP Address Blocked**
   - Your IP address might be flagged by Cloudflare
   - Solution: Try from a different network or contact Cerebras support

3. **Rate Limiting**
   - Too many requests in a short time
   - Solution: Wait a few minutes before trying again

4. **VPN/Proxy Issues**
   - Some VPNs or proxies are blocked by Cloudflare
   - Solution: Disable VPN/proxy or try a different one

### How to Get a Valid API Key:

1. Visit [Cerebras Cloud](https://cloud.cerebras.ai/)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Generate a new API key
5. Copy the key and update your `.env` file:
   ```
   CEREBRAS_API_KEY=your_new_api_key_here
   ```
6. Restart the Streamlit app

### Testing Your Connection:

Use the "🧪 Test Connection" button in the sidebar to verify your API key works before sending messages.

### Still Having Issues?

1. **Check Python Version**: Ensure you're using Python 3.8 or higher
   ```bash
   python --version
   ```

2. **Reinstall Dependencies**: 
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **Check Environment Variables**:
   ```bash
   # Windows PowerShell
   Get-Content .env
   
   # Make sure the file shows your API key
   ```

4. **Verify SDK Installation**:
   ```bash
   pip show cerebras-cloud-sdk
   ```

5. **Contact Cerebras Support**: 
   - Email: support@cerebras.ai
   - Include the Cloudflare Ray ID from the error message

## Other Common Issues

### "ModuleNotFoundError: No module named 'cerebras'"
```bash
pip install cerebras-cloud-sdk
```

### "ModuleNotFoundError: No module named 'streamlit'"
```bash
pip install streamlit
```

### "No module named 'dotenv'"
```bash
pip install python-dotenv
```

### Port Already in Use
If port 8501 is already in use:
```bash
streamlit run app.py --server.port 8502
```

### Clear Cache
If you're experiencing weird behavior:
1. Click the menu (☰) in top right
2. Click "Clear Cache"
3. Or press `C` key in the app

## Need More Help?

- 📚 [Cerebras Documentation](https://docs.cerebras.ai/)
- 💬 [Cerebras Community](https://community.cerebras.ai/)
- 🐛 [Report Issues](https://github.com/cerebras/cerebras-cloud-sdk/issues)


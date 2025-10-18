# 🚀 Deployment Guide

Complete guide for deploying the RAG Chat Assistant.

## 📋 Prerequisites

- Python 3.8 or higher
- Git installed
- Cerebras API key (from https://cloud.cerebras.ai/)
- 4GB+ RAM recommended
- Internet connection (for BERT model download)

## 🖥️ Local Deployment

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/NEW-RAG.git
cd NEW-RAG
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

*Note: First run downloads BERT models (~100MB)*

### 3. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your API key
# CEREBRAS_API_KEY=your_actual_key_here
```

### 4. Test Setup

```bash
python check_api.py
```

### 5. Run Application

```bash
streamlit run app.py
```

App opens at `http://localhost:8501`

## ☁️ Cloud Deployment

### Streamlit Cloud (Recommended - Free)

**Steps:**

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to https://share.streamlit.io/
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file: `app.py`
   - Click "Deploy"

3. **Add Secrets:**
   - In Streamlit Cloud dashboard
   - Go to App Settings → Secrets
   - Add:
     ```toml
     CEREBRAS_API_KEY = "your_key_here"
     ```

**Pros:**
- ✅ Free tier available
- ✅ Easy deployment
- ✅ Auto-updates from GitHub
- ✅ Built-in secret management

**Cons:**
- ❌ Limited resources (1GB RAM)
- ❌ May sleep after inactivity
- ❌ Public by default

### Heroku

**Steps:**

1. **Install Heroku CLI**

2. **Create Procfile:**
   ```
   web: streamlit run app.py --server.port=$PORT
   ```

3. **Create runtime.txt:**
   ```
   python-3.11.0
   ```

4. **Deploy:**
   ```bash
   heroku login
   heroku create your-app-name
   heroku config:set CEREBRAS_API_KEY=your_key_here
   git push heroku main
   ```

**Pros:**
- ✅ More resources
- ✅ Custom domain
- ✅ Good reliability

**Cons:**
- ❌ Paid (free tier removed)
- ❌ More complex setup

### AWS EC2

**Steps:**

1. **Launch EC2 Instance:**
   - Ubuntu 22.04 LTS
   - t2.medium or larger
   - Open port 8501

2. **SSH and Setup:**
   ```bash
   ssh -i your-key.pem ubuntu@your-ip
   
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python
   sudo apt install python3-pip -y
   
   # Clone repo
   git clone https://github.com/YOUR_USERNAME/NEW-RAG.git
   cd NEW-RAG
   
   # Install dependencies
   pip3 install -r requirements.txt
   
   # Set environment variable
   echo "export CEREBRAS_API_KEY='your_key'" >> ~/.bashrc
   source ~/.bashrc
   ```

3. **Run with Screen:**
   ```bash
   screen -S rag-app
   streamlit run app.py --server.port=8501 --server.address=0.0.0.0
   # Detach with Ctrl+A, D
   ```

**Pros:**
- ✅ Full control
- ✅ High resources
- ✅ Custom configuration

**Cons:**
- ❌ Manual management
- ❌ Paid service
- ❌ Requires server knowledge

### Docker Deployment

**Create Dockerfile:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8501

# Run app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Build and Run:**

```bash
# Build image
docker build -t rag-chat-assistant .

# Run container
docker run -p 8501:8501 \
  -e CEREBRAS_API_KEY=your_key \
  -v $(pwd)/data:/app/data \
  rag-chat-assistant
```

**Docker Compose (docker-compose.yml):**

```yaml
version: '3.8'
services:
  rag-app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - CEREBRAS_API_KEY=${CEREBRAS_API_KEY}
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

Run: `docker-compose up -d`

## 🔒 Security Best Practices

### 1. Environment Variables

- ✅ Never commit `.env` file
- ✅ Use `.env.example` for template
- ✅ Use platform secrets management
- ✅ Rotate API keys regularly

### 2. Data Protection

- ✅ Add `.gitignore` for sensitive data
- ✅ Don't commit vector databases
- ✅ Don't commit uploaded documents
- ✅ Sanitize user inputs

### 3. Access Control

- ✅ Use authentication if public
- ✅ Rate limit API calls
- ✅ Monitor usage
- ✅ Set up logging

## 📊 Performance Optimization

### For Production:

1. **Use Gunicorn (optional):**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app
   ```

2. **Cache BERT Models:**
   - Pre-download models
   - Use persistent storage
   - Set `TRANSFORMERS_CACHE` env variable

3. **Vector Database:**
   - Use IVF or HNSW for large collections
   - Regular backups
   - Optimize index size

4. **Resource Limits:**
   - Set max file size
   - Limit concurrent users
   - Monitor memory usage

## 🔍 Monitoring

### Logs

```bash
# View Streamlit logs
streamlit run app.py 2>&1 | tee app.log
```

### Metrics to Track

- Response times
- API usage
- Error rates
- Memory usage
- Active users
- Document processing times

## 🐛 Troubleshooting

### Issue: Port already in use
```bash
# Change port
streamlit run app.py --server.port=8502
```

### Issue: Out of memory
```bash
# Use smaller BERT model
# Reduce max_chunk_size
# Limit concurrent processing
```

### Issue: Slow performance
```bash
# Use GPU if available
# Upgrade to IVF/HNSW index
# Increase instance size
```

## 🔄 Updates and Maintenance

### Update Application:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
streamlit run app.py
```

### Backup Data:

```bash
# Backup vector database
tar -czf vector_db_backup.tar.gz data/vector_db/

# Backup processed documents
tar -czf processed_backup.tar.gz data/processed/
```

## 📱 Mobile Optimization

Streamlit is responsive, but for better mobile experience:

1. Use `layout="wide"` selectively
2. Test on mobile devices
3. Optimize file upload sizes
4. Simplify complex layouts

## 🌐 Custom Domain

### With Streamlit Cloud:
- Upgrade to paid plan
- Configure custom domain in settings

### With Other Platforms:
1. Point domain to server IP
2. Set up SSL (Let's Encrypt)
3. Configure reverse proxy (nginx)
4. Update firewall rules

## 📈 Scaling

### Horizontal Scaling:
- Load balancer (nginx)
- Multiple app instances
- Shared vector database
- Session management

### Vertical Scaling:
- Increase server resources
- Better CPU/RAM
- SSD storage
- GPU for BERT

## 💰 Cost Estimation

### Streamlit Cloud:
- Free: 1 app, limited resources
- Team: $250/month (unlimited)

### AWS EC2:
- t2.medium: ~$30/month
- t2.large: ~$60/month

### Heroku:
- Basic: $7/month
- Standard: $25-50/month

### Self-hosted:
- VPS: $5-20/month
- Dedicated: $50-200/month

## ✅ Pre-Deployment Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] .env.example created
- [ ] .gitignore configured
- [ ] API keys secured
- [ ] Error handling tested
- [ ] Performance optimized
- [ ] Monitoring set up
- [ ] Backup strategy in place
- [ ] README updated

## 🆘 Support

- **Issues**: GitHub Issues
- **Documentation**: See README.md
- **Community**: GitHub Discussions

---

**Ready to deploy! Choose your platform and follow the guide above. 🚀**


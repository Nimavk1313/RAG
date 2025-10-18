# Contributing to RAG Chat Assistant

Thank you for your interest in contributing to the RAG Chat Assistant! 🎉

## 🚀 Getting Started

1. **Fork the repository**
2. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/NEW-RAG.git
   cd NEW-RAG
   ```

3. **Create a branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 🛠️ Development Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment:**
   ```bash
   cp .env.example .env
   # Add your Cerebras API key to .env
   ```

3. **Test your setup:**
   ```bash
   python check_api.py
   streamlit run app.py
   ```

## 📝 How to Contribute

### Reporting Bugs 🐛

- Use the GitHub Issues tab
- Describe the bug clearly
- Include steps to reproduce
- Provide error messages and logs
- Mention your environment (OS, Python version)

### Suggesting Features 💡

- Open a GitHub Issue
- Describe the feature and use case
- Explain why it would be valuable
- Include mockups or examples if applicable

### Submitting Code 🔧

1. **Make your changes:**
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation if needed

2. **Test your changes:**
   - Test locally with `streamlit run app.py`
   - Try different document types
   - Test RAG chat functionality

3. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```
   
   **Commit message format:**
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `style:` - Code style changes
   - `refactor:` - Code refactoring
   - `test:` - Test additions/changes
   - `chore:` - Maintenance tasks

4. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request:**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Describe your changes clearly
   - Reference any related issues

## 🎯 Areas for Contribution

### Easy (Good First Issues)
- Improve documentation
- Add more example documents
- Fix typos
- Update README with examples
- Add error message improvements

### Medium
- Add new document format support
- Improve UI/UX
- Add new BERT models
- Enhance chunking strategies
- Add export formats

### Advanced
- Implement hybrid search
- Add vector database backends (Pinecone, Chroma)
- Multi-language support
- Advanced RAG techniques
- Performance optimizations
- OCR for scanned documents

## 📋 Code Style

- **Python:** Follow PEP 8
- **Docstrings:** Use Google style
- **Type hints:** Add where helpful
- **Comments:** Explain "why", not "what"
- **Naming:** Descriptive and clear

## 🧪 Testing

- Test with different document types
- Verify RAG chat responses
- Check vector database operations
- Test error handling
- Verify UI responsiveness

## 📚 Documentation

When adding features:
- Update relevant .md files
- Add docstrings to functions
- Include usage examples
- Update README if needed

## ❓ Questions?

- Open a GitHub Discussion
- Comment on existing issues
- Check documentation first

## 🤝 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Provide constructive feedback
- Focus on the issue, not the person
- Keep discussions professional

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to RAG Chat Assistant! 🙏**


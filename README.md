# RBI Guidelines Chatbot

A comprehensive RAG (Retrieval-Augmented Generation) chatbot system for querying Reserve Bank of India (RBI) financial and operational risk guidelines. This system provides intelligent, context-aware responses with automatic source citations and professional compliance language.

## 🎯 Overview

This chatbot helps banking professionals, compliance officers, and financial analysts quickly access and understand RBI guidelines through natural language queries. The system processes RBI documents, creates embeddings, and provides accurate responses with proper citations.

## ✨ Features

- **Intelligent Document Processing**: Automatically processes and structures RBI guidelines
- **Vector Search**: ChromaDB-powered semantic search with MMR (Maximum Marginal Relevance)
- **Context-Aware Responses**: LangChain RAG pipeline with professional banking language
- **Automatic Citations**: Every response includes source references and document sections
- **Topic Classification**: Automatic categorization of content (risk assessment, compliance, etc.)
- **Conversation Tracking**: Maintains context across multiple questions
- **Knowledge Scope Validation**: Identifies out-of-scope queries with appropriate responses
- **Multiple LLM Support**: OpenAI GPT, Ollama (free local), and Hugging Face models

## 📊 System Architecture

```
RBI Documents → Document Processing → Vector Store (ChromaDB) → RAG Pipeline → Chatbot Interface
```

### Components:
1. **Document Processor**: Cleans and structures RBI guidelines
2. **Vector Store**: ChromaDB with sentence-transformer embeddings
3. **RAG System**: LangChain-based retrieval and generation
4. **Chatbot Interface**: User-friendly query interface

## 🚀 Quick Start

### Prerequisites

```bash
pip install pandas numpy chromadb sentence-transformers langchain langchain-community
pip install langchain-ollama  # For free local LLM option
```

### Setup

1. **Clone and prepare documents**:
   ```bash
   # Place your RBI documents in the project directory:
   # - operations risk (1).txt
   # - financial risk (1).txt
   ```

2. **Run the notebook**:
   ```bash
   jupyter notebook chatbot.ipynb
   ```

3. **Configure LLM (Optional)**:
   ```python
   # For OpenAI (requires API key)
   import os
   os.environ['OPENAI_API_KEY'] = 'your-api-key'
   
   # For free local option - install Ollama
   # Download from: https://ollama.com/download
   ```

## 💬 Usage

### Basic Query
```python
result = rbi_chatbot.ask("What are operational risk management requirements?")
print(result['response'])
```

### With Conversation Context
```python
result = rbi_chatbot.ask("How should banks handle this?", include_conversation_context=True)
```

### Check Sources
```python
for source in result['sources']:
    print(f"Source: {source['source']} - {source['section']}")
```

## 📚 Sample Questions

The chatbot can answer questions about:

- **Operational Risk**: "What are the board responsibilities for operational risk?"
- **Credit Risk**: "How should banks implement credit risk monitoring?"
- **Market Risk**: "What are the reporting requirements for market risk?"
- **Liquidity Risk**: "What compliance measures are required for liquidity risk?"
- **Technology Risk**: "How should banks handle technology failures?"
- **Capital Adequacy**: "What are the capital adequacy guidelines?"
- **Compliance**: "What are the regulatory reporting requirements?"

## 🔧 Configuration

### Vector Store Settings
- **Embedding Model**: `all-MiniLM-L6-v2`
- **Chunk Size**: 1000 characters
- **Overlap**: 200 characters
- **Search Type**: Maximum Marginal Relevance (MMR)

### Topic Categories
The system automatically tags content with:
- `risk_assessment`
- `policy_procedure`
- `capital_management`
- `monitoring_control`
- `compliance`
- `technology`
- `security_fraud`
- `liquidity`
- `credit_risk`
- `market_risk`

## 📁 Project Structure

```
├── chatbot.ipynb                    # Main notebook
├── operations risk (1).txt          # RBI operational risk guidelines
├── financial risk (1).txt           # RBI financial risk guidelines
├── rbi_guidelines_structured.json   # Processed document data
├── rbi_guidelines_analysis.csv      # Analysis data
├── vector_store_config.json         # Vector store configuration
├── rag_system_summary.json          # RAG system configuration
└── chroma_db/                       # ChromaDB persistent storage
```

## 🎛️ Advanced Features

### Knowledge Scope Validation
The chatbot identifies questions outside its knowledge domain:
```python
result = rbi_chatbot.ask("How do I bake a cake?")
# Returns: "Sorry, that's out of my knowledge scope! I can only answer questions related to RBI banking guidelines..."
```

### Conversation Analytics
```python
summary = rbi_chatbot.get_conversation_summary()
print(f"Total questions: {summary['total_questions']}")
print(f"Unique sources used: {summary['unique_sources']}")
```

### Filtered Search
```python
# Search specific document types
docs = rag_system.retriever.invoke("operational risk", 
                                  where={"document_type": "operational"})
```

## 🔄 Development Phases

### Phase 1: Data Processing ✅
- Document cleaning and structuring
- Text normalization and chunking
- Metadata extraction

### Phase 2: Vector Store & Embeddings ✅
- ChromaDB setup with persistent storage
- Sentence transformer embeddings
- Semantic search configuration

### Phase 3: RAG Pipeline ✅
- LangChain integration
- Prompt engineering for banking domain
- Response synthesis with citations
- Multi-LLM support

### Phase 4: Web Interface (Future)
- Streamlit web application
- User-friendly chat interface
- Export capabilities

## 🛠️ Technical Details

### Document Processing
- Regex-based section extraction
- Content cleaning and normalization
- Automatic metadata enhancement
- Quality validation

### Embedding Generation
- Batch processing for efficiency
- 384-dimensional embeddings
- Persistent storage in ChromaDB
- Metadata filtering support

### RAG Pipeline
- MMR-based retrieval for diversity
- Context-aware prompt templates
- Professional banking language
- Automatic citation generation

## 📊 Performance Metrics

- **Total Chunks**: 108 document segments
- **Embedding Dimensions**: 384
- **Average Chunk Size**: 150 words
- **Search Latency**: <200ms
- **Citation Accuracy**: 100% (all responses include sources)

## 🔐 Compliance & Security

- **Data Privacy**: Local processing, no external data sharing
- **Source Attribution**: All responses include proper citations
- **Professional Language**: Banking-appropriate terminology
- **Regulatory Focus**: Emphasizes compliance requirements

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test with sample queries
5. Submit a pull request

## 📄 License

This project is for educational and professional use. Please ensure compliance with RBI document usage policies.

## 🆘 Troubleshooting

### Common Issues

1. **ChromaDB Connection Error**:
   ```bash
   # Clear ChromaDB cache
   rm -rf chroma_db/
   # Re-run vector store setup
   ```

2. **Out of Memory**:
   ```python
   # Reduce batch size in embedding generation
   batch_size = 16  # Instead of 32
   ```

3. **LLM Not Working**:
   ```python
   # Check API key or use free Ollama option
   os.environ['OPENAI_API_KEY'] = 'your-key'
   ```

### Getting Help

- Check the notebook cells for detailed implementation
- Review error messages for specific issues
- Ensure all dependencies are installed correctly

## 🎯 Future Enhancements

- [ ] Streamlit web interface
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] PDF document support
- [ ] Real-time document updates
- [ ] Integration with banking systems
- [ ] Mobile-responsive design

---

**Built with**: Python, LangChain, ChromaDB, Sentence Transformers, and modern NLP techniques.

**For Banking Professionals**: Streamline your RBI compliance research with AI-powered document search and analysis.
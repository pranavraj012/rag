# SOP Knowledge Assistant

A powerful AI-powered document Q&A system for Standard Operating Procedures (SOPs) built with Streamlit, LangChain, and ChromaDB.

## 🚀 Features

- **Document Processing**: Supports PDF, DOCX, and TXT files
- **GPU Acceleration**: Optimized for NVIDIA GPUs (GTX 1650, RTX 4060, etc.)
- **Vector Search**: Semantic search using ChromaDB
- **AI Q&A**: Natural language question answering using DialoGPT
- **Web Interface**: User-friendly Streamlit interface

## 📋 Requirements

- Python 3.8+
- NVIDIA GPU with CUDA support (recommended)
- 2GB+ GPU VRAM (4GB+ recommended)

## 🛠️ Installation

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd sop_project
```

2. **Create virtual environment:**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Install PyTorch with CUDA support:**
```bash
# For CUDA 11.8 (GTX 1650, RTX 30/40 series)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.1 (Latest RTX 40 series)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

## 🚀 Usage

1. **Start the application:**
```bash
streamlit run app.py
```

2. **Open your browser:** http://localhost:8501

3. **Upload documents** using the sidebar

4. **Ask questions** about your SOPs!

## 💾 Models

### Recommended Language Models (1B+ params)

The system now supports high-quality 1B+ parameter models for better answers:

#### **Phi-2 (Recommended)** ⭐
- **Size:** 2.7B parameters (~2.5GB VRAM)
- **Quality:** ⭐⭐⭐⭐⭐ Excellent
- **Best for:** Production-quality answers, detailed explanations
- **Works on:** GTX 1650 4GB and up

#### **TinyLlama-1.1B-Chat** 💨
- **Size:** 1.1B parameters (~1.2GB VRAM)
- **Quality:** ⭐⭐⭐⭐ Very Good  
- **Best for:** Fast responses, low memory usage
- **Works on:** Any GPU with 2GB+ VRAM

#### **StableLM-2-1.6B** ⚖️
- **Size:** 1.6B parameters (~1.8GB VRAM)
- **Quality:** ⭐⭐⭐⭐ Excellent
- **Best for:** Balanced performance
- **Works on:** GTX 1650 4GB and up

#### **DialoGPT-medium** 🪶
- **Size:** 350M parameters (~400MB VRAM)
- **Quality:** ⭐⭐⭐ Good
- **Best for:** Low memory systems, CPU fallback
- **Works on:** Any system

### Changing Models

Edit `.env` file and set your preferred model:
```bash
# Best quality (recommended)
LLM_MODEL=microsoft/phi-2

# Fastest
LLM_MODEL=TinyLlama/TinyLlama-1.1B-Chat-v1.0

# Lightweight
LLM_MODEL=microsoft/DialoGPT-medium
```

See [MODEL_GUIDE.md](MODEL_GUIDE.md) for detailed comparison and recommendations.

### Download Information

Models are automatically downloaded on first run:
- **Phi-2:** ~5.2GB download
- **TinyLlama:** ~2.2GB download
- **StableLM-2:** ~3.2GB download
- **DialoGPT:** ~400MB download
- **Embeddings (all-MiniLM-L6-v2):** ~80MB

Models are cached in: `~/.cache/huggingface/`

## 🖥️ GPU Support

### Tested Configurations:
- **GTX 1650 (4GB)**: ✅ Works perfectly
- **RTX 4060 (8GB)**: ✅ Excellent performance
- **RTX 3070/4070+**: ✅ Optimal performance

### Performance:
- **Model Loading**: ~5 seconds on GPU vs ~20+ seconds on CPU
- **Query Processing**: ~2-3 seconds on GPU vs ~10+ seconds on CPU
- **VRAM Usage**: ~2-3GB (leaves room for other applications)

## 📁 Project Structure

```
├── app.py                 # Main Streamlit application
├── document_processor.py  # Document text extraction and chunking
├── vector_store.py        # ChromaDB vector database
├── query_engine.py        # AI query processing
├── requirements.txt      # Python dependencies
├── .env                  # Configuration file (GTX 1650 optimized)
├── .env.rtx4060          # Configuration for RTX 4060 users
├── documents/           # Place your SOP documents here
├── chroma_db/          # Vector database storage (auto-created)
└── tests/              # Test files and utilities
```

## ⚙️ Configuration

Edit `.env` file to customize:
```bash
DOCUMENTS_FOLDER=./documents
CHROMA_PATH=./chroma_db
COLLECTION_NAME=sop-knowledge
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

## 🧪 Testing

Run the comprehensive test to verify everything works:
```bash
python tests/test_advanced.py
```

Or run a basic functionality test:
```bash
python tests/final_test.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - Feel free to use for personal and commercial projects!

## 🆘 Troubleshooting

### CUDA Issues:
```bash
# Check CUDA availability
python -c "import torch; print('CUDA:', torch.cuda.is_available())"
```

### Memory Issues:
- Reduce `CHUNK_SIZE` in .env
- Close other GPU applications
- Use CPU fallback if needed

### Model Download Issues:
- Check internet connection
- Manually clear cache: `rm -rf ~/.cache/huggingface/`
#!/usr/bin/env python3
"""
Quick GPU performance test
"""
import torch
import time
from query_engine import QueryEngine
from document_processor import DocumentProcessor

def quick_test():
    print("🚀 GPU Performance Test")
    print(f"CUDA Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    
    print("\n🔧 Testing Query Engine initialization...")
    start_time = time.time()
    
    # This will now use GPU automatically
    query_engine = QueryEngine()
    
    init_time = time.time() - start_time
    print(f"⏱️ Model loading time: {init_time:.2f} seconds")
    print(f"✅ Model loaded on: {'GPU' if torch.cuda.is_available() else 'CPU'}")
    
    # Test a simple document processing
    print("\n📄 Testing document processing...")
    processor = DocumentProcessor(chunk_size=500, chunk_overlap=100)
    docs = processor.process_folder("./documents")
    print(f"✅ Processed {len(docs)} document chunks")
    
    return query_engine, docs

if __name__ == "__main__":
    quick_test()
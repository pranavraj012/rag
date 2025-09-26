#!/usr/bin/env python3
"""
Quick manual test for the SOP Knowledge Assistant
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from query_engine import QueryEngine
from vector_store import VectorStore
import torch

def quick_test():
    print("🚀 Quick SOP Knowledge Assistant Test")
    print("=" * 50)
    
    # Initialize components
    print("\n🔧 Initializing system...")
    vector_store = VectorStore()
    query_engine = QueryEngine()
    
    # Add documents using the processor
    from document_processor import DocumentProcessor
    processor = DocumentProcessor()
    
    test_files = [
        "documents/quality_control.txt",
        "documents/safety_procedures.txt", 
        "documents/sops for repair of vessels.pdf"
    ]
    
    all_docs = []
    for file_path in test_files:
        if os.path.exists(file_path):
            print(f"📄 Processing: {file_path}")
            docs = processor.process_document(file_path)
            all_docs.extend(docs)
    
    vector_store.add_documents(all_docs)
    print(f"✅ Added {len(all_docs)} document chunks")
    
    # Test query
    test_query = "What safety equipment is required for equipment maintenance?"
    print(f"\n❓ Test Query: {test_query}")
    print("-" * 50)
    
    # Get relevant documents
    relevant_docs = vector_store.search(test_query, k=3)
    context = "\n".join([doc.page_content for doc in relevant_docs])
    
    # Generate response
    response = query_engine.generate_answer(test_query, context)
    
    print(f"💬 Response:")
    print(response)
    print("\n✅ Test completed successfully!")

if __name__ == "__main__":
    quick_test()
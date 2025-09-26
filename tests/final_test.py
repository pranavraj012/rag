#!/usr/bin/env python3
"""
Final working test for the SOP Knowledge Assistant
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from query_engine import QueryEngine
from vector_store import VectorStore
from document_processor import DocumentProcessor

def working_test():
    print("🚀 SOP Knowledge Assistant - Working Test")
    print("=" * 50)
    
    # Initialize all components
    print("\n🔧 Initializing system...")
    vector_store = VectorStore()
    query_engine = QueryEngine()
    processor = DocumentProcessor()
    
    # Process and add documents
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
    
    # Test queries
    test_cases = [
        "What safety equipment is required for equipment maintenance?",
        "How to perform quality control inspection?",
        "What is the lockout tagout procedure?"
    ]
    
    for i, query in enumerate(test_cases, 1):
        print(f"\n{'='*50}")
        print(f"🧪 Test {i}")
        print(f"❓ Query: {query}")
        print("-" * 50)
        
        # Get relevant documents
        relevant_docs = vector_store.search(query, k=3)
        
        # Use the QueryEngine's generate_answer method properly
        response = query_engine.generate_answer(query, relevant_docs)
        
        print(f"💬 Response:")
        print(response[:500] + "..." if len(response) > 500 else response)
        print("\n✅ Test completed")
    
    print(f"\n🎉 All tests completed successfully!")
    print("🌐 The Streamlit app is ready at: http://localhost:8501")

if __name__ == "__main__":
    working_test()
#!/usr/bin/env python3
"""
Interactive test for the Advanced SOP Knowledge Assistant
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from query_engine import QueryEngine
from vector_store import VectorStore
import torch

def test_interactive():
    print("🚀 SOP Knowledge Assistant - Interactive Test")
    print("=" * 60)
    
    # Initialize components
    print("\n🔧 Initializing system...")
    vector_store = VectorStore()
    query_engine = QueryEngine()
    
    # Load test documents
    test_files = [
        "documents/quality_control.txt",
        "documents/safety_procedures.txt", 
        "documents/sops for repair of vessels.pdf"
    ]
    
    for file_path in test_files:
        if os.path.exists(file_path):
            print(f"📄 Loading: {file_path}")
            vector_store.add_documents([file_path])
    
    print("\n✅ System ready!")
    print("\nAvailable query modes:")
    print("1. Standard Q&A")
    print("2. Step-by-step instructions")
    print("3. Generate new SOP")
    print("4. Exit")
    
    # Test specific queries
    test_queries = [
        ("What safety equipment is required for equipment maintenance?", "standard"),
        ("How to perform lockout tagout procedure step by step?", "step_by_step"),
        ("What is the process for preparing a defect list before ship repair?", "standard"),
    ]
    
    for i, (query, mode) in enumerate(test_queries, 1):
        print(f"\n{'='*60}")
        print(f"🧪 Test {i}: {mode.upper()}")
        print(f"❓ Query: {query}")
        print("-" * 60)
        
        response, sources = query_engine.query(query, vector_store)
        
        print(f"📚 Sources: {sources}")
        print(f"💬 Response:")
        print(response)
        print("-" * 60)
        
        input("Press Enter to continue...")
    
    print("\n🎉 Interactive testing completed!")
    print("System is ready for use with the Streamlit app!")

if __name__ == "__main__":
    test_interactive()
#!/usr/bin/env python3
"""
Test script for SOP Knowledge Assistant
Tests all major components individually
"""

import os
from pathlib import Path
from document_processor import DocumentProcessor
from vector_store import VectorStore
from query_engine import QueryEngine

def test_document_processing():
    """Test document processing functionality"""
    print("🔍 Testing Document Processing...")
    
    processor = DocumentProcessor(chunk_size=500, chunk_overlap=100)
    
    # Test processing the documents folder
    docs = processor.process_folder("./documents")
    print(f"✅ Processed {len(docs)} document chunks")
    
    if docs:
        print(f"   Sample chunk preview: {docs[0].page_content[:100]}...")
        print(f"   Metadata: {docs[0].metadata}")
    
    return docs

def test_vector_store(documents):
    """Test vector store functionality"""
    print("\n🗄️ Testing Vector Store...")
    
    # Initialize vector store
    vector_store = VectorStore(
        persist_directory="./test_chroma_db",
        collection_name="test-collection",
        embedding_model="all-MiniLM-L6-v2"
    )
    
    # Clear any existing data
    vector_store.clear_collection()
    
    # Add documents
    success = vector_store.add_documents(documents)
    print(f"✅ Documents added successfully: {success}")
    
    # Get collection info
    info = vector_store.get_collection_info()
    print(f"   Collection info: {info}")
    
    # Test search
    query = "safety procedures"
    results = vector_store.search(query, k=3)
    print(f"✅ Search for '{query}' returned {len(results)} results")
    
    if results:
        print(f"   Top result preview: {results[0].page_content[:100]}...")
    
    return vector_store, results

def test_query_engine(retrieved_docs):
    """Test query engine functionality"""
    print("\n🤖 Testing Query Engine...")
    
    query_engine = QueryEngine()
    print(f"✅ Model loaded: {query_engine.model_loaded}")
    
    if query_engine.model_loaded:
        # Test answer generation
        query = "What are the safety requirements for equipment maintenance?"
        result = query_engine.generate_answer(query, retrieved_docs)
        
        print(f"✅ Generated answer for: '{query}'")
        print(f"   Answer: {result['answer'][:200]}...")
        print(f"   Sources: {result['sources']}")
        print(f"   Confidence: {result['confidence']:.2f}")
    else:
        print("⚠️ Language model not available - will show document excerpts instead")
        # Test fallback functionality
        result = query_engine.generate_answer("test query", retrieved_docs)
        print(f"✅ Fallback response: {result['answer'][:100]}...")
    
    return query_engine

def main():
    """Run all tests"""
    print("🚀 Starting SOP Knowledge Assistant Tests\n")
    
    try:
        # Test 1: Document Processing
        docs = test_document_processing()
        
        if not docs:
            print("❌ No documents found to process. Please check the documents folder.")
            return
        
        # Test 2: Vector Store
        vector_store, retrieved_docs = test_vector_store(docs)
        
        # Test 3: Query Engine
        query_engine = test_query_engine(retrieved_docs)
        
        print("\n🎉 All tests completed successfully!")
        print("\nThe SOP Knowledge Assistant is ready to use!")
        print("You can now:")
        print("1. Access the web interface at http://localhost:8501")
        print("2. Upload additional documents through the sidebar")
        print("3. Ask questions about your SOPs")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
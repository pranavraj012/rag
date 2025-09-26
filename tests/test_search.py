#!/usr/bin/env python3
"""
Test vector search to see what documents are being retrieved
"""
from vector_store import VectorStore
from document_processor import DocumentProcessor

def test_vector_search():
    print("🔍 Testing Vector Search")
    
    # Initialize components
    processor = DocumentProcessor()
    vector_store = VectorStore()
    
    # Process and add documents
    print("\n📄 Processing documents...")
    docs = processor.process_folder('./documents')
    print(f"✅ Processed {len(docs)} chunks")
    
    # Show what documents we have
    for i, doc in enumerate(docs[:10]):
        print(f"Chunk {i}: {doc.metadata['file_name']} - {doc.page_content[:100]}...")
    
    # Clear and re-add documents
    print("\n🗄️ Adding to vector store...")
    vector_store.clear_collection()
    success = vector_store.add_documents(docs)
    print(f"✅ Added successfully: {success}")
    
    # Test different search queries
    test_queries = [
        "safety equipment PPE hard hat",
        "lockout tagout procedures",
        "personal protective equipment",
        "safety procedures",
        "quality control inspection"
    ]
    
    print("\n🔍 Testing searches:")
    for query in test_queries:
        print(f"\n❓ Query: '{query}'")
        results = vector_store.search(query, k=3)
        for i, doc in enumerate(results):
            print(f"  {i+1}. {doc.metadata['file_name']}: {doc.page_content[:100]}...")

if __name__ == "__main__":
    test_vector_search()
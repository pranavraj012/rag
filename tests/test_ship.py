#!/usr/bin/env python3
"""
Test with specific ship repair query using the right documents
"""
from query_engine import QueryEngine
from vector_store import VectorStore
from document_processor import DocumentProcessor

def test_ship_repair_query():
    print("🚢 Testing Ship Repair Query with Right Documents")
    
    # Initialize all components
    processor = DocumentProcessor()
    vector_store = VectorStore()
    qe = QueryEngine()
    
    # Process documents and add to vector store
    print("\n📄 Processing documents...")
    docs = processor.process_folder('./documents')
    
    # Clear and add documents to vector store
    vector_store.clear_collection()
    vector_store.add_documents(docs)
    
    # Search specifically for ship/vessel repair documents
    query = "What is the process for preparing a defect list before ship repair?"
    print(f"\n🔍 Searching for: '{query}'")
    
    # Get relevant documents from vector search
    relevant_docs = vector_store.search(query, k=5)
    
    print(f"\n📚 Found {len(relevant_docs)} relevant documents:")
    for i, doc in enumerate(relevant_docs):
        print(f"  {i+1}. {doc.metadata['file_name']}: {doc.page_content[:100]}...")
        
    # Generate answer with the retrieved documents
    print(f"\n🤖 Generating answer...")
    result = qe.generate_answer(query, relevant_docs)
    
    print(f"\n💬 Complete Answer:")
    print(f"{result['answer']}")
    print(f"\n📚 Sources: {result['sources']}")
    print(f"🎯 Confidence: {result['confidence']:.2f}")
    print(f"📏 Answer length: {len(result['answer'])} characters")
    
    # Check if answer mentions vessel/ship repair specifically
    ship_keywords = ['vessel', 'ship', 'defect list', 'repair', 'deck', 'crew']
    mentions_ships = any(keyword.lower() in result['answer'].lower() for keyword in ship_keywords)
    print(f"🚢 Answer mentions ship/vessel repair: {mentions_ships}")

if __name__ == "__main__":
    test_ship_repair_query()
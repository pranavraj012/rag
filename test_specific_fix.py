#!/usr/bin/env python3
"""Fix and test the defect list query specifically"""

from vector_store import VectorStore
from query_engine import QueryEngine

def test_specific_query():
    print("🔧 Testing specific defect list query with detailed debugging")
    print("=" * 70)
    
    # Initialize
    vector_store = VectorStore()
    query_engine = QueryEngine()
    
    query = "How is a defect list prepared for annual repair?"
    
    print(f"Query: {query}")
    print("-" * 70)
    
    # Get the documents
    docs = vector_store.search(query, k=3)
    
    print(f"Found {len(docs)} documents")
    for i, doc in enumerate(docs):
        print(f"\nDocument {i+1}:")
        print(f"Source: {doc.metadata.get('source', 'Unknown')}")
        print(f"Content: '{doc.page_content}'")
        print("-" * 50)
    
    # Test the _extract_key_information method directly with complete content
    complete_context = ""
    for doc in docs:
        complete_context += doc.page_content + " "
    
    print(f"\nComplete context length: {len(complete_context)} chars")
    print(f"Complete context: '{complete_context}'")
    print("-" * 70)
    
    # Test extraction
    extracted = query_engine._extract_key_information(complete_context, query)
    
    print(f"\nExtracted result:")
    print(f"Length: {len(extracted)} chars")
    print(f"Content: '{extracted}'")
    
    # Test the full generate_answer method
    result = query_engine.generate_answer(query, docs)
    
    print(f"\nFull result:")
    print(f"Answer: {result['answer']}")
    print(f"Confidence: {result['confidence']:.2%}")

if __name__ == "__main__":
    test_specific_query()
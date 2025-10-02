#!/usr/bin/env python3
"""Test the improved response generation for the defect list query"""

import sys
from vector_store import VectorStore
from query_engine import QueryEngine

def test_defect_list_query():
    print("Testing improved response generation...")
    print("=" * 60)
    
    # Initialize components
    vector_store = VectorStore()
    query_engine = QueryEngine()
    
    # The problematic query
    query = "How is a defect list prepared for annual repair?"
    
    print(f"Query: {query}")
    print("-" * 60)
    
    # Search for relevant documents
    print("🔍 Searching for relevant documents...")
    docs = vector_store.search(query, k=3)
    
    if docs:
        print(f"✅ Found {len(docs)} relevant documents")
        for i, doc in enumerate(docs):
            print(f"\nDocument {i+1} content preview:")
            print(f"Source: {doc.metadata.get('source', 'Unknown')}")
            print(f"Content (first 200 chars): {doc.page_content[:200]}...")
            print(f"Full content length: {len(doc.page_content)} characters")
    
    # Generate answer with improved system
    print("\n🤖 Generating answer with improved system...")
    print("-" * 60)
    
    result = query_engine.generate_answer(query, docs)
    
    print(f"Generated Answer:")
    print(f"Confidence: {result['confidence']:.2%}")
    print(f"Intent: {result.get('intent', 'Not available')}")
    print(f"Response Length: {len(result['answer'])} characters")
    print(f"Word Count: {len(result['answer'].split())} words")
    print("\nFull Answer:")
    print(result['answer'])
    
    # Test if the response is complete and non-repetitive
    print("\n📊 Response Analysis:")
    answer = result['answer']
    
    # Check for completeness
    has_deck_info = 'deck' in answer.lower()
    has_engine_info = 'engine' in answer.lower()
    has_master_info = 'master' in answer.lower()
    has_crew_info = 'crew' in answer.lower()
    
    print(f"✅ Contains deck information: {has_deck_info}")
    print(f"✅ Contains engine information: {has_engine_info}")
    print(f"✅ Contains master information: {has_master_info}")
    print(f"✅ Contains crew information: {has_crew_info}")
    
    # Check for repetition
    sentences = answer.split('.')
    unique_sentences = set(s.strip().lower() for s in sentences if len(s.strip()) > 10)
    repetition_ratio = len(sentences) / len(unique_sentences) if unique_sentences else 1
    
    print(f"📈 Repetition ratio: {repetition_ratio:.2f} (lower is better)")
    print(f"📝 Total sentences: {len(sentences)}")
    print(f"🔄 Unique sentences: {len(unique_sentences)}")
    
    # Overall quality assessment
    is_complete = has_deck_info and has_engine_info and has_master_info
    is_not_repetitive = repetition_ratio < 1.5
    is_adequate_length = 50 <= len(answer.split()) <= 300
    
    print(f"\n🎯 Quality Assessment:")
    print(f"✅ Complete information: {is_complete}")
    print(f"✅ Non-repetitive: {is_not_repetitive}")
    print(f"✅ Adequate length: {is_adequate_length}")
    
    overall_quality = is_complete and is_not_repetitive and is_adequate_length
    print(f"🏆 Overall Quality: {'GOOD' if overall_quality else 'NEEDS IMPROVEMENT'}")

if __name__ == "__main__":
    test_defect_list_query()
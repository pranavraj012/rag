#!/usr/bin/env python3
"""
Test the improved answer generation with longer, complete answers
"""
from query_engine import QueryEngine
from document_processor import DocumentProcessor

def test_complete_answers():
    print("🧪 Testing Complete Answer Generation")
    
    # Initialize components
    qe = QueryEngine()
    processor = DocumentProcessor()
    docs = processor.process_folder('./documents')
    
    print(f"✅ Loaded {len(docs)} document chunks")
    
    # Test the specific query that was getting truncated
    test_query = "What is the process for preparing a defect list before ship repair?"
    print(f"\n❓ Query: {test_query}")
    
    result = qe.generate_answer(test_query, docs[:5])  # Use more context docs
    
    print(f"\n💬 Complete Answer:")
    print(f"{result['answer']}")
    print(f"\n📚 Sources: {result['sources']}")
    print(f"🎯 Confidence: {result['confidence']:.2f}")
    print(f"📏 Answer length: {len(result['answer'])} characters")
    print(f"📝 Word count: {len(result['answer'].split())} words")
    
    # Check if answer is complete (should end with proper punctuation)
    is_complete = result['answer'].endswith(('.', '!', '?', ':'))
    print(f"✅ Answer appears complete: {is_complete}")

if __name__ == "__main__":
    test_complete_answers()
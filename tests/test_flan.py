#!/usr/bin/env python3
"""
Quick test of the new Flan-T5 model
"""
from query_engine import QueryEngine
from document_processor import DocumentProcessor

def test_new_model():
    print("🚀 Testing New Flan-T5 Model")
    
    # Initialize query engine
    qe = QueryEngine()
    
    if not qe.model_loaded:
        print("❌ Model failed to load!")
        return
    
    # Process documents
    print("\n📄 Processing documents...")
    processor = DocumentProcessor()
    docs = processor.process_folder('./documents')
    print(f"✅ Processed {len(docs)} document chunks")
    
    if not docs:
        print("❌ No documents found!")
        return
    
    # Test Q&A
    print("\n🤔 Testing Q&A...")
    test_questions = [
        "What safety equipment is required?",
        "How often should materials be inspected?",
        "What are the lockout procedures?"
    ]
    
    for question in test_questions:
        print(f"\n❓ Question: {question}")
        result = qe.generate_answer(question, docs[:3])
        print(f"💬 Answer: {result['answer']}")
        print(f"📚 Sources: {result['sources']}")
        print(f"🎯 Confidence: {result['confidence']:.2f}")
        print("-" * 50)

if __name__ == "__main__":
    test_new_model()
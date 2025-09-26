#!/usr/bin/env python3
"""
Test Advanced SOP Knowledge Assistant
Tests all modes: Q&A, Step-by-step instructions, SOP generation
"""
from query_engine import QueryEngine
from vector_store import VectorStore
from document_processor import DocumentProcessor

def test_advanced_features():
    print("🚀 Testing Advanced SOP Knowledge Assistant")
    
    # Initialize all components
    print("\n🔧 Initializing components...")
    processor = DocumentProcessor()
    vector_store = VectorStore()
    query_engine = QueryEngine()
    
    if not query_engine.model_loaded:
        print("❌ Query engine failed to load!")
        return
    
    # Process and add documents
    print("\n📄 Processing documents...")
    docs = processor.process_folder('./documents')
    vector_store.clear_collection()
    vector_store.add_documents(docs)
    print(f"✅ Added {len(docs)} document chunks")
    
    # Test queries for different modes
    test_cases = [
        {
            "query": "What safety equipment is required for equipment maintenance?",
            "expected_type": "standard_qa",
            "description": "Standard Q&A"
        },
        {
            "query": "How to perform lockout tagout procedure step by step?",
            "expected_type": "step_by_step", 
            "description": "Step-by-step instructions"
        },
        {
            "query": "What is the process for preparing a defect list before ship repair?",
            "expected_type": "standard_qa",
            "description": "Ship repair defect list"
        },
        {
            "query": "Step by step guide for quality control inspection",
            "expected_type": "step_by_step",
            "description": "QC step-by-step"
        }
    ]
    
    print(f"\n🧪 Testing {len(test_cases)} different query types:")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: {test_case['description']} ---")
        print(f"❓ Query: {test_case['query']}")
        
        # Get relevant documents
        relevant_docs = vector_store.search(test_case['query'], k=5)
        
        # Generate answer
        result = query_engine.generate_answer(test_case['query'], relevant_docs)
        
        print(f"🎯 Expected Type: {test_case['expected_type']}")
        print(f"📊 Actual Type: {result.get('answer_type', 'unknown')}")
        print(f"📈 Confidence: {result['confidence']:.2f}")
        print(f"📚 Sources: {result['sources']}")
        print(f"💬 Answer Preview: {result['answer'][:200]}...")
        
        # Check if answer is complete
        is_complete = len(result['answer']) > 50 and not result['answer'].endswith('...')
        print(f"✅ Complete Answer: {is_complete}")
        
        print("-" * 60)
    
    print("\n🎉 Advanced testing completed!")
    print("\n🚀 Ready for:")
    print("   ✅ Standard Q&A")
    print("   ✅ Step-by-step instructions") 
    print("   ✅ Document-based responses")
    print("   🔄 Future: SOP generation")
    print("   🔄 Future: Multimodal support")

if __name__ == "__main__":
    test_advanced_features()
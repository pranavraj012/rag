#!/usr/bin/env python3
"""
Compare different language models for answer quality
"""
import time
import torch
from query_engine import QueryEngine
from vector_store import VectorStore

def test_model(model_name: str, query: str, docs):
    """Test a specific model with a query"""
    print(f"\n{'='*70}")
    print(f"🤖 Testing Model: {model_name}")
    print(f"{'='*70}")
    
    try:
        # Record start time
        start_time = time.time()
        
        # Initialize query engine with specific model
        qe = QueryEngine(model_name=model_name)
        
        if not qe.model_loaded:
            print(f"❌ Failed to load {model_name}")
            return None
        
        load_time = time.time() - start_time
        print(f"⏱️ Model loading time: {load_time:.2f} seconds")
        
        # Check VRAM usage
        if torch.cuda.is_available():
            vram_used = torch.cuda.memory_allocated(0) / 1024**3
            vram_total = torch.cuda.get_device_properties(0).total_memory / 1024**3
            print(f"💾 VRAM Usage: {vram_used:.2f}GB / {vram_total:.1f}GB")
        
        # Generate answer
        print(f"\n❓ Query: {query}")
        print("-" * 70)
        
        gen_start = time.time()
        result = qe.generate_answer(query, docs)
        gen_time = time.time() - gen_start
        
        print(f"⏱️ Generation time: {gen_time:.2f} seconds")
        print(f"📏 Answer length: {len(result['answer'])} chars, {len(result['answer'].split())} words")
        print(f"🎯 Confidence: {result['confidence']:.2%}")
        print(f"\n💬 Answer Preview (first 300 chars):")
        print(result['answer'][:300] + "..." if len(result['answer']) > 300 else result['answer'])
        
        return {
            'model': model_name,
            'load_time': load_time,
            'gen_time': gen_time,
            'answer_length': len(result['answer']),
            'word_count': len(result['answer'].split()),
            'confidence': result['confidence'],
            'answer': result['answer']
        }
        
    except Exception as e:
        print(f"❌ Error testing {model_name}: {e}")
        return None
    finally:
        # Clean up memory
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

def main():
    print("🚀 Language Model Comparison Test")
    print("=" * 70)
    
    # Initialize vector store and get test documents
    print("\n🔧 Initializing vector store...")
    vector_store = VectorStore()
    
    # Test query
    test_query = "How is a defect list prepared for annual repair?"
    
    print(f"🔍 Retrieving documents for test query...")
    docs = vector_store.search(test_query, k=3)
    
    if not docs:
        print("❌ No documents found! Please ensure documents are loaded.")
        print("   Run: python app.py and upload documents first")
        return
    
    print(f"✅ Retrieved {len(docs)} relevant documents")
    
    # Models to test (in order of quality)
    models_to_test = [
        "microsoft/phi-2",  # Best quality
        "TinyLlama/TinyLlama-1.1B-Chat-v1.0",  # Fastest
        "stabilityai/stablelm-2-1_6b",  # Balanced
        "microsoft/DialoGPT-medium"  # Lightweight baseline
    ]
    
    results = []
    
    print(f"\n🧪 Testing {len(models_to_test)} models...")
    print(f"⚠️  Note: First model may take longer due to initial CUDA setup")
    
    for model_name in models_to_test:
        result = test_model(model_name, test_query, docs)
        if result:
            results.append(result)
        
        # Small delay between tests
        time.sleep(2)
    
    # Summary comparison
    if results:
        print(f"\n{'='*70}")
        print("📊 COMPARISON SUMMARY")
        print(f"{'='*70}")
        
        print(f"\n{'Model':<45} {'Load(s)':<10} {'Gen(s)':<10} {'Words':<10} {'Quality'}")
        print("-" * 70)
        
        for r in results:
            model_short = r['model'].split('/')[-1][:40]
            quality_stars = "⭐" * min(5, int(r['confidence'] * 10))
            print(f"{model_short:<45} {r['load_time']:<10.1f} {r['gen_time']:<10.1f} {r['word_count']:<10} {quality_stars}")
        
        # Recommendations
        print(f"\n🎯 RECOMMENDATIONS:")
        
        # Find best by quality (word count as proxy)
        best_quality = max(results, key=lambda x: x['word_count'])
        print(f"   Best Quality: {best_quality['model']} ({best_quality['word_count']} words)")
        
        # Find fastest generation
        fastest = min(results, key=lambda x: x['gen_time'])
        print(f"   Fastest: {fastest['model']} ({fastest['gen_time']:.1f}s)")
        
        # Find best balance (quality/speed ratio)
        for r in results:
            r['efficiency'] = r['word_count'] / r['gen_time']
        best_balance = max(results, key=lambda x: x['efficiency'])
        print(f"   Best Balance: {best_balance['model']} ({best_balance['efficiency']:.1f} words/sec)")
        
        print(f"\n💡 For GTX 1650 4GB: Recommended is **{best_quality['model']}**")
        print(f"   It provides the best answer quality with acceptable performance.")
    
    print(f"\n✅ Comparison complete! See MODEL_GUIDE.md for more details.")

if __name__ == "__main__":
    main()

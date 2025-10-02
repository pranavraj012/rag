#!/usr/bin/env python3
"""Quick test to verify Phi-2 is working properly"""

from query_engine import QueryEngine
from vector_store import VectorStore

print("🧪 Testing Phi-2 Response Generation")
print("=" * 60)

# Initialize
vector_store = VectorStore()
query_engine = QueryEngine()

if not query_engine.model_loaded:
    print("❌ Model not loaded!")
    exit(1)

# Test query
query = "What safety equipment is required?"
print(f"\n❓ Query: {query}")
print("-" * 60)

# Get documents
docs = vector_store.search(query, k=3)
print(f"📚 Retrieved {len(docs)} documents")

# Generate answer
result = query_engine.generate_answer(query, docs)

print(f"\n💬 Answer:")
print(result['answer'])
print(f"\n📊 Stats:")
print(f"   Length: {len(result['answer'])} chars")
print(f"   Words: {len(result['answer'].split())} words")
print(f"   Confidence: {result['confidence']:.2%}")
print(f"\n✅ Test complete!")

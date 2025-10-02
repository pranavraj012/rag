from vector_store import VectorStore

# Initialize vector store
vs = VectorStore()

# Test query about spares
query = "how should new spares be recorded after repairs"
results = vs.search_with_scores(query, k=5)

print(f"Query: {query}")
print(f"Found {len(results)} results\n")
print("="*100)

for i, (doc, score) in enumerate(results):
    print(f"\nDocument {i+1}:")
    print(f"Similarity Score: {score:.4f}")
    print(f"Source: {doc.metadata.get('file_name', 'Unknown')}")
    print(f"Content Length: {len(doc.page_content)} chars")
    print(f"\nContent Preview (first 300 chars):")
    print(doc.page_content[:300])
    print("="*100)

# Check for duplicates
print("\n\n🔍 DUPLICATE CHECK:")
contents = [doc.page_content for doc, score in results]
unique_contents = set(contents)
print(f"Total documents retrieved: {len(contents)}")
print(f"Unique documents: {len(unique_contents)}")
print(f"Duplicates found: {len(contents) - len(unique_contents)}")

if len(contents) != len(unique_contents):
    print("\n⚠️ WARNING: Duplicate documents detected!")
    from collections import Counter
    content_counts = Counter(contents)
    for content, count in content_counts.items():
        if count > 1:
            print(f"\n  This content appears {count} times:")
            print(f"  {content[:150]}...")

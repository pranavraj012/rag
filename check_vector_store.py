from vector_store import VectorStore
import chromadb
from collections import Counter

# Initialize
vs = VectorStore()
client = chromadb.PersistentClient(path='./chroma_db')
coll = client.get_collection('sop-knowledge')

# Get all documents
results = coll.get()

print(f"Total embeddings in vector store: {len(results['ids'])}")
print(f"\nDocuments by source file:")
sources = [m.get('file_name', 'Unknown') for m in results['metadatas']]
for source, count in Counter(sources).most_common():
    print(f"  {source}: {count} chunks")

# Check for exact duplicate content
print(f"\n\n🔍 Checking for duplicate content...")
documents = results['documents']
unique_docs = set(documents)
print(f"Total document chunks: {len(documents)}")
print(f"Unique document chunks: {len(unique_docs)}")
print(f"Duplicate chunks: {len(documents) - len(unique_docs)}")

if len(documents) != len(unique_docs):
    print("\n⚠️ WARNING: Duplicate chunks found in vector store!")
    content_counts = Counter(documents)
    duplicates = [(content, count) for content, count in content_counts.items() if count > 1]
    print(f"\nNumber of content pieces that are duplicated: {len(duplicates)}")
    
    print("\nTop 5 most duplicated chunks:")
    for i, (content, count) in enumerate(sorted(duplicates, key=lambda x: x[1], reverse=True)[:5], 1):
        print(f"\n{i}. Appears {count} times:")
        print(f"   {content[:150]}...")

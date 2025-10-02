"""
Rebuild Vector Store - Remove all duplicates and reprocess documents cleanly
"""
from vector_store import VectorStore
from document_processor import DocumentProcessor
from collections import Counter
import os

print("="*80)
print("VECTOR STORE REBUILD - DUPLICATE REMOVAL")
print("="*80)

# Step 1: Check current state
print("\n📊 STEP 1: Checking current vector store state...")
vs = VectorStore()
import chromadb
client = chromadb.PersistentClient(path='./chroma_db')
coll = client.get_collection('sop-knowledge')
results = coll.get()

print(f"Current embeddings: {len(results['ids'])}")
documents = results['documents']
unique_docs = set(documents)
print(f"Unique chunks: {len(unique_docs)}")
print(f"Duplicate chunks: {len(documents) - len(unique_docs)}")

# Step 2: Clear the vector store
print("\n🗑️  STEP 2: Clearing vector store...")
vs.clear_collection()
print("✅ Vector store cleared")

# Step 3: Reprocess documents with deduplication
print("\n📄 STEP 3: Reprocessing documents...")
doc_processor = DocumentProcessor(chunk_size=1000, chunk_overlap=200)

documents_folder = "./documents"
if not os.path.exists(documents_folder):
    print(f"❌ Documents folder not found: {documents_folder}")
    exit(1)

# Process all documents
all_docs = doc_processor.process_folder(documents_folder)
print(f"\nProcessed {len(all_docs)} chunks from documents")

# Step 4: Deduplicate chunks before adding
print("\n🔍 STEP 4: Removing duplicates...")
seen_content = set()
unique_docs = []

for doc in all_docs:
    content_hash = doc.page_content.strip()
    if content_hash not in seen_content:
        seen_content.add(content_hash)
        unique_docs.append(doc)

print(f"Original chunks: {len(all_docs)}")
print(f"After deduplication: {len(unique_docs)}")
print(f"Removed duplicates: {len(all_docs) - len(unique_docs)}")

# Step 5: Add deduplicated documents to vector store
print("\n💾 STEP 5: Adding deduplicated documents to vector store...")
vs.add_documents(unique_docs)
print("✅ Documents added successfully")

# Step 6: Verify the rebuild
print("\n✔️  STEP 6: Verifying rebuild...")
info = vs.get_collection_info()
print(f"Final document count: {info['document_count']}")

# Check sources
print("\n📚 Documents by source:")
sources = [doc.metadata.get('file_name', 'Unknown') for doc in unique_docs]
for source, count in Counter(sources).most_common():
    print(f"  {source}: {count} chunks")

print("\n" + "="*80)
print("✅ REBUILD COMPLETE!")
print("="*80)
print("\nNext steps:")
print("1. Restart Streamlit: streamlit run app.py")
print("2. Test your queries - you should see:")
print("   - No duplicate results")
print("   - Higher confidence scores")
print("   - Better quality answers")

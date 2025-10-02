#!/usr/bin/env python3
"""Deep inspect the vector store content"""

from vector_store import VectorStore
import chromadb

def inspect_vector_store():
    print("🔍 Deep inspection of vector store content")
    print("=" * 60)
    
    # Initialize vector store
    vector_store = VectorStore()
    
    # Access the ChromaDB collection directly
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection("sop-knowledge")
    
    # Get all documents
    all_docs = collection.get()
    
    print(f"📚 Total documents in collection: {len(all_docs['ids'])}")
    
    # Search for defect-related documents
    defect_query = "defect list annual repair vessel crew master"
    
    print(f"\n🔍 Searching for: '{defect_query}'")
    print("-" * 60)
    
    # Get search results
    docs = vector_store.search(defect_query, k=5)
    
    for i, doc in enumerate(docs):
        print(f"\n📄 Document {i+1}:")
        print(f"Source: {doc.metadata.get('source', 'Unknown')}")
        print(f"Page: {doc.metadata.get('page', 'Unknown')}")
        print(f"Content length: {len(doc.page_content)} chars")
        print(f"Full content:")
        print("'" + doc.page_content + "'")
        print("-" * 60)
    
    # Also look for all documents containing "defect"
    print("\n🔍 All documents containing 'defect':")
    print("-" * 40)
    
    for i, doc_id in enumerate(all_docs['ids']):
        doc_text = all_docs['documents'][i]
        if 'defect' in doc_text.lower():
            print(f"\nDoc ID: {doc_id}")
            print(f"Metadata: {all_docs['metadatas'][i]}")
            print(f"Content: {doc_text}")
            print("-" * 40)

if __name__ == "__main__":
    inspect_vector_store()
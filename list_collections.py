#!/usr/bin/env python3
"""List ChromaDB collections"""

import chromadb

def list_collections():
    print("🔍 Listing ChromaDB collections")
    print("=" * 40)
    
    # Access the ChromaDB
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # List all collections
    collections = client.list_collections()
    
    print(f"📚 Found {len(collections)} collections:")
    for i, collection in enumerate(collections):
        print(f"{i+1}. Name: {collection.name}")
        print(f"   ID: {collection.id}")
        
        # Get some info about the collection
        try:
            count = collection.count()
            print(f"   Documents: {count}")
            
            # Get a sample document if any exist
            if count > 0:
                sample = collection.peek(limit=1)
                if sample['documents']:
                    print(f"   Sample text: {sample['documents'][0][:100]}...")
        except Exception as e:
            print(f"   Error getting info: {e}")
        
        print("-" * 40)

if __name__ == "__main__":
    list_collections()
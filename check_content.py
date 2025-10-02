#!/usr/bin/env python3
"""
Check what document content is being retrieved for defect list query
"""

from vector_store import VectorStore

def check_defect_list_content():
    print("🔍 Checking document content for 'defect list annual repair' query")
    print("=" * 60)
    
    vs = VectorStore()
    docs = vs.search('defect list annual repair', k=3)
    
    for i, doc in enumerate(docs, 1):
        print(f"\nDoc {i}:")
        print(f"Source: {doc.metadata.get('file_name', 'Unknown')}")
        print(f"Content preview:")
        print(doc.page_content[:800])
        print("-" * 60)

if __name__ == "__main__":
    check_defect_list_content()
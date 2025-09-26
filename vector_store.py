# vector_store.py
import os
from typing import List, Optional
import chromadb
from chromadb.config import Settings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

class VectorStore:
    def __init__(self, persist_directory: str = "./chroma_db", 
                 collection_name: str = "sop-knowledge",
                 embedding_model: str = "all-MiniLM-L6-v2"):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        # Initialize embeddings with GPU support
        import torch
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"🔧 Initializing embeddings on: {device.upper()}")
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model,
            model_kwargs={'device': device},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Initialize Chroma
        self.vectorstore = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory=persist_directory
        )
    
    def add_documents(self, documents: List[Document]) -> bool:
        """Add documents to vector store"""
        try:
            if documents:
                self.vectorstore.add_documents(documents)
                self.vectorstore.persist()
                print(f"Added {len(documents)} document chunks to vector store")
                return True
            return False
        except Exception as e:
            print(f"Error adding documents to vector store: {e}")
            return False
    
    def search(self, query: str, k: int = 5) -> List[Document]:
        """Search for relevant documents"""
        try:
            results = self.vectorstore.similarity_search(query, k=k)
            return results
        except Exception as e:
            print(f"Error searching vector store: {e}")
            return []
    
    def search_with_scores(self, query: str, k: int = 5) -> List[tuple]:
        """Search with similarity scores"""
        try:
            results = self.vectorstore.similarity_search_with_score(query, k=k)
            return results
        except Exception as e:
            print(f"Error searching vector store with scores: {e}")
            return []
    
    def get_collection_info(self) -> dict:
        """Get information about the collection"""
        try:
            collection = self.vectorstore._collection
            count = collection.count()
            return {
                "document_count": count,
                "collection_name": self.collection_name
            }
        except:
            return {"document_count": 0, "collection_name": self.collection_name}
    
    def clear_collection(self):
        """Clear all documents from collection"""
        try:
            self.vectorstore.delete_collection()
            self.vectorstore = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory
            )
            print("Collection cleared successfully")
        except Exception as e:
            print(f"Error clearing collection: {e}")

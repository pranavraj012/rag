# app.py
import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv
from document_processor import DocumentProcessor
from vector_store import VectorStore
from query_engine import QueryEngine
import tempfile

# Load environment variables
load_dotenv()

# Configuration
DOCUMENTS_FOLDER = os.getenv('DOCUMENTS_FOLDER', './documents')
CHROMA_PATH = os.getenv('CHROMA_PATH', './chroma_db')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'sop-knowledge')
CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', '1000'))
CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', '200'))
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')

# Initialize components
@st.cache_resource
def initialize_components():
    doc_processor = DocumentProcessor(CHUNK_SIZE, CHUNK_OVERLAP)
    vector_store = VectorStore(CHROMA_PATH, COLLECTION_NAME, EMBEDDING_MODEL)
    query_engine = QueryEngine()
    return doc_processor, vector_store, query_engine

def main():
    st.set_page_config(
        page_title="SOP Knowledge Assistant",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("🔧 SOP Knowledge Assistant")
    st.markdown("Upload your Standard Operating Procedure documents and ask questions!")
    
    # Initialize components
    doc_processor, vector_store, query_engine = initialize_components()
    
    # Sidebar for document management
    with st.sidebar:
        st.header("📁 Document Management")
        
        # Display current collection info
        info = vector_store.get_collection_info()
        st.metric("Documents in Database", info["document_count"])
        
        st.subheader("Upload Documents")
        uploaded_files = st.file_uploader(
            "Choose files",
            accept_multiple_files=True,
            type=['pdf', 'docx', 'txt'],
            help="Upload PDF, DOCX, or TXT files"
        )
        
        if uploaded_files:
            if st.button("Process Uploaded Files"):
                with st.spinner("Processing documents..."):
                    all_docs = []
                    for file in uploaded_files:
                        # Save uploaded file temporarily
                        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.name).suffix) as tmp_file:
                            tmp_file.write(file.getvalue())
                            tmp_path = tmp_file.name
                        
                        # Process document
                        docs = doc_processor.process_document(tmp_path)
                        all_docs.extend(docs)
                        
                        # Clean up temp file
                        os.unlink(tmp_path)
                    
                    if all_docs:
                        success = vector_store.add_documents(all_docs)
                        if success:
                            st.success(f"Successfully processed {len(all_docs)} document chunks!")
                            st.rerun()
                        else:
                            st.error("Error processing documents")
                    else:
                        st.warning("No content found in uploaded files")
        
        st.subheader("Load from Local Folder")
        folder_path = st.text_input("Folder Path", value=DOCUMENTS_FOLDER)
        
        if st.button("Load from Folder"):
            if os.path.exists(folder_path):
                with st.spinner("Processing folder..."):
                    docs = doc_processor.process_folder(folder_path)
                    if docs:
                        success = vector_store.add_documents(docs)
                        if success:
                            st.success(f"Successfully processed {len(docs)} document chunks!")
                            st.rerun()
                        else:
                            st.error("Error processing documents")
                    else:
                        st.warning("No supported documents found in folder")
            else:
                st.error("Folder does not exist")
        
        if st.button("Clear Database", type="secondary"):
            vector_store.clear_collection()
            st.success("Database cleared!")
            st.rerun()
    
    # Main query interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🤔 Ask Questions")
        
        # Query input
        query = st.text_area(
            "What would you like to know about your SOPs?",
            placeholder="e.g., What are the safety procedures for equipment maintenance?",
            height=100
        )
        
        # Search parameters
        with st.expander("Search Settings"):
            num_results = st.slider("Number of relevant documents to retrieve", 1, 10, 5)
        
        if st.button("Ask Question", type="primary"):
            if query.strip():
                with st.spinner("Searching and generating answer..."):
                    # Retrieve relevant documents
                    relevant_docs = vector_store.search(query, k=num_results)
                    
                    if relevant_docs:
                        # Generate answer
                        result = query_engine.generate_answer(query, relevant_docs)
                        
                        # Display answer
                        st.subheader("📋 Answer")
                        st.write(result["answer"])
                        
                        # Display confidence and sources
                        col_conf, col_sources = st.columns(2)
                        with col_conf:
                            confidence_pct = result.get("confidence", 0) * 100
                            st.metric("Confidence", f"{confidence_pct:.1f}%")
                        
                        with col_sources:
                            st.write("**Sources:**")
                            for source in result["sources"]:
                                st.write(f"• {source}")
                        
                        # Display relevant excerpts
                        with st.expander("View Relevant Document Excerpts"):
                            for i, doc in enumerate(relevant_docs):
                                st.write(f"**Excerpt {i+1}** (from {doc.metadata.get('file_name', 'Unknown')})")
                                st.write(doc.page_content)
                                st.write("---")
                    
                    else:
                        st.warning("No relevant documents found. Please upload some SOP documents first.")
            else:
                st.warning("Please enter a question.")
    
    with col2:
        st.header("📊 System Status")
        
        # System information
        info = vector_store.get_collection_info()
        st.metric("Total Documents", info["document_count"])
        st.metric("Collection Name", info["collection_name"])
        
        # Model status
        if query_engine.model_loaded:
            st.success("✅ Language Model Ready")
        else:
            st.warning("⚠️ Language Model Not Available")
        
        # Quick help
        with st.expander("💡 Tips"):
            st.markdown("""
            **How to use:**
            1. Upload your SOP documents using the sidebar
            2. Ask specific questions about procedures
            3. Review the generated answer and source documents
            
            **Best practices:**
            - Use clear, specific questions
            - Upload documents in PDF, DOCX, or TXT format
            - Review the confidence score and sources
            """)

if __name__ == "__main__":
    main()

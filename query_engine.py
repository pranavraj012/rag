# query_engine.py
import re
import torch
from typing import List, Dict, Any
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from langchain.schema import Document

class QueryEngine:
    def __init__(self, model_name: str = "google/flan-t5-small"):
        try:
            # Check if CUDA is available and set device
            device = 0 if torch.cuda.is_available() else -1
            device_name = "GPU (CUDA)" if device == 0 else "CPU"
            print(f"🚀 Loading model on: {device_name}")
            print(f"📦 Model: {model_name} (~80MB)")
            
            if torch.cuda.is_available():
                print(f"   GPU: {torch.cuda.get_device_name(0)}")
                print(f"   GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
            
            # Initialize the text2text-generation pipeline (better for Q&A)
            dtype = torch.float16 if torch.cuda.is_available() else torch.float32
            self.generator = pipeline(
                "text2text-generation",  # Better for Q&A than text-generation
                model=model_name,
                tokenizer=model_name,
                device=device,  # Use GPU if available
                max_length=256,  # Smaller max length for focused answers
                do_sample=False,  # Deterministic for better consistency
                model_kwargs={"dtype": dtype}  # Use dtype instead of torch_dtype
            )
            self.model_loaded = True
            print(f"✅ Model loaded successfully on {device_name}")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            print("   Falling back to CPU...")
            try:
                # Fallback to CPU
                self.generator = pipeline(
                    "text2text-generation",
                    model=model_name,
                    tokenizer=model_name,
                    device=-1,  # CPU fallback
                    max_length=256,
                    do_sample=False,
                    model_kwargs={"dtype": torch.float32}  # Use dtype instead of torch_dtype
                )
                self.model_loaded = True
                print("✅ Model loaded on CPU (fallback)")
            except Exception as e2:
                print(f"❌ CPU fallback also failed: {e2}")
                self.generator = None
                self.model_loaded = False
    
    def generate_answer(self, query: str, context_docs: List[Document], 
                       max_context_length: int = 1500) -> Dict[str, Any]:
        """Generate answer based on query and context documents"""
        
        if not self.model_loaded:
            return {
                "answer": "Language model not available. Here are the relevant document excerpts:",
                "sources": [doc.metadata.get("file_name", "Unknown") for doc in context_docs[:3]],
                "context": [doc.page_content[:200] + "..." for doc in context_docs[:3]]
            }
        
        # Prepare context from retrieved documents - more focused
        context = self._prepare_context(context_docs, max_context_length)
        
        # Create better prompt for Flan-T5
        prompt = f"""Please answer the question based on the following information:

{context}

Question: {query}
Answer:"""
        
        try:
            # Generate response with Flan-T5
            response = self.generator(
                prompt,
                max_length=150,  # Shorter for more focused answers
                num_return_sequences=1,
                truncation=True,
                clean_up_tokenization_spaces=True,
                do_sample=False  # More deterministic
            )
            
            # Extract the generated answer
            answer = response[0]['generated_text'].strip()
            
            # Clean up the answer
            answer = self._clean_answer(answer)
            
            # If answer is too short or generic, extract key info from context
            if not answer or len(answer.split()) < 5:
                answer = self._extract_key_info(context, query)
            
        except Exception as e:
            print(f"Error generating answer: {e}")
            answer = self._extract_key_info(context, query)
        
        return {
            "answer": answer,
            "sources": list(set([doc.metadata.get("file_name", "Unknown") for doc in context_docs])),
            "context": [doc.page_content for doc in context_docs],
            "confidence": self._calculate_confidence(context_docs, query)
        }
    
    def _prepare_context(self, docs: List[Document], max_length: int) -> str:
        """Prepare context string from documents"""
        context_parts = []
        current_length = 0
        
        for doc in docs:
            content = doc.page_content
            if current_length + len(content) > max_length:
                remaining = max_length - current_length
                if remaining > 100:  # Only add if significant space left
                    context_parts.append(content[:remaining] + "...")
                break
            context_parts.append(content)
            current_length += len(content)
        
        return "\n\n".join(context_parts)
    
    def _clean_answer(self, answer: str) -> str:
        """Clean and format the generated answer"""
        # Remove repetitive text
        sentences = answer.split('.')
        unique_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and sentence not in unique_sentences:
                unique_sentences.append(sentence)
        
        cleaned = '. '.join(unique_sentences)
        
        # Remove incomplete sentences at the end
        if cleaned and not cleaned.endswith('.'):
            last_period = cleaned.rfind('.')
            if last_period > len(cleaned) * 0.7:  # If last period is in last 30%
                cleaned = cleaned[:last_period + 1]
        
        return cleaned
    
    def _extract_key_info(self, context: str, query: str) -> str:
        """Extract key information from context when model fails"""
        query_words = query.lower().split()
        context_lower = context.lower()
        
        # Find sentences that contain query words
        sentences = context.split('.')
        relevant_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if any(word in sentence.lower() for word in query_words) and len(sentence) > 20:
                relevant_sentences.append(sentence)
        
        if relevant_sentences:
            # Return the most relevant sentences
            return '. '.join(relevant_sentences[:3]) + '.'
        else:
            # Return first part of context
            return context[:300] + '...'
    
    def _calculate_confidence(self, docs: List[Document], query: str) -> float:
        """Calculate confidence score based on retrieved documents"""
        if not docs:
            return 0.0
        
        # Simple confidence calculation based on number of docs and query word overlap
        query_words = set(query.lower().split())
        total_overlap = 0
        
        for doc in docs:
            doc_words = set(doc.page_content.lower().split())
            overlap = len(query_words.intersection(doc_words))
            total_overlap += overlap
        
        # Normalize confidence score
        max_possible = len(query_words) * len(docs)
        confidence = min(total_overlap / max_possible if max_possible > 0 else 0, 1.0)
        
        return confidence

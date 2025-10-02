# query_engine.py
import re
import torch
from typing import List, Dict, Any
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from langchain.schema import Document

class QueryEngine:
    def __init__(self, model_name: str = "microsoft/phi-2"):
        """
        Advanced Query Engine for SOP Knowledge Assistant with 1B+ parameter model
        
        Recommended models (in order of quality):
        1. "microsoft/phi-2" - 2.7B params, BEST for Q&A (2.5GB VRAM)
        2. "TinyLlama/TinyLlama-1.1B-Chat-v1.0" - 1.1B params, Good balance (1.2GB VRAM)
        3. "stabilityai/stablelm-2-1_6b" - 1.6B params, Very good (1.8GB VRAM)
        4. "microsoft/DialoGPT-medium" - 350M params, Lightweight fallback (400MB VRAM)
        
        Supports: Q&A, Step-by-step instructions, Future multimodal capabilities
        """
        try:
            # Check if CUDA is available and set device
            device = 0 if torch.cuda.is_available() else -1
            device_name = "GPU (CUDA)" if device == 0 else "CPU"
            
            # Determine model size for display
            model_sizes = {
                "microsoft/phi-2": "2.7B params (~2.5GB)",
                "TinyLlama/TinyLlama-1.1B-Chat-v1.0": "1.1B params (~1.2GB)",
                "stabilityai/stablelm-2-1_6b": "1.6B params (~1.8GB)",
                "microsoft/DialoGPT-medium": "350M params (~400MB)"
            }
            model_size = model_sizes.get(model_name, "Unknown size")
            
            print(f"🚀 Loading Advanced Query Engine on: {device_name}")
            print(f"📦 Model: {model_name}")
            print(f"   Size: {model_size} - Optimized for high-quality answers")
            
            if torch.cuda.is_available():
                print(f"   GPU: {torch.cuda.get_device_name(0)}")
                print(f"   GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
                print(f"   Ready for multimodal extensions")
            
            # Initialize advanced text generation pipeline with optimized settings
            dtype = torch.float16 if torch.cuda.is_available() else torch.float32
            
            # Special handling for Phi-2 and other instruction-tuned models
            if "phi-2" in model_name.lower():
                # Phi-2 specific optimizations
                self.generator = pipeline(
                    "text-generation",
                    model=model_name,
                    tokenizer=model_name,
                    device=device,
                    max_length=2048,
                    do_sample=True,
                    temperature=0.7,  # Lower for Phi-2 (more focused)
                    top_p=0.95,
                    repetition_penalty=1.15,
                    model_kwargs={"torch_dtype": dtype, "trust_remote_code": True}
                )
            elif "tinyllama" in model_name.lower():
                # TinyLlama chat optimizations
                self.generator = pipeline(
                    "text-generation",
                    model=model_name,
                    tokenizer=model_name,
                    device=device,
                    max_length=2048,
                    do_sample=True,
                    temperature=0.75,
                    top_p=0.9,
                    repetition_penalty=1.1,
                    model_kwargs={"torch_dtype": dtype}
                )
            elif "stablelm" in model_name.lower():
                # StableLM optimizations
                self.generator = pipeline(
                    "text-generation",
                    model=model_name,
                    tokenizer=model_name,
                    device=device,
                    max_length=2048,
                    do_sample=True,
                    temperature=0.8,
                    top_p=0.9,
                    repetition_penalty=1.2,
                    model_kwargs={"torch_dtype": dtype, "trust_remote_code": True}
                )
            else:
                # Default/DialoGPT configuration
                self.generator = pipeline(
                    "text-generation",
                    model=model_name,
                    tokenizer=model_name,
                    device=device,
                    max_length=2048,
                    do_sample=True,
                    temperature=0.8,
                    top_p=0.9,
                    repetition_penalty=1.1,
                    pad_token_id=50256,
                    model_kwargs={"dtype": dtype}
                )
            
            self.model_loaded = True
            self.model_name = model_name
            print(f"✅ Advanced Query Engine loaded successfully")
            print(f"   Features: Q&A, Step-by-step instructions, SOP generation ready")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            print("   Falling back to CPU or smaller model...")
            try:
                # Fallback to CPU with smaller model
                fallback_model = "microsoft/DialoGPT-medium"
                print(f"   Attempting fallback to {fallback_model} on CPU...")
                self.generator = pipeline(
                    "text-generation",
                    model=fallback_model,
                    tokenizer=fallback_model,
                    device=-1,
                    max_length=2048,
                    do_sample=True,
                    temperature=0.8,
                    top_p=0.9,
                    repetition_penalty=1.1,
                    pad_token_id=50256,
                    model_kwargs={"dtype": torch.float32}
                )
                self.model_loaded = True
                self.model_name = fallback_model
                print(f"✅ Advanced Query Engine loaded on CPU with fallback model")
            except Exception as e2:
                print(f"❌ CPU fallback also failed: {e2}")
                self.generator = None
                self.model_loaded = False
                self.model_name = None
    
    def generate_answer(self, query: str, context_docs: List[Document], 
                       max_context_length: int = 3500) -> Dict[str, Any]:
        """
        Advanced answer generation with multiple modes:
        - Standard Q&A
        - Step-by-step instructions
        - SOP generation (future)
        """
        
        if not self.model_loaded:
            return {
                "answer": "Advanced Query Engine not available. Here are the relevant document excerpts:",
                "sources": [doc.metadata.get("file_name", "Unknown") for doc in context_docs[:3]],
                "context": [doc.page_content[:200] + "..." for doc in context_docs[:3]],
                "answer_type": "fallback"
            }
        
        # Analyze query intent to determine response type
        response_type = self._analyze_query_intent(query)
        
        # Prepare context from retrieved documents
        context = self._prepare_context(context_docs, max_context_length)
        
        # Generate appropriate response based on intent
        if response_type == "step_by_step":
            answer = self._generate_step_by_step_instructions(query, context)
        elif response_type == "generate_sop":
            answer = self._generate_new_sop(query, context)
        else:
            answer = self._generate_standard_answer(query, context)
        
        return {
            "answer": answer,
            "sources": list(set([doc.metadata.get("file_name", "Unknown") for doc in context_docs])),
            "context": [doc.page_content for doc in context_docs],
            "confidence": self._calculate_confidence(context_docs, query),
            "answer_type": response_type
        }
    
    def _analyze_query_intent(self, query: str) -> str:
        """Analyze query to determine the type of response needed"""
        query_lower = query.lower()
        
        # Step-by-step instruction indicators
        step_indicators = [
            "how to", "step by step", "procedure", "process", 
            "instructions", "guide", "walkthrough", "tutorial"
        ]
        
        # SOP generation indicators
        sop_indicators = [
            "create sop", "generate sop", "new procedure", 
            "write procedure", "draft sop", "develop procedure"
        ]
        
        if any(indicator in query_lower for indicator in step_indicators):
            return "step_by_step"
        elif any(indicator in query_lower for indicator in sop_indicators):
            return "generate_sop"
        else:
            return "standard_qa"
    
    def _generate_standard_answer(self, query: str, context: str) -> str:
        """Generate standard Q&A response"""
        prompt = f"""Based on the SOP documentation below, provide a comprehensive and accurate answer.

SOP Documentation:
{context}

Question: {query}

Detailed Answer:"""
        
        return self._generate_response(prompt, temperature=0.7, max_tokens=300)
    
    def _generate_step_by_step_instructions(self, query: str, context: str) -> str:
        """Generate detailed step-by-step instructions"""
        prompt = f"""Based on the SOP documentation, create detailed step-by-step instructions for the following request.

SOP Documentation:
{context}

Request: {query}

Step-by-Step Instructions:

1."""
        
        response = self._generate_response(prompt, temperature=0.8, max_tokens=400)
        
        # Ensure proper step formatting
        if not response.startswith("1."):
            response = "1. " + response
            
        return self._format_step_by_step(response)
    
    def _generate_new_sop(self, query: str, context: str) -> str:
        """Generate new SOP based on existing procedures (future feature)"""
        prompt = f"""Based on the existing SOP documentation, create a new Standard Operating Procedure for the following requirement.

Existing SOP Documentation:
{context}

Requirement: {query}

NEW STANDARD OPERATING PROCEDURE

Title: [Generated based on requirement]

Purpose:"""
        
        return self._generate_response(prompt, temperature=0.9, max_tokens=500)
    
    def _generate_response(self, prompt: str, temperature: float = 0.7, max_tokens: int = 300) -> str:
        """Core response generation with error handling and smart fallback"""
        try:
            response = self.generator(
                prompt,
                max_new_tokens=max_tokens,
                num_return_sequences=1,
                truncation=True,
                do_sample=True,
                temperature=temperature,
                top_p=0.9,
                repetition_penalty=1.1,
                pad_token_id=50256
            )
            
            # Extract generated text
            full_text = response[0]['generated_text']
            generated_part = full_text[len(prompt):].strip()
            
            # Clean and format response
            cleaned_response = self._clean_and_format_response(generated_part)
            
            # If response is too short or empty, use document-based extraction
            if not cleaned_response or len(cleaned_response.split()) < 10:
                print("Generated response too short, using document extraction")
                return self._extract_from_context(prompt)
            
            return cleaned_response
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return self._extract_from_context(prompt)
    
    def _extract_from_context(self, prompt: str) -> str:
        """Extract relevant information directly from the context in the prompt"""
        # Find the context section in the prompt
        context_markers = ["Context:", "Documentation:", "SOP Documentation:"]
        question_markers = ["Question:", "Request:", "Query:"]
        
        context_start = -1
        for marker in context_markers:
            pos = prompt.find(marker)
            if pos != -1:
                context_start = pos
                break
        
        question_start = -1
        for marker in question_markers:
            pos = prompt.find(marker)
            if pos != -1:
                question_start = pos
                break
        
        if context_start != -1 and question_start != -1:
            # Extract context and clean it
            context_section = prompt[context_start:question_start]
            for marker in context_markers:
                context_section = context_section.replace(marker, "")
            context = context_section.strip()
            
            # Extract the question
            question_section = prompt[question_start:]
            for marker in question_markers:
                question_section = question_section.replace(marker, "")
            question = question_section.split("\n")[0].strip()
            
            # Use the existing key info extraction
            return self._extract_key_information(context, question)
        
        return "Unable to process the request. Please check the document content."
    
    def _extract_key_information(self, context: str, query: str) -> str:
        """Smart extraction of key information from context"""
        if not context or not query:
            return "No context or query provided."
        
        query_lower = query.lower()
        
        # Check if this is a step-by-step request
        is_step_request = any(word in query_lower for word in ['step', 'procedure', 'process', 'how to', 'guide'])
        
        # Split context into meaningful chunks
        # First try line-based splitting for better structure preservation
        if '\n' in context:
            lines = [line.strip() for line in context.split('\n') if line.strip()]
            # Filter out very short lines and combine related ones
            chunks = []
            current_chunk = ""
            
            for line in lines:
                if len(line) < 15:  # Very short line, might be a fragment
                    current_chunk += " " + line if current_chunk else line
                elif current_chunk:
                    # Complete the previous chunk and start a new one
                    chunks.append(current_chunk.strip())
                    current_chunk = line
                else:
                    chunks.append(line)
            
            # Don't forget the last chunk
            if current_chunk:
                chunks.append(current_chunk.strip())
        else:
            # Fall back to sentence splitting
            chunks = re.split(r'[.!?]+', context)
            chunks = [chunk.strip() for chunk in chunks if len(chunk.strip()) > 15]
        
        # Remove duplicate chunks (common issue)
        unique_chunks = []
        seen = set()
        for chunk in chunks:
            # Create a normalized version for comparison
            normalized = re.sub(r'\s+', ' ', chunk.lower().strip())
            if normalized not in seen and len(normalized) > 20:
                unique_chunks.append(chunk)
                seen.add(normalized)
        
        chunks = unique_chunks
        
        # Score chunks based on relevance to query
        query_words = set(word.lower() for word in query.split() if len(word) > 2)
        scored_chunks = []
        
        for chunk in chunks:
            chunk_words = set(word.lower() for word in chunk.split())
            overlap = len(query_words.intersection(chunk_words))
            
            # Boost score for procedural keywords if step request
            if is_step_request:
                procedural_words = {'step', 'first', 'then', 'next', 'finally', 'procedure', 'process', 'perform', 'prepared', 'covering'}
                procedural_overlap = len(procedural_words.intersection(chunk_words))
                overlap += procedural_overlap * 2
            
            # Boost score for specific domain terms
            domain_words = {'defect', 'list', 'repair', 'annual', 'vessel', 'master', 'engine', 'deck'}
            domain_overlap = len(domain_words.intersection(chunk_words))
            overlap += domain_overlap
            
            if overlap > 0:
                score = overlap / max(len(query_words), 1)
                scored_chunks.append((chunk, score))
        
        # Sort by relevance and take top chunks
        scored_chunks.sort(key=lambda x: x[1], reverse=True)
        
        if scored_chunks:
            # Take top relevant chunks, but ensure we get a complete answer
            top_chunks = [chunk[0] for chunk in scored_chunks[:8]]
            
            if is_step_request:
                # Format as steps if it's a procedural request
                formatted_steps = []
                step_num = 1
                for chunk in top_chunks:
                    # Check if chunk already has numbering
                    if re.match(r'^\d+\.?\s+', chunk.strip()):
                        formatted_steps.append(chunk.strip())
                    elif any(marker in chunk.lower() for marker in ['i.', 'ii.', 'iii.', 'a.', 'b.', 'c.']):
                        formatted_steps.append(f"  {chunk.strip()}")  # Sub-point
                    else:
                        formatted_steps.append(f"{step_num}. {chunk.strip()}")
                        step_num += 1
                return '\n'.join(formatted_steps)
            else:
                # For regular Q&A, create a coherent narrative
                result = []
                for chunk in top_chunks:
                    # Clean up the chunk
                    clean_chunk = chunk.strip()
                    if clean_chunk and not clean_chunk.endswith('.'):
                        clean_chunk += '.'
                    result.append(clean_chunk)
                
                return ' '.join(result)
        else:
            # If no matches, return first few meaningful chunks
            if chunks:
                return '. '.join(chunks[:3]) + '.'
            return "No specific information found for your query in the available documents."
    
    def _format_step_by_step(self, text: str) -> str:
        """Format text as proper step-by-step instructions"""
        lines = text.split('\n')
        formatted_steps = []
        step_counter = 1
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # If line doesn't start with a number, make it a step
            if not re.match(r'^\d+\.', line):
                line = f"{step_counter}. {line}"
                step_counter += 1
            
            formatted_steps.append(line)
        
        return '\n'.join(formatted_steps)
    
    def _clean_and_format_response(self, response: str) -> str:
        """Clean and format the generated response"""
        if not response:
            return "No response generated."
        
        # Basic cleaning
        response = response.strip()
        
        # Remove repetitive patterns
        lines = response.split('\n')
        unique_lines = []
        for line in lines:
            line = line.strip()
            if line and line not in unique_lines:
                unique_lines.append(line)
        
        cleaned = '\n'.join(unique_lines)
        
        # Ensure proper sentence endings
        if cleaned and not cleaned.endswith(('.', '!', '?', ':')):
            # Find last complete sentence
            last_period = cleaned.rfind('.')
            if last_period > len(cleaned) * 0.7:
                cleaned = cleaned[:last_period + 1]
        
        return cleaned
    
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
    
    # Future: Multimodal capabilities preparation
    def _prepare_multimodal_context(self, context_docs: List[Document], images: List = None) -> str:
        """
        Future method for multimodal context preparation
        Will integrate text + images for comprehensive SOP understanding
        """
        # Currently text-only, ready for image integration
        return self._prepare_context(context_docs, 3500)
    
    def _generate_sop_with_images(self, query: str, context: str, images: List = None) -> str:
        """
        Future method for generating SOPs with visual elements
        Will create comprehensive SOPs with text + diagrams/images
        """
        # Placeholder for future multimodal SOP generation
        return self._generate_new_sop(query, context)
    
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

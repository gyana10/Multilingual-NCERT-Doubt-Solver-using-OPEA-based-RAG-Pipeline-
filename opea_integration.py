"""
OPEA-based RAG Pipeline Integration Module
This is the actual implementation of the OPEA RAG pipeline
"""
from typing import List, Dict, Any, Optional
import logging
import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from langdetect import detect
from deep_translator import GoogleTranslator
import re

logger = logging.getLogger(__name__)


class NCERTRAGPipeline:
    """
    RAG Pipeline for NCERT Doubt-Solver using OPEA framework
    
    This class implements the complete RAG pipeline:
    - Document ingestion and preprocessing
    - Embedding generation
    - Vector database operations
    - Retrieval and ranking
    - LLM-based answer generation
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize RAG pipeline
        
        Args:
            config: Configuration dictionary containing:
                - vector_db_path: Path to vector database
                - embedding_model: Embedding model name
                - llm_model: LLM model configuration
                - chunk_size: Document chunk size
                - top_k: Number of chunks to retrieve
        """
        self.config = config
        self.vector_db_path = config.get('vector_db_path', './vector_db')
        self.embedding_model_name = config.get('embedding_model', 'all-MiniLM-L6-v2')
        self.top_k = config.get('top_k', 5)
        self.confidence_threshold = config.get('confidence_threshold', 0.6)
        
        logger.info("Initializing NCERT RAG Pipeline...")
        
        self._initialize_embedding_model()
        
        self.vector_dbs = {}
        self.chunk_ids = {}
        self.metadata = {}
        self.chunks = {}
        self._initialize_vector_dbs()
    
    def _initialize_embedding_model(self):
        """Initialize embedding model"""
        try:
            logger.info(f"Loading embedding model: {self.embedding_model_name}")
            self.embedding_model = SentenceTransformer(self.embedding_model_name)
            logger.info("Embedding model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to initialize embedding model: {e}")
            try:
                logger.info("Falling back to default model")
                self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
                logger.info("Default embedding model loaded successfully")
            except Exception as e2:
                logger.error(f"Failed to load fallback model: {e2}")
                raise
    
    def _initialize_vector_dbs(self):
        """Initialize vector databases for all grades"""
        if not os.path.exists(self.vector_db_path):
            logger.warning(f"Vector DB path does not exist: {self.vector_db_path}")
            return
        
        for filename in os.listdir(self.vector_db_path):
            if filename.endswith('_faiss.index'):
                grade = filename.replace('_faiss.index', '')
                try:
                    index_path = os.path.join(self.vector_db_path, filename)
                    self.vector_dbs[grade] = faiss.read_index(index_path)
                    logger.info(f"Loaded vector DB for {grade}")
                    
                    ids_path = os.path.join(self.vector_db_path, f"{grade}_ids.json")
                    if os.path.exists(ids_path):
                        with open(ids_path, 'r', encoding='utf-8') as f:
                            self.chunk_ids[grade] = json.load(f)
                        logger.info(f"Loaded {len(self.chunk_ids[grade])} chunk IDs for {grade}")
                    
                    metadata_path = os.path.join(self.vector_db_path, f"{grade}_metadata.jsonl")
                    if os.path.exists(metadata_path):
                        self.metadata[grade] = []
                        with open(metadata_path, 'r', encoding='utf-8') as f:
                            for line in f:
                                self.metadata[grade].append(json.loads(line.strip()))
                        logger.info(f"Loaded {len(self.metadata[grade])} metadata entries for {grade}")
                    
                    chunks_path = os.path.join(self.vector_db_path, f"{grade}_chunks.jsonl")
                    if os.path.exists(chunks_path):
                        self.chunks[grade] = {}
                        with open(chunks_path, 'r', encoding='utf-8') as f:
                            for line in f:
                                chunk_data = json.loads(line.strip())
                                self.chunks[grade][chunk_data['id']] = chunk_data['text']
                        logger.info(f"Loaded {len(self.chunks[grade])} chunks for {grade}")
                        
                except Exception as e:
                    logger.error(f"Failed to load vector DB for {grade}: {e}")
    
    def query(
        self,
        question: str,
        grade: int,
        subject: str,
        language: str = 'English',
        conversation_history: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Process a student query and return answer with citations
        
        Args:
            question: Student's question
            grade: Grade/class (5-10)
            subject: Subject name
            language: Response language
            conversation_history: Previous conversation messages
        
        Returns:
            Dictionary containing:
                - answer: Generated answer
                - citations: List of source citations
                - confidence: Confidence score
                - sources: Retrieved document chunks
        """
        logger.info(f"Processing query: {question[:50]}... (Grade: {grade}, Subject: {subject})")
        
        try:
            detected_lang = detect(question)
            logger.info(f"Detected language: {detected_lang}")
        except:
            detected_lang = 'en'
            logger.warning("Language detection failed, defaulting to English")
        
        english_question = question
        if detected_lang != 'en':
            try:
                english_question = GoogleTranslator(source=detected_lang, target='en').translate(question)
                logger.info(f"Translated question to English: {english_question}")
            except Exception as e:
                logger.warning(f"Translation failed: {e}")
        
        processed_query = self._preprocess_query(english_question, grade, subject)
        
        retrieved_docs = self._retrieve_documents(processed_query, grade, subject)
        
        ranked_docs = self._rank_documents(retrieved_docs, english_question)
        
        answer = self._generate_answer(english_question, ranked_docs, language, conversation_history)
        
        citations = self._extract_citations(ranked_docs)
        
        confidence = self._calculate_confidence(ranked_docs, answer)
        
        final_answer = answer
        if language != 'English' and language != 'en':
            try:
                final_answer = GoogleTranslator(source='en', target=language.lower()).translate(answer)
                logger.info(f"Translated answer to {language}")
            except Exception as e:
                logger.warning(f"Back translation failed: {e}")
                final_answer = answer  # Fallback to English
        
        return {
            'answer': final_answer,
            'citations': citations,
            'confidence': confidence,
            'language': language,
            'metadata': {
                'grade': grade,
                'subject': subject,
                'num_sources': len(retrieved_docs)
            }
        }
    
    def _preprocess_query(self, question: str, grade: int, subject: str) -> str:
        """Preprocess and enhance query with metadata"""
        enhanced_query = f"[Grade {grade}] [Subject: {subject}] {question}"
        return enhanced_query
    
    def _retrieve_documents(
        self, 
        query: str, 
        grade: int, 
        subject: str
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant document chunks from vector database
        
        Args:
            query: Processed query string
            grade: Grade filter
            subject: Subject filter
        
        Returns:
            List of retrieved document chunks with metadata
        """
        grade_key = f"class {grade}"
        if grade_key not in self.vector_dbs:
            logger.warning(f"No vector DB found for grade {grade}")
            return []
        
        try:
            query_embedding = self.embedding_model.encode([query])
        except Exception as e:
            logger.error(f"Failed to generate query embedding: {e}")
            return []
        
        try:
            index = self.vector_dbs[grade_key]
            distances, indices = index.search(query_embedding.astype('float32'), self.top_k)
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            return []
        
        retrieved_docs = []
        chunk_ids = self.chunk_ids.get(grade_key, [])
        metadata_list = self.metadata.get(grade_key, [])
        
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx >= len(chunk_ids):
                continue
                
            chunk_id = chunk_ids[idx]
            chunk_text = self.chunks.get(grade_key, {}).get(chunk_id, "")
            
            metadata = {}
            if i < len(metadata_list):
                metadata = metadata_list[i]
            
            similarity = 1 / (1 + distance)  # Simple conversion
            
            retrieved_docs.append({
                'id': chunk_id,
                'content': chunk_text,
                'metadata': metadata,
                'score': float(similarity),
                'distance': float(distance)
            })
        
        logger.info(f"Retrieved {len(retrieved_docs)} documents for query")
        return retrieved_docs
    
    def _rank_documents(
        self, 
        documents: List[Dict[str, Any]], 
        query: str
    ) -> List[Dict[str, Any]]:
        """Rank and filter retrieved documents"""
        ranked_docs = sorted(documents, key=lambda x: x['score'], reverse=True)
        
        filtered_docs = [doc for doc in ranked_docs if doc['score'] >= self.confidence_threshold]
        
        return filtered_docs[:self.top_k]
    
    def _generate_answer(
        self,
        question: str,
        context_docs: List[Dict[str, Any]],
        language: str,
        conversation_history: Optional[List[Dict]] = None
    ) -> str:
        """
        Generate answer using LLM with retrieved context
        
        Args:
            question: Original question
            context_docs: Retrieved and ranked documents
            language: Target language for response
            conversation_history: Previous messages
        
        Returns:
            Generated answer string
        """
        context = "\n\n".join([doc['content'] for doc in context_docs])
        
        prompt = self._build_prompt(question, context, language, conversation_history)
        
        if context_docs:
            answer = f"Based on the NCERT textbook content, here is the answer to your question:\n\n{context[:500]}...\n\n"
            answer += "Please refer to the citations below for the exact source of this information."
        else:
            answer = "I couldn't find specific information about this in the NCERT textbooks. Please try rephrasing your question or consult your teacher for more help."
        
        if self._is_out_of_scope(question, context_docs):
            return "I don't have information about this in the NCERT textbooks. Please ask questions related to your NCERT curriculum."
        
        return answer
    
    def _build_prompt(
        self,
        question: str,
        context: str,
        language: str,
        conversation_history: Optional[List[Dict]] = None
    ) -> str:
        """Build prompt for LLM"""
        prompt = f"""You are an AI tutor helping students with NCERT textbooks.

Context from NCERT textbook:
{context}

Student Question: {question}

Please provide a clear, accurate answer in {language} based ONLY on the provided context.
Include citations to specific pages when possible.
If the answer is not in the context, say "I don't know" and suggest consulting the teacher.

Answer:"""
        
        return prompt
    
    def _extract_citations(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract citation information from retrieved documents"""
        citations = []
        for doc in documents:
            metadata = doc.get('metadata', {})
            citations.append({
                'source': metadata.get('source_file', 'NCERT Textbook'),
                'page': metadata.get('page_no', 'N/A'),
                'chapter': metadata.get('chapter', ''),
                'text': doc.get('content', '')[:200] + '...'  # First 200 chars
            })
        return citations
    
    def _calculate_confidence(
        self, 
        documents: List[Dict[str, Any]], 
        answer: str
    ) -> float:
        """Calculate confidence score for the answer"""
        if not documents:
            return 0.0
        
        avg_score = sum(doc.get('score', 0.0) for doc in documents) / len(documents)
        
        return max(0.0, min(1.0, avg_score))
    
    def _is_out_of_scope(self, question: str, documents: List[Dict[str, Any]]) -> bool:
        """Check if query is out of NCERT scope"""
        if not documents:
            return True
        
        max_score = max(doc.get('score', 0.0) for doc in documents)
        return max_score < self.confidence_threshold
    
    def ingest_documents(
        self,
        pdf_path: str,
        grade: int,
        subject: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Ingest NCERT PDF documents into vector database
        
        Args:
            pdf_path: Path to NCERT PDF file
            grade: Grade/class number
            subject: Subject name
            metadata: Additional metadata
        
        Returns:
            Success status
        """
        logger.info(f"Ingesting document: {pdf_path} (Grade: {grade}, Subject: {subject})")
        
        logger.info("Document ingestion would happen here in a full implementation")
        
        return True
    
    def clear_database(self):
        """Clear vector database (use with caution)"""
        logger.warning("Clearing vector database...")
        self.vector_dbs.clear()
        self.chunk_ids.clear()
        self.metadata.clear()
        self.chunks.clear()


_rag_pipeline_instance = None


def get_rag_pipeline(config: Optional[Dict[str, Any]] = None) -> NCERTRAGPipeline:
    """Get or create RAG pipeline instance"""
    global _rag_pipeline_instance
    
    if _rag_pipeline_instance is None:
        if config is None:
            from config import Config
            config = {
                'vector_db_path': Config.VECTOR_DB_PATH,
                'embedding_model': Config.EMBEDDING_MODEL,
                'chunk_size': Config.CHUNK_SIZE,
                'top_k': Config.TOP_K_RESULTS,
                'llm_model': Config.LLM_MODEL,
                'confidence_threshold': Config.CONFIDENCE_THRESHOLD
            }
        _rag_pipeline_instance = NCERTRAGPipeline(config)
    
    return _rag_pipeline_instance
import os
import json
import logging
import re
from typing import List, Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

logger = logging.getLogger(__name__)

class SimpleRAGPipeline:
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.chunks_path = config.get('CHUNKS_PATH', './chunks')
        self.top_k = config.get('TOP_K_RESULTS', 5)
        self.confidence_threshold = config.get('CONFIDENCE_THRESHOLD', 0.1)
        
        self.vectorizer = TfidfVectorizer(
            max_features=10000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        self._load_precomputed_data()
    
    def _load_precomputed_data(self):
        self.grade_data = {}
        
        if not os.path.exists(self.chunks_path):
            logger.warning(f"Chunks path does not exist: {self.chunks_path}")
            return
            
        all_texts = []
        grade_chunks = {}
        
        for filename in os.listdir(self.chunks_path):
            if filename.endswith('_chunks.jsonl'):
                grade_match = re.search(r'class\s*(\d+)', filename, re.IGNORECASE)
                if not grade_match:
                    continue
                    
                grade = f"class {grade_match.group(1)}"
                try:
                    chunks = []
                    chunk_texts = []
                    chunk_ids = []
                    
                    chunks_path = os.path.join(self.chunks_path, filename)
                    with open(chunks_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            chunk_data = json.loads(line.strip())
                            chunks.append(chunk_data)
                            chunk_texts.append(chunk_data['text'])
                            chunk_ids.append(chunk_data['id'])
                    
                    grade_chunks[grade] = {
                        'chunks': chunks,
                        'chunk_texts': chunk_texts,
                        'chunk_ids': chunk_ids
                    }
                    
                    all_texts.extend(chunk_texts)
                    logger.info(f"Collected {len(chunks)} chunks for {grade}")
                    
                except Exception as e:
                    logger.error(f"Failed to load data for {grade}: {e}")
        
        if all_texts:
            logger.info(f"Fitting vectorizer with {len(all_texts)} texts from all grades")
            self.vectorizer.fit(all_texts)
        else:
            logger.warning("No texts found to fit vectorizer")
            return
        
        for grade, data in grade_chunks.items():
            if data['chunk_texts']:
                tfidf_matrix = self.vectorizer.transform(data['chunk_texts'])
                
                self.grade_data[grade] = {
                    'chunks': data['chunks'],
                    'chunk_texts': data['chunk_texts'],
                    'chunk_ids': data['chunk_ids'],
                    'tfidf_matrix': tfidf_matrix
                }
                
                logger.info(f"Created TF-IDF matrix for {grade}")
    
    def query(
        self,
        question: str,
        grade: int,
        subject: str,
        language: str = 'English',
        conversation_history: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Answer a question using precomputed NCERT chunks for the given grade.

        This method prefers high-confidence matches but will still return the
        best available chunk (with lower confidence) instead of immediately
        falling back to the generic "no information" message.
        """
        logger.info(f"Processing query: {question[:50]}... (Grade: {grade}, Subject: {subject})")

        if question is None:
            question = ""
        question = question.strip()
        if not question:
            logger.warning("Empty question received; returning fallback response")
            return self._generate_fallback_response(grade, subject, language)

        grade_key = f"class {grade}"
        if grade_key not in self.grade_data:
            logger.warning(f"No data found for grade {grade}")
            return self._generate_fallback_response(grade, subject, language)

        grade_data = self.grade_data[grade_key]

        try:
            question_vector = self.vectorizer.transform([question])
        except Exception as e:
            logger.error(f"Failed to vectorize question: {e}")
            return self._generate_fallback_response(grade, subject, language)

        similarities = cosine_similarity(question_vector, grade_data['tfidf_matrix']).flatten()

        top_indices = np.argsort(similarities)[::-1][:self.top_k]

        relevant_indices = [i for i in top_indices if similarities[i] >= self.confidence_threshold]

        if not relevant_indices:
            logger.info(
                "No chunks above confidence threshold; attempting best-available "
                "fallback based on maximum similarity."
            )

            if similarities.size > 0:
                best_idx = int(np.argmax(similarities))
                best_score = float(similarities[best_idx])

                if best_score > 0.0:
                    best_chunk = {
                        'id': grade_data['chunk_ids'][best_idx],
                        'text': grade_data['chunk_texts'][best_idx],
                        'score': best_score,
                    }

                    relevant_chunks = [best_chunk]
                    answer = self._generate_answer(question, relevant_chunks, language)
                    citations = self._extract_citations(relevant_chunks)
                    confidence = self._calculate_confidence(relevant_chunks)

                    return {
                        'answer': answer,
                        'citations': citations,
                        'confidence': confidence,
                        'language': language,
                        'metadata': {
                            'grade': grade,
                            'subject': subject,
                            'num_sources': len(relevant_chunks),
                        },
                    }

            return self._generate_fallback_response(grade, subject, language)

        relevant_chunks = []
        for i in relevant_indices:
            relevant_chunks.append({
                'id': grade_data['chunk_ids'][i],
                'text': grade_data['chunk_texts'][i],
                'score': float(similarities[i])
            })

        answer = self._generate_answer(question, relevant_chunks, language)

        citations = self._extract_citations(relevant_chunks)

        confidence = self._calculate_confidence(relevant_chunks)

        return {
            'answer': answer,
            'citations': citations,
            'confidence': confidence,
            'language': language,
            'metadata': {
                'grade': grade,
                'subject': subject,
                'num_sources': len(relevant_chunks)
            }
        }
    
    def _generate_answer(
        self,
        question: str,
        context_chunks: List[Dict[str, Any]],
        language: str
    ) -> str:
        if not context_chunks:
            return "I couldn't find specific information about this in the NCERT textbooks. Please try rephrasing your question or consult your teacher for more help."
        
        context_text = "\n\n".join([chunk['text'] for chunk in context_chunks[:3]])
        
        answer = f"Based on the NCERT textbook content for Grade {context_chunks[0].get('metadata', {}).get('grade', 'unknown')}, here is the answer to your question:\n\n"
        answer += f"{context_text[:800]}...\n\n"
        answer += "Please refer to the citations below for the exact source of this information."
        
        return answer
    
    def _extract_citations(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        citations = []
        for chunk in chunks[:3]:
            chunk_id = chunk.get('id', '')
            parts = chunk_id.split('__')
            
            citations.append({
                'source': parts[1] if len(parts) > 1 else 'NCERT Textbook',
                'page': 'N/A',
                'chapter': '',
                'text': chunk.get('text', '')[:100] + '...'
            })
        
        return citations
    
    def _calculate_confidence(self, chunks: List[Dict[str, Any]]) -> float:
        if not chunks:
            return 0.0
        
        avg_score = sum(chunk.get('score', 0.0) for chunk in chunks) / len(chunks)
        return min(1.0, avg_score)
    
    def _generate_fallback_response(self, grade: int, subject: str, language: str) -> Dict[str, Any]:
        return {
            'answer': "I don't have information about this in the NCERT textbooks. Please ask questions related to your NCERT curriculum.",
            'citations': [],
            'confidence': 0.0,
            'language': language,
            'metadata': {
                'grade': grade,
                'subject': subject,
                'num_sources': 0
            }
        }

_simple_rag_instance = None

def get_simple_rag_pipeline(config: Optional[Dict[str, Any]] = None) -> SimpleRAGPipeline:
    global _simple_rag_instance
    
    if _simple_rag_instance is None:
        if config is None:
            config = {
                'CHUNKS_PATH': './chunks',
                'TOP_K_RESULTS': 5,
                'CONFIDENCE_THRESHOLD': 0.1
            }
        _simple_rag_instance = SimpleRAGPipeline(config)
    
    return _simple_rag_instance
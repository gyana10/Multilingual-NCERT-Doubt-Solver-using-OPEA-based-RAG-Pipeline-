"""
Document Ingestion Pipeline for NCERT Doubt Solver
Handles PDF processing, OCR, chunking, and embedding generation
"""
import os
import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import pymupdf as fitz
import pdfplumber
import pytesseract
from PIL import Image
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from langdetect import detect
import re

logger = logging.getLogger(__name__)

class DocumentIngestionPipeline:
    """Pipeline for ingesting NCERT documents and preparing them for RAG"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the document ingestion pipeline
        
        Args:
            config: Configuration dictionary with:
                - chunk_size: Size of text chunks
                - chunk_overlap: Overlap between chunks
                - embedding_model: Name of sentence transformer model
                - vector_db_path: Path to store FAISS indexes
        """
        self.config = config
        self.chunk_size = config.get('chunk_size', 512)
        self.chunk_overlap = config.get('chunk_overlap', 50)
        self.embedding_model_name = config.get('embedding_model', 'sentence-transformers/all-MiniLM-L6-v2')
        self.vector_db_path = config.get('vector_db_path', './vector_db')
        
        logger.info(f"Loading embedding model: {self.embedding_model_name}")
        self.embedding_model = SentenceTransformer(self.embedding_model_name)
        
        os.makedirs(self.vector_db_path, exist_ok=True)
    
    def extract_text_from_pdf(self, pdf_path: str) -> List[Dict[str, Any]]:
        """
        Extract text from PDF with OCR for scanned pages
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of dictionaries with page text and metadata
        """
        pages_content = []
        
        try:
            logger.info(f"Extracting text from {pdf_path} using PyMuPDF")
            doc = fitz.open(pdf_path)
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text()
                
                if not text.strip():
                    logger.info(f"Page {page_num} appears to be scanned, performing OCR")
                    pix = page.get_pixmap()
                    img_data = pix.tobytes("png")
                    image = Image.open(io.BytesIO(img_data))
                    text = pytesseract.image_to_string(image)
                
                pages_content.append({
                    'page_num': page_num + 1,
                    'text': text,
                    'source_file': os.path.basename(pdf_path)
                })
            
            doc.close()
            
        except Exception as e:
            logger.warning(f"PyMuPDF failed for {pdf_path}: {e}")
            
            try:
                logger.info(f"Extracting text from {pdf_path} using pdfplumber")
                with pdfplumber.open(pdf_path) as pdf:
                    for page_num, page in enumerate(pdf.pages):
                        text = page.extract_text()
                        
                        if not text or not text.strip():
                            logger.info(f"Page {page_num} appears to be scanned, performing OCR")
                            img = page.to_image(resolution=200)
                            text = pytesseract.image_to_string(img.original)
                        
                        pages_content.append({
                            'page_num': page_num + 1,
                            'text': text,
                            'source_file': os.path.basename(pdf_path)
                        })
            except Exception as e2:
                logger.error(f"All extraction methods failed for {pdf_path}: {e2}")
                raise
        
        return pages_content
    
    def chunk_text(self, pages_content: List[Dict[str, Any]], metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Split text into chunks with metadata
        
        Args:
            pages_content: List of page content dictionaries
            metadata: Additional metadata (grade, subject, etc.)
            
        Returns:
            List of chunk dictionaries with text and metadata
        """
        chunks = []
        chunk_id_counter = 0
        
        for page_content in pages_content:
            text = page_content['text']
            page_num = page_content['page_num']
            source_file = page_content['source_file']
            
            text = self._clean_text(text)
            
            sentences = re.split(r'[.!?]+', text)
            current_chunk = ""
            current_chunk_sentences = []
            
            for sentence in sentences:
                sentence = sentence.strip()
                if not sentence:
                    continue
                
                if len(current_chunk) + len(sentence) + 1 > self.chunk_size and current_chunk:
                    chunk_id = f"{metadata['grade']}__{metadata['subject']}__p{page_num}__c{chunk_id_counter}"
                    chunks.append({
                        'id': chunk_id,
                        'text': current_chunk.strip(),
                        'metadata': {
                            'grade': metadata['grade'],
                            'subject': metadata['subject'],
                            'chapter': metadata.get('chapter', ''),
                            'page_no': page_num,
                            'source_file': source_file,
                            'language': self._detect_language(current_chunk)
                        }
                    })
                    chunk_id_counter += 1
                    
                    overlap_sentences = max(1, len(current_chunk_sentences) // 3)
                    current_chunk_sentences = current_chunk_sentences[-overlap_sentences:] if overlap_sentences > 0 else []
                    current_chunk = " ".join(current_chunk_sentences) + " " + sentence + " "
                else:
                    current_chunk += sentence + " "
                    current_chunk_sentences.append(sentence)
            
            if current_chunk.strip():
                chunk_id = f"{metadata['grade']}__{metadata['subject']}__p{page_num}__c{chunk_id_counter}"
                chunks.append({
                    'id': chunk_id,
                    'text': current_chunk.strip(),
                    'metadata': {
                        'grade': metadata['grade'],
                        'subject': metadata['subject'],
                        'chapter': metadata.get('chapter', ''),
                        'page_no': page_num,
                        'source_file': source_file,
                        'language': self._detect_language(current_chunk)
                    }
                })
                chunk_id_counter += 1
        
        logger.info(f"Created {len(chunks)} chunks from {len(pages_content)} pages")
        return chunks
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text"""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s.,!?;:()\-\n]', '', text)
        return text.strip()
    
    def _detect_language(self, text: str) -> str:
        """Detect language of text"""
        try:
            return detect(text[:100])  # Detect on first 100 chars for efficiency
        except:
            return 'unknown'
    
    def generate_embeddings(self, chunks: List[Dict[str, Any]]) -> np.ndarray:
        """
        Generate embeddings for text chunks
        
        Args:
            chunks: List of chunk dictionaries
            
        Returns:
            numpy array of embeddings
        """
        texts = [chunk['text'] for chunk in chunks]
        logger.info(f"Generating embeddings for {len(texts)} chunks")
        embeddings = self.embedding_model.encode(texts, show_progress_bar=True)
        return embeddings
    
    def create_vector_index(self, embeddings: np.ndarray, chunks: List[Dict[str, Any]]) -> str:
        """
        Create FAISS index and save it with chunk IDs
        
        Args:
            embeddings: Array of embeddings
            chunks: List of chunk dictionaries
            
        Returns:
            Path to saved index file
        """
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings.astype('float32'))
        
        grade = chunks[0]['metadata']['grade'] if chunks else 'unknown'
        index_path = os.path.join(self.vector_db_path, f"{grade}_faiss.index")
        faiss.write_index(index, index_path)
        
        ids_path = os.path.join(self.vector_db_path, f"{grade}_ids.json")
        chunk_ids = [chunk['id'] for chunk in chunks]
        with open(ids_path, 'w', encoding='utf-8') as f:
            json.dump(chunk_ids, f, ensure_ascii=False, indent=2)
        
        metadata_path = os.path.join(self.vector_db_path, f"{grade}_metadata.jsonl")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            for chunk in chunks:
                f.write(json.dumps(chunk['metadata'], ensure_ascii=False) + '\n')
        
        chunks_path = os.path.join(self.vector_db_path, f"{grade}_chunks.jsonl")
        with open(chunks_path, 'w', encoding='utf-8') as f:
            for chunk in chunks:
                chunk_data = {
                    'id': chunk['id'],
                    'text': chunk['text']
                }
                f.write(json.dumps(chunk_data, ensure_ascii=False) + '\n')
        
        logger.info(f"Saved vector index to {index_path}")
        logger.info(f"Saved {len(chunk_ids)} chunk IDs to {ids_path}")
        logger.info(f"Saved metadata to {metadata_path}")
        logger.info(f"Saved chunks to {chunks_path}")
        
        return index_path
    
    def process_document(self, pdf_path: str, grade: str, subject: str, chapter: str = '') -> str:
        """
        Process a single document through the entire pipeline
        
        Args:
            pdf_path: Path to PDF file
            grade: Grade level (e.g., '5', '6', etc.)
            subject: Subject name
            chapter: Chapter name (optional)
            
        Returns:
            Path to saved FAISS index
        """
        logger.info(f"Processing document: {pdf_path}")
        
        pages_content = self.extract_text_from_pdf(pdf_path)
        
        metadata = {
            'grade': grade,
            'subject': subject,
            'chapter': chapter
        }
        chunks = self.chunk_text(pages_content, metadata)
        
        chunks_file = os.path.join(self.vector_db_path, f"{grade}_{subject}_chunks.jsonl")
        with open(chunks_file, 'w', encoding='utf-8') as f:
            for chunk in chunks:
                f.write(json.dumps(chunk, ensure_ascii=False) + '\n')
        
        embeddings = self.generate_embeddings(chunks)
        
        index_path = self.create_vector_index(embeddings, chunks)
        
        logger.info(f"Document processing completed for {pdf_path}")
        return index_path

def process_ncert_directory(ncert_dir: str, output_dir: str):
    """
    Process all NCERT documents in a directory
    
    Args:
        ncert_dir: Path to NCERT directory
        output_dir: Path to output directory
    """
    config = {
        'chunk_size': 512,
        'chunk_overlap': 50,
        'embedding_model': 'sentence-transformers/all-MiniLM-L6-v2',
        'vector_db_path': output_dir
    }
    
    pipeline = DocumentIngestionPipeline(config)
    
    for class_dir in os.listdir(ncert_dir):
        class_path = os.path.join(ncert_dir, class_dir)
        if not os.path.isdir(class_path):
            continue
            
        grade_match = re.search(r'class\s*(\d+)', class_dir, re.IGNORECASE)
        if not grade_match:
            logger.warning(f"Could not extract grade from directory name: {class_dir}")
            continue
            
        grade = grade_match.group(1)
        
        for filename in os.listdir(class_path):
            if not filename.lower().endswith('.pdf'):
                continue
                
            pdf_path = os.path.join(class_path, filename)
            
            subject = os.path.splitext(filename)[0].lower()
            
            try:
                logger.info(f"Processing {pdf_path}")
                pipeline.process_document(pdf_path, grade, subject)
            except Exception as e:
                logger.error(f"Failed to process {pdf_path}: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    
    pass
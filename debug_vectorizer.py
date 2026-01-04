import logging
from simple_rag import get_simple_rag_pipeline
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

logging.basicConfig(level=logging.DEBUG)

def debug_vectorizer():
    print("Debugging TF-IDF Vectorizer...")
    
    rag_pipeline = get_simple_rag_pipeline({
        'CHUNKS_PATH': './chunks',
        'TOP_K_RESULTS': 5,
        'CONFIDENCE_THRESHOLD': 0.1
    })
    
    grade_key = "class 5"
    if grade_key in rag_pipeline.grade_data:
        grade_data = rag_pipeline.grade_data[grade_key]
        print(f"Grade 5 data:")
        print(f"  Number of chunks: {len(grade_data['chunks'])}")
        print(f"  TF-IDF matrix shape: {grade_data['tfidf_matrix'].shape}")
        
        sample_text = grade_data['chunk_texts'][0]
        print(f"\nSample chunk text: {sample_text[:100]}...")
        
        try:
            sample_vector = rag_pipeline.vectorizer.transform([sample_text])
            print(f"Sample text vector shape: {sample_vector.shape}")
            
            similarity = np.dot(sample_vector, grade_data['tfidf_matrix'][0].T)[0, 0]
            print(f"Similarity with itself: {similarity}")
            
            vocab_size = len(rag_pipeline.vectorizer.vocabulary_)
            print(f"Vectorizer vocabulary size: {vocab_size}")
            
            if vocab_size == 0:
                print("Vectorizer has no vocabulary!")
                
        except Exception as e:
            print(f"Error during vectorization: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"Grade {grade_key} not found in data")

if __name__ == "__main__":
    debug_vectorizer()
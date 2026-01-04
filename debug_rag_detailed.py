import logging
from simple_rag import get_simple_rag_pipeline
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

logging.basicConfig(level=logging.DEBUG)

def debug_rag_detailed():
    print("Detailed debugging of Simple RAG Pipeline...")
    
    rag_pipeline = get_simple_rag_pipeline({
        'CHUNKS_PATH': './chunks',
        'TOP_K_RESULTS': 5,
        'CONFIDENCE_THRESHOLD': 0.1
    })
    
    print(f"Loaded data for grades: {list(rag_pipeline.grade_data.keys())}")
    
    grade_key = "class 5"
    if grade_key in rag_pipeline.grade_data:
        grade_data = rag_pipeline.grade_data[grade_key]
        print(f"\nGrade 5 data:")
        print(f"  Number of chunks: {len(grade_data['chunks'])}")
        print(f"  TF-IDF matrix shape: {grade_data['tfidf_matrix'].shape}")
        
        question = "What is We the Travellers about?"
        print(f"\nTesting question: {question}")
        
        try:
            question_vector = rag_pipeline.vectorizer.transform([question])
            print(f"Question vector shape: {question_vector.shape}")
            
            similarities = cosine_similarity(question_vector, grade_data['tfidf_matrix']).flatten()
            print(f"Similarities array shape: {similarities.shape}")
            print(f"Max similarity: {np.max(similarities)}")
            print(f"Min similarity: {np.min(similarities)}")
            print(f"Mean similarity: {np.mean(similarities)}")
            
            top_indices = np.argsort(similarities)[::-1][:5]
            print(f"Top 5 indices: {top_indices}")
            print(f"Top 5 similarities: {similarities[top_indices]}")
            
            relevant_indices = [i for i in top_indices if similarities[i] >= 0.1]
            print(f"Indices above threshold (0.1): {relevant_indices}")
            
        except Exception as e:
            print(f"Error during vectorization: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"Grade {grade_key} not found in data")

if __name__ == "__main__":
    debug_rag_detailed()
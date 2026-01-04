import logging
from simple_rag import get_simple_rag_pipeline
import numpy as np

logging.basicConfig(level=logging.DEBUG)

def debug_tfidf_matrix():
    print("Debugging TF-IDF Matrix...")
    
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
        print(f"  TF-IDF matrix type: {type(grade_data['tfidf_matrix'])}")
        
        sample_row = grade_data['tfidf_matrix'][0]
        print(f"\nSample row type: {type(sample_row)}")
        print(f"Sample row shape: {sample_row.shape}")
        
        try:
            dense_sample = sample_row.toarray()
            print(f"Dense sample shape: {dense_sample.shape}")
            print(f"Non-zero elements in sample: {np.count_nonzero(dense_sample)}")
            print(f"Max value in sample: {np.max(dense_sample)}")
            print(f"Min value in sample: {np.min(dense_sample)}")
        except Exception as e:
            print(f"Error converting to dense: {e}")
            
        sample_row_2 = grade_data['tfidf_matrix'][1]
        try:
            dense_sample_2 = sample_row_2.toarray()
            print(f"\nSecond sample non-zero elements: {np.count_nonzero(dense_sample_2)}")
        except Exception as e:
            print(f"Error converting second sample: {e}")
            
    else:
        print(f"Grade {grade_key} not found in data")

if __name__ == "__main__":
    debug_tfidf_matrix()
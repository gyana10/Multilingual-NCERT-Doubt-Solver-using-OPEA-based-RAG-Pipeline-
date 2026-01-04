import logging
from simple_rag import get_simple_rag_pipeline

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def debug_rag_pipeline():
    print("Debugging Simple RAG Pipeline...")
    
    rag_pipeline = get_simple_rag_pipeline({
        'CHUNKS_PATH': './chunks',
        'TOP_K_RESULTS': 5,
        'CONFIDENCE_THRESHOLD': 0.1
    })
    
    print(f"Loaded data for grades: {list(rag_pipeline.grade_data.keys())}")
    
    print("\nTesting with grade=7 (integer)...")
    result = rag_pipeline.query(
        question="What is photosynthesis?",
        grade=7,
        subject="Science",
        language="English"
    )
    
    print("Answer:", result['answer'][:100] + "...")
    print("Confidence:", result['confidence'])
    
    print("\nTesting with grade=8 (different integer)...")
    result = rag_pipeline.query(
        question="What is photosynthesis?",
        grade=8,
        subject="Science",
        language="English"
    )
    
    print("Answer:", result['answer'][:100] + "...")
    print("Confidence:", result['confidence'])

if __name__ == "__main__":
    debug_rag_pipeline()
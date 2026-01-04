import json

def read_chunks():
    print("Reading sample chunks from class 5...")
    
    with open('chunks/class 5_chunks.jsonl', 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 3:  # Read only first 3 lines
                break
            chunk = json.loads(line.strip())
            print(f"\nChunk {i+1}:")
            print(f"  ID: {chunk.get('id', 'N/A')}")
            print(f"  Text: {chunk.get('text', 'N/A')[:200]}...")
            print(f"  Metadata: {chunk.get('metadata', 'N/A')}")

if __name__ == "__main__":
    read_chunks()
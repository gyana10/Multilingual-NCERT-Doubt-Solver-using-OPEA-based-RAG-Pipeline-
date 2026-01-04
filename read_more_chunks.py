import json

def read_chunks():
    print("Reading more sample chunks from class 5...")
    
    with open('chunks/class 5_chunks.jsonl', 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i < 3:  # Skip first 3 lines
                continue
            if i >= 10:  # Read only up to line 10
                break
            chunk = json.loads(line.strip())
            print(f"\nChunk {i+1}:")
            print(f"  ID: {chunk.get('id', 'N/A')}")
            print(f"  Text: {chunk.get('text', 'N/A')[:200]}...")
            if i >= 15:  # Stop after 15 lines
                break

if __name__ == "__main__":
    read_chunks()
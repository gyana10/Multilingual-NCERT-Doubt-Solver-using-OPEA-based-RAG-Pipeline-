import json

def check_chunks():
    print("Checking chunks in class 5...")
    
    math_count = 0
    total_count = 0
    
    with open('chunks/class 5_chunks.jsonl', 'r', encoding='utf-8') as f:
        for line in f:
            total_count += 1
            chunk = json.loads(line.strip())
            if 'math' in chunk.get('id', '').lower():
                math_count += 1
    
    print(f"Total chunks: {total_count}")
    print(f"Math chunks: {math_count}")
    
    print("\nSample math chunks:")
    with open('chunks/class 5_chunks.jsonl', 'r', encoding='utf-8') as f:
        count = 0
        for line in f:
            chunk = json.loads(line.strip())
            if 'math' in chunk.get('id', '').lower():
                print(f"  ID: {chunk.get('id', 'N/A')}")
                print(f"  Text: {chunk.get('text', 'N/A')[:100]}...")
                count += 1
                if count >= 3:
                    break

if __name__ == "__main__":
    check_chunks()
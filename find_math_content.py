import json

def find_math_content():
    print("Looking for math content in class 5 chunks...")
    
    with open('chunks/class 5_chunks.jsonl', 'r', encoding='utf-8') as f:
        count = 0
        for i, line in enumerate(f):
            chunk = json.loads(line.strip())
            if 'math' in chunk.get('id', '').lower():
                text = chunk.get('text', '')
                if any(term in text.lower() for term in ['fraction', 'number', 'add', 'subtract', 'multiply', 'divide']):
                    print(f"\nChunk {i+1}:")
                    print(f"  ID: {chunk.get('id', 'N/A')}")
                    print(f"  Text: {text[:200]}...")
                    count += 1
                    if count >= 5:
                        break

if __name__ == "__main__":
    find_math_content()
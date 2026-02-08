from text_utils import chunk_text_meaningfully, save_extracted_text_to_json
import os

def test_utils():
    # 1. Test Chunking
    text = "This is a sentence. " * 20 # 4 words * 20 = 80 words.
    text += "Another sentence. " * 30 # 2 words * 30 = 60 words. Total 140 words.
    # This should barely fit in one chunk or split if strict.
    
    chunks = chunk_text_meaningfully(text, min_words=100, max_words=150)
    print(f"Text length: {len(text.split())} words")
    print(f"Number of chunks: {len(chunks)}")
    for i, c in enumerate(chunks):
        print(f"Chunk {i+1} words: {len(c.split())}")
        
    # Test 2: Large text
    long_text = "Word " * 400
    chunks_long = chunk_text_meaningfully(long_text, min_words=100, max_words=150)
    print(f"\nLong text chunks: {len(chunks_long)}")
    
    # 2. Test JSON Save
    saved = save_extracted_text_to_json(text, "test_output.json")
    print(f"\nJSON Saved: {saved}")
    if os.path.exists("test_output.json"):
        print("File exists.")
        os.remove("test_output.json")
    else:
        print("File not found.")

if __name__ == "__main__":
    test_utils()

import json
import os
import re

def save_extracted_text_to_json(text, filename="temp_ocr_data.json"):
    """
    Saves the extracted text to a JSON file.
    
    Args:
        text (str): The text to save.
        filename (str): The name of the file to save to.
    """
    data = {"extracted_text": text}
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving to JSON: {e}")
        return False

def chunk_text_meaningfully(text, min_words=100, max_words=150):
    """
    Chunks text into meaningful segments based on word count, preserving line breaks.
    
    Args:
        text (str): The input text.
        min_words (int): Minimum words per chunk (soft target).
        max_words (int): Target maximum words per chunk.
        
    Returns:
        list: A list of text chunks.
    """
    if not text:
        return []
        
    # Split text into lines to preserve original structure/alignment
    lines = text.splitlines()
    
    chunks = []
    current_chunk = []
    current_word_count = 0
    
    for line in lines:
        # Preserve empty lines as structural spacers within a chunk if possible,
        # or they just get added.
        word_count = len(line.split())
        
        # If adding this line exceeds the max limit:
        # 1. Close current chunk (if it has content).
        # 2. Start new chunk with this line.
        if current_chunk and (current_word_count + word_count > max_words):
             chunks.append("\n".join(current_chunk))
             current_chunk = [line]
             current_word_count = word_count
        else:
             # Add line to current chunk
             current_chunk.append(line)
             current_word_count += word_count
            
    # Add any remaining text
    if current_chunk:
        chunks.append("\n".join(current_chunk))
        
    return chunks

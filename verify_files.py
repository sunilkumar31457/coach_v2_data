import os
import io
import fitz # PyMuPDF
from PIL import Image

def test_file_handling():
    print("--- Testing Imports ---")
    try:
        import fitz
        print("✅ PyMuPDF (fitz) imported successfully")
    except ImportError:
        print("❌ PyMuPDF not found")
        
    print("\n--- Testing Image Encoding Fix ---")
    # Simulate 'P' mode image
    img = Image.new('P', (100, 100), color=255)
    print(f"Created Test Image Mode: {img.mode}")
    
    try:
        # Simulate the logic in code
        if img.mode != 'RGB':
            img = img.convert('RGB')
            print("✅ Converted to RGB")
        
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        print("✅ Saved as JPEG successfully")
    except Exception as e:
        print(f"❌ Failed to save image: {e}")

if __name__ == "__main__":
    test_file_handling()

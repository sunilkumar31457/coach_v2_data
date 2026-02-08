from text_utils import chunk_text_meaningfully

def test_chunking_strict():
    # User's provided text
    user_text = "Explain in detail various image filtering techniques and their importance in digital image analysis. Apply appropriate alignment strategies (global or pairwise) to solve misalignment issues in an image stitching scenario. Apply the illumination–reflectance model to interpret brightness and contrast variations in real images. Demonstrate how radiometric normalization can be applied to achieve consistent intensity levels for accurate image alignment. Compare handcrafted segmentation models and learning-based approaches in medical image analysis and autonomous driving. Illustrate how image patches are processed through a Vision Transformer and apply this process to an image classification example such as classifying an image as a cat or a dog. Demonstrate how reflectance models can be applied to examine surface reflectivity and illumination effects in an image. Apply intensity and color normalization methods to improve the robustness of feature matching in multi-image alignment."
    
    print(f"Original User Text Word Count: {len(user_text.split())}")
    
    chunks = chunk_text_meaningfully(user_text, min_words=100, max_words=150)
    
    print(f"Number of chunks: {len(chunks)}")
    for i, c in enumerate(chunks):
        count = len(c.split())
        print(f"Chunk {i+1} Length: {count} words")
        print(f"--- Chunk Start ---\n{c[:50]}...\n--- Chunk End ---")
        if count > 150:
            print("❌ FAIL: Exceeds 150 words!")
        else:
            print("✅ PASS: Within limit.")

if __name__ == "__main__":
    test_chunking_strict()

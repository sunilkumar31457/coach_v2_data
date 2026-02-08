
import os
import sys
from groq import Groq
from dotenv import load_dotenv

# Redirect output to a file
sys.stdout = open("available_models.txt", "w")

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("Error: GROQ_API_KEY not found.")
else:
    try:
        client = Groq(api_key=api_key)
        models = client.models.list()
        print("Available Models:")
        for model in models.data:
            print(f"- {model.id}")
    except Exception as e:
        print(f"Error fetching models: {e}")

sys.stdout.close()

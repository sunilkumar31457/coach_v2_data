
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("GROQ_API_KEY not found in environment variables.")
else:
    try:
        client = Groq(api_key=api_key)
        models = client.models.list()
        print("Available Models:")
        for model in models.data:
            print(f"- {model.id}")
    except Exception as e:
        print(f"Error listing models: {e}")

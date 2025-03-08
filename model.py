import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

api_key = os.getenv("GROQ_API_KEY")
print(f"GROQ_API_KEY: {api_key}")  # Debugging output

if not api_key:
    raise ValueError("❌ API Key is missing! Set GROQ_API_KEY in your environment or .env file.")

from groq import Groq
client = Groq(api_key=api_key)
models = client.models.list()
print(models)


import os
from dotenv import load_dotenv

# Load environment variables from .env once, globally
load_dotenv()

# Access your OpenAI key safely
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the .env file or environment.")
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)
def ask_gemini(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="You are a sophisticated finance application and will answer this question: " + prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
        ),
    )
    return response.text
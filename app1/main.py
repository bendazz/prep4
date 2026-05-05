from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI 
import os
from dotenv import load_dotenv
from google import genai 
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-flash-lite-latest"

CATEGORIES = ["positive", "negative", "neutral"]

SYSTEM_PROMPT = """You are a sentiment classifier.
Read the user's text and reply with EXACTLY one word from this list:
positive, negative, neutral.
No punctuation, no explanation, just the single word."""


app = FastAPI()

@app.get("/categories")
def get_categories():
    return {"categories": CATEGORIES}

@app.get("/classify")
def classify(text: str):
    response = client.models.generate_content(
        model=MODEL,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        contents=text,
    )
    return response.text

app.mount("/", StaticFiles(directory="static", html=True), name="static")
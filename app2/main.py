from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-flash-lite-latest"

SECRET = 42

def secret_number():
    return {"number": SECRET}

TOOL = types.Tool(function_declarations=[
    types.FunctionDeclaration(
        name="secret_number",
        description="Returns the secret number known only to this server.",
    ),
])

app = FastAPI()

@app.get("/ask_without")
def get_ask_without(text: str):
    response = client.models.generate_content(model=MODEL, contents=text)
    return response.text

@app.get("/ask_with")
def get_ask_with(text: str):
    # Step 1: ask the model, telling it the tool exists.
    response = client.models.generate_content(
        model=MODEL,
        config=types.GenerateContentConfig(tools=[TOOL]),
        contents=text,
    )
    
    
    
    call = response.candidates[0].content.parts[0].function_call
    if not call:
         return response.text

    # Step 3: run the function ourselves.
    result = secret_number()

    # Step 4: tell the model the answer in plain words and let it phrase the reply.
    follow_up = client.models.generate_content(
        model=MODEL,
        contents=f"The user asked: {text}\nThe answer from the function is: {result}",
    )
    return follow_up.text

app.mount("/", StaticFiles(directory="static", html=True), name="static")
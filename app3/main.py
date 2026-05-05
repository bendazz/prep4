from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
import os
import random
import threading
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-flash-lite-latest"

# The finite set of allowed positions: a 5x5 grid.
POSITIONS = [(x, y) for x in range(1, 6) for y in range(1, 6)]

# The current location of the point. Updated by a background thread.
current_position = random.choice(POSITIONS)

def move_point():
    global current_position
    while True:
        time.sleep(5)
        current_position = random.choice(POSITIONS)

threading.Thread(target=move_point, daemon=True).start()

def get_position():
    return {"x": current_position[0], "y": current_position[1]}

TOOL = types.Tool(function_declarations=[
    types.FunctionDeclaration(
        name="get_position",
        description="Returns the current x, y coordinates of the moving point on the server.",
    ),
])

app = FastAPI()

@app.get("/positions")
def positions():
    return {"positions": [{"x": x, "y": y} for x, y in POSITIONS]}

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

    # Step 2: did the model decide to call our function?
    call = response.candidates[0].content.parts[0].function_call
    if not call:
        return response.text

    # Step 3: run the function ourselves and return the result.
    return get_position()

app.mount("/", StaticFiles(directory="static", html=True), name="static")

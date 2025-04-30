import os
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import numpy as np
import io
import random

app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dummy class names and fun facts
ANIMALS = [
    ("cat", "Cats have five toes on their front paws, but only four on the back!"),
    ("dog", "Dogs' noses are wet to help absorb scent chemicals."),
    ("elephant", "Elephants are the only mammals that can't jump."),
    ("lion", "A lion's roar can be heard from 5 miles away."),
    ("turtle", "Some turtles can breathe through their butts!"),
]
SHAPES = [
    ("circle", "The circle is the shape with the smallest perimeter for a given area."),
    ("triangle", "Triangles are the strongest shape in engineering."),
    ("square", "A square has four equal sides and four right angles."),
    ("star", "Stars are often used to symbolize excellence."),
]
ALL_CLASSES = ANIMALS + SHAPES

def dummy_predict(image: Image.Image):
    # Randomly select a class and confidence for demo
    cls, fact = random.choice(ALL_CLASSES)
    confidence = round(random.uniform(0.7, 0.99), 2)
    return cls, confidence, fact

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read()))
    cls, confidence, fact = dummy_predict(image)
    return JSONResponse(content={
        "class": cls,
        "confidence": confidence,
        "fact": fact
    })

@app.get("/")
async def root():
    return {"message": "Welcome to WildShapes! Upload an image to classify animals and shapes."}

if __name__ == "__main__":
    import uvicorn
    import threading, webbrowser
    def open_browser():
        url = "http://localhost:3000"
        threading.Timer(1.5, lambda: webbrowser.open(url)).start()
    open_browser()
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

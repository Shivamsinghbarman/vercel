from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json
from typing import List  # Import List from typing

# Load data from the q-vercel-python.json file
with open('q-vercel-python.json', 'r') as file:
    data = json.load(file)

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/api")
async def get_marks(name: List[str]=Query(...)):  # Accept 'name' as a list of strings
    marks = []
    name_set = set(name)  # Use set for faster lookup
    for student in data:
        if student["name"] in name_set:
            marks.append(student["marks"])

    # If no marks were found, return a 404 error with a message
    if not marks:
        raise HTTPException(status_code=404, detail="Names not found")

    # Return the JSON response
    return JSONResponse(content={"marks": marks})

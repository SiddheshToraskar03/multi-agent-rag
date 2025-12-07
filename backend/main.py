# backend/main.py
import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from backend.pipeline import RagPipeline

env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

if not os.getenv("GEMINI_API_KEY"):
    raise ValueError(
        "GEMINI_API_KEY is not set. "
        "Please create a .env file in the project root with: GEMINI_API_KEY=your-api-key"
    )

app = FastAPI(title="Multi-Agent RAG over Postgres")
pipeline = RagPipeline()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    question: str


@app.post("/ask")
def ask(req: AskRequest):
    result = pipeline.ask(req.question)
    return result

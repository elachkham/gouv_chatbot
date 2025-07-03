from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

from rag_pipeline import ask_gemini_rag

app = FastAPI()

# Autoriser React en développement (port 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Requête utilisateur
class Question(BaseModel):
    query: str

@app.post("/ask")
def ask(question: Question):
    response = ask_gemini_rag(question.query)
    return {"answer": response}

# 📁 Localisation réelle du dossier build de React
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_BUILD_DIR = os.path.join(BASE_DIR, "frontend", "build")

# Monter le dossier static de React
STATIC_DIR = os.path.join(FRONTEND_BUILD_DIR, "static")
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Servir index.html pour la racine
@app.get("/")
def serve_frontend():
    index_path = os.path.join(FRONTEND_BUILD_DIR, "index.html")
    return FileResponse(index_path)

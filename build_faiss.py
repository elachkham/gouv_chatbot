import os
from app.embedding_utils import embed_texts, save_faiss_index

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT_PATH = os.path.join(BASE_DIR, "chatbot-rag/data", "code_travail.txt")

with open(TEXT_PATH, "r", encoding="utf-8") as f:
    lines = f.read().split("\n")

texts = [line.strip() for line in lines if len(line.strip()) > 20]

embeddings = embed_texts(texts)
save_faiss_index(embeddings, texts)

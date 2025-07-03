import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_DIR = os.path.join(BASE_DIR, "chatbot-rag/vector_store", "faiss_index")

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

def embed_texts(texts):
    return model.encode(texts, convert_to_numpy=True)

def save_faiss_index(embeddings, texts):
    os.makedirs(INDEX_DIR, exist_ok=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, os.path.join(INDEX_DIR, "index.faiss"))
    with open(os.path.join(INDEX_DIR, "texts.pkl"), "wb") as f:
        pickle.dump(texts, f)
    print(" Index FAISS sauvegardé")

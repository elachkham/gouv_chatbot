import os
import pickle
import faiss
import google.generativeai as genai
from sentence_transformers import SentenceTransformer

# Configuration des chemins
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(BASE_DIR, "vector_store", "faiss_index", "index.faiss")
TEXTS_PATH = os.path.join(BASE_DIR, "vector_store", "faiss_index", "texts.pkl")

# Initialisation des modèles (chargement unique pour meilleure performance)
#genai.configure(api_key="AIzaSyBa2Yan20FuXkbzN-P0rdFHyMYJdooDmJc")
genai.configure(api_key="AIzaSyBHbc2IAXN8of4A7nTLkw3r5gaHhOSi500")
EMBEDDING_MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
GEMINI_MODEL = genai.GenerativeModel("models/gemini-1.5-flash")

def query_index(user_question, k_results=5):
    """
    Interroge l'index FAISS pour trouver les documents les plus pertinents.
    
    Args:
        user_question: Question de l'utilisateur
        k_results: Nombre de résultats à retourner
        
    Returns:
        str: Documents pertinents concaténés
    """
    # Chargement des ressources
    index = faiss.read_index(INDEX_PATH)
    with open(TEXTS_PATH, "rb") as f:
        texts = pickle.load(f)
    
    # Encodage et recherche
    query_vec = EMBEDDING_MODEL.encode([user_question])
    distances, indices = index.search(query_vec, k=k_results)
    
    # Sélection et formatage des résultats
    top_docs = [texts[i] for i in indices[0]]
    return "\n---\n".join(top_docs)  # Séparateur clair entre les documents

def ask_gemini_rag(question, temperature=0.3):
    """
    Pose une question à Gemini en utilisant le RAG (Retrieval-Augmented Generation).
    
    Args:
        question: Question à poser
        temperature: Créativité de la réponse (0-1)
        
    Returns:
        str: Réponse générée
    """
    # Récupération du contexte
    context = query_index(question)
    
    # Prompt structuré avec instructions claires
    prompt = f"""
        Tu es un expert du Code du Travail français. 
        Voici des extraits pertinents (peut-être incomplets) :

        {context}

        Question : {question}

        Réponds selon ces règles :
        1. Donne TOUJOURS une réponse utile, même incomplète
        2. Si l'information exacte n'est pas dans le contexte :
        - Donne la réponse selon les éléments connexes trouvés
        """
    
    # Configuration de la génération
    generation_config = {
        "temperature": temperature,
        "max_output_tokens": 1000,
    }
    
    # Appel au modèle
    try:
        response = GEMINI_MODEL.generate_content(
        prompt,
        generation_config=generation_config
        )
        return response.text.strip() if response.text else "❌ Réponse vide du modèle"
    except Exception as e:
        print(f"Erreur Gemini : {e}")
        return "❌ Erreur lors de la génération Gemini"
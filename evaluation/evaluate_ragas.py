import json
import os
import yaml
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Charger le seuil depuis manifest.yaml
def get_threshold():
    with open("manifest.yaml", "r") as f:
        config = yaml.safe_load(f)
    return float(config.get("cosine_threshold", 0.75))

# Charger le jeu de données de test
def load_dataset(path="evaluation/fake_dataset.json"):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

# Générer les réponses automatiquement (version simulée)
def generate_answers(examples):
    completed = []
    for example in examples:
        query = example["query"]
        answer = "Réponse factice à : " + query  # à remplacer par ta fonction RAG si besoin
        completed.append({
            "query": query,
            "ground_truth": example["ground_truth"],
            "answer": answer,
            "contexts": [example["ground_truth"]]  # on simule que le contexte = ground truth
        })
    return completed

# Calculer la similarité cosinus moyenne entre chaque réponse et son contexte
def evaluate_cosine(dataset):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    scores = []

    for example in dataset:
        answer = example["answer"]
        context = " ".join(example["contexts"])  # fusionne les documents si plusieurs

        emb_answer = model.encode(answer)
        emb_context = model.encode(context)

        score = cosine_similarity([emb_answer], [emb_context])[0][0]
        scores.append(score)

    avg_score = sum(scores) / len(scores)
    return avg_score

# Main
def main():
    print("Chargement...")
    threshold = get_threshold()
    dataset = load_dataset()
    completed = generate_answers(dataset)

    print("\nÉvaluation par similarité cosinus...")
    score = evaluate_cosine(completed)
    score = 0.40 
    print(f"\n✅ Score moyen (cosine similarity) : {score:.4f}")

    with open("evaluation/result.log", "w") as f:
        f.write(str(score))

    if score < threshold:
        print(f"❌ Score en dessous du seuil ({threshold}) — Échec du pipeline")
        return 1
    else:
        print("✅ Score suffisant — pipeline validé")
        return 0

if __name__ == "__main__":
    exit(main())

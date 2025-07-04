"""
evaluate_ragas.py - Version qui force l'échec
Remplace complètement ton fichier evaluate_ragas.py pour forcer l'échec
"""

import json
import os
import yaml

def main():
    print("🔴 Test d'ÉCHEC FORCÉ")
    print("=" * 50)
    
    # Créer le dossier d'évaluation
    os.makedirs("evaluation", exist_ok=True)
    
    # FORCER L'ÉCHEC : Score très bas
    score = 0.25  # Score intentionnellement très bas
    threshold = 0.70  # Seuil normal
    
    print(f"📊 Score forcé : {score:.4f}")
    print(f"🎯 Seuil : {threshold}")
    print(f"❌ Résultat : {score} < {threshold} = ÉCHEC")
    
    # Sauvegarder le résultat
    with open("evaluation/result.log", "w") as f:
        f.write(f"{score:.4f}\n")
        f.write(f"Seuil: {threshold}\n")
        f.write(f"Status: FAIL\n")
        f.write(f"Test: FORCED FAILURE\n")
    
    print("💾 Résultat sauvegardé dans evaluation/result.log")
    
    # FORCER L'ÉCHEC DU PIPELINE
    if score < threshold:
        print(f"❌ ÉCHEC FORCÉ - Score {score:.4f} < Seuil {threshold}")
        print("🚨 Le pipeline DOIT échouer maintenant")
        return 1  # Code d'erreur pour faire échouer le pipeline
    else:
        print("✅ Score suffisant")
        return 0

if __name__ == "__main__":
    exit(main())

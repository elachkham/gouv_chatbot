import os
import requests
import fitz  # PyMuPDF

def download_code_du_travail():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(BASE_DIR, "chatbot-rag/data")
    os.makedirs(data_dir, exist_ok=True)

    pdf_path = os.path.join(data_dir, "LEGITEXT000006072050.pdf")
    txt_path = os.path.join(data_dir, "code_travail.txt")
    # Convertir le PDF en texte
    with fitz.open(pdf_path) as doc:
        with open(txt_path, "w", encoding="utf-8") as f:
            for page in doc:
                text = page.get_text()
                f.write(text)
                f.write("\n")

    print(f"PDF converti en texte : {txt_path}")

# Dockerfile Multi-Stage - PERMISSIONS CORRIGÉES

# ==============================================
# STAGE 1: Build Frontend React
# ==============================================
FROM node:18-alpine AS frontend-builder

WORKDIR /frontend

# Si vous avez déjà un frontend
COPY frontend/ ./

# Si package.json existe, build React
RUN if [ -f package.json ]; then \
        npm install && npm run build; \
    else \
        # Créer un frontend minimal si absent
        mkdir -p build && \
        echo '<!DOCTYPE html><html><head><title>Chatbot</title></head><body><h1>Chatbot Code du Travail</h1><div id="app">Interface disponible via API</div></body></html>' > build/index.html; \
    fi

# ==============================================
# STAGE 2: Backend Python Production
# ==============================================
FROM python:3.10-slim AS production

# Variables d'environnement optimisées
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app:/app/app

# 🔧 CORRECTION: Variables d'environnement pour les caches
ENV TRANSFORMERS_CACHE=/app/.cache/transformers
ENV HUGGINGFACE_HUB_CACHE=/app/.cache/huggingface
ENV SENTENCE_TRANSFORMERS_HOME=/app/.cache/sentence-transformers

# Métadonnées
LABEL maintainer="votre-email@example.com"
LABEL description="Chatbot RAG Code du Travail - Production Ready"

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 🔧 CORRECTION: Créer utilisateur ET dossiers de cache AVANT l'installation
RUN groupadd -r appuser && useradd -r -g appuser -m appuser

# 🔧 CORRECTION: Créer les dossiers de cache avec bonnes permissions
RUN mkdir -p /app/.cache/transformers \
    /app/.cache/huggingface \
    /app/.cache/sentence-transformers \
    /app/vector_store/faiss_index \
    && chown -R appuser:appuser /app

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier TOUT votre code existant
COPY . .

# Corrections automatiques sans modifier votre code source
RUN touch app/__init__.py

# Copier le build frontend
COPY --from=frontend-builder /frontend/build ./frontend/build

# 🔧 CORRECTION: Donner les permissions APRÈS avoir copié tous les fichiers
RUN chown -R appuser:appuser /app

# Nettoyer les outils de build
RUN apt-get remove -y gcc g++ && apt-get autoremove -y

# 🔧 CORRECTION: Passer à l'utilisateur non-root APRÈS avoir configuré les permissions
USER appuser

# Exposer le port
EXPOSE 8000

# Health check robuste
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1

# Commande de démarrage production
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
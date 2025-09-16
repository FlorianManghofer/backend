# Basis-Image mit Python 3.12, schlankes Debian
FROM python:3.12-slim AS runtime

# Schnellere/saubere Logs, keine .pyc-Dateien
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Arbeitsverzeichnis im Container
WORKDIR /app

# (Optional) System-Pakete – hier leer gehalten
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Zuerst nur die Prod-Requirements kopieren (bessere Layer-Caches)
COPY requirements-prod.txt .
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements-prod.txt

# Jetzt den eigentlichen App-Code
COPY app ./app

# Non-root-User für mehr Sicherheit
RUN useradd -m appuser
USER appuser

# Der Port, an dem die App innerhalb des Containers lauscht
EXPOSE 8000

# Start-Kommando: Gunicorn mit Uvicorn-Worker
CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "--access-logfile", "-", "--error-logfile", "-"]

# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings

app = FastAPI(title=settings.APP_NAME)

allow_origins = settings.CORS_ORIGINS
if settings.ENVIRONMENT != "production" and not allow_origins:
    # in Dev alles erlauben, wenn nichts gesetzt
    allow_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

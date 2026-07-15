from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router
from .pdf_routes import router as pdf_router

app = FastAPI(title="Jarvis AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://jarvis-frontend-dun.vercel.app",
        "https://jarvis-frontend-jifz8vo3e-pratik1509.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(pdf_router)

@app.get("/")
def home():
    return {"message": "Jarvis AI Backend is Running 🚀"}
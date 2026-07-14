from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router
from .pdf_routes import router as pdf_router


app = FastAPI(
    title="Jarvis AI API"
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
   allow_origins=[
    "http://localhost:5173",
    "https://jarvis-frontend-pratik1509.vercel.app",
    "https://jarvis-frontend-git-main-pratik1509.vercel.app"
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes
app.include_router(router)
app.include_router(pdf_router)


@app.get("/")
def home():
    return {
        "message": "Jarvis AI Backend is Running 🚀"
    }
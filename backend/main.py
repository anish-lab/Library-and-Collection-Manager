import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, collections, assets, tags
from app.core.database import engine
from app.models.base import Base

# Ensure uploads directory exists
os.makedirs("uploads", exist_ok=True)

app = FastAPI(title="Library & Collections Manager API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for uploads
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include Routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(collections.router, prefix="/api/collections", tags=["Collections"])
app.include_router(assets.router, prefix="/api/assets", tags=["Assets"])
app.include_router(tags.router, prefix="/api/tags", tags=["Tags"])

@app.get("/")
def root():
    return {"message": "Welcome to the Library & Collections Manager API"}
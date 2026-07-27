from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.api import api_router
from app.core.config import settings
from app.database.session import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler to perform startup folder creation and DB migration."""
    # Ensure local folders exist
    Path(settings.MODEL_DIR).mkdir(parents=True, exist_ok=True)
    Path(settings.OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    Path(settings.TEMP_DIR).mkdir(parents=True, exist_ok=True)
    
    # Create SQLite database tables
    Base.metadata.create_all(bind=engine)
    
    yield
    
    # Optional cleanup on shutdown can go here
    pass

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Jupiter Sonic - Open-Source Fully Local Speech Intelligence Platform",
    version="0.1.0",
    lifespan=lifespan
)

# CORS Configuration
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Serve static audio/video output directories for UI rendering
# Ensure static directory exists before mounting to avoid startup crash
static_dir = Path("static")
static_dir.mkdir(parents=True, exist_ok=True)
Path(settings.OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Mount primary API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    """Root health check index."""
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "docs_url": "/docs",
        "local_inference_only": True
    }

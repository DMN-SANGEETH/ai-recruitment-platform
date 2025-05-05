# main.py (FastAPI backend)
import sys
from pathlib import Path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.utils.config import Settings


from app.api.v1.router import router as api_router

def create_application() -> FastAPI:
    app = FastAPI(
        title="Resume Matcher API",
        description="API for uploading resumes and finding matching jobs",
        version="1.0.0"
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=Settings.get_allowed_hosts(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(api_router, prefix="/api/v1")

    return app

app = create_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # FastAPI runs on port 8000
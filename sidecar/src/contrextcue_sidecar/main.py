from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contrextcue_sidecar.routers import rewrite, transcribe, settings, status

app = FastAPI(
    title="ContrextCue Sidecar API",
    version="0.1.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)

# CORS so your Tauri frontend (or localhost:3000) can hit it in dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "tauri://localhost",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rewrite.router, prefix="/api/v1/rewrite", tags=["rewrite"])
app.include_router(transcribe.router, prefix="/api/v1/transcribe", tags=["transcribe"])
app.include_router(settings.router, prefix="/api/v1/settings", tags=["settings"])
app.include_router(status.router, prefix="/api/v1/status", tags=["status"])


def start():
    import uvicorn
    uvicorn.run(
        "contrextcue_sidecar.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

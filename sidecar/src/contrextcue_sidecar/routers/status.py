from fastapi import APIRouter
from contrextcue_sidecar.schemas.status import StatusResponse

router = APIRouter()

@router.get("/", 
           response_model=StatusResponse,
           summary="Get system health and configuration status",
           description="""
           Retrieves the current status of system components and configuration.
           
           Returns information about:
           - LLM status (model name and whether it's loaded successfully)
           - Speech-to-text engine status (engine name and model)
           - Current keyboard shortcut configuration
           - Warm-up status for performance optimization
           
           This endpoint is used by the UI to display system status and verify that components are functioning.
           """
)
async def get_status():
    # TODO: hook up real health checks
    return StatusResponse(
        llm={"model": "rene-v0.1-1.3b", "loaded": True},
        stt={"engine": "whisper.cpp", "model": "tiny.en"},
        hotkey="Ctrl+Shift+Enter",
        warmUpEnabled=True
    )

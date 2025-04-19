from fastapi import APIRouter, HTTPException
from contrextcue_sidecar.schemas.transcribe import TranscribeRequest, TranscribeResponse
from contrextcue_sidecar.stt_runner import transcribe
from contrextcue_sidecar.llm_runner import rewrite_text

router = APIRouter()

@router.post("/", 
            response_model=TranscribeResponse,
            summary="Transcribe audio input to text with optional rewrite",
            description="""
            Records audio from the user's microphone and transcribes it to text using the local STT engine.
            
            The workflow involves:
            1. Capturing audio using the system microphone
            2. Processing through whisper.cpp for transcription
            3. Optionally applying an LLM rewrite if a prompt is provided
            4. Returning both the raw transcription and final result
            
            The request includes options for how to process and insert the result (append/replace, clipboard/paste).
            """
)
async def transcribe_endpoint(req: TranscribeRequest):
    try:
        # Continuously transcribed under the hood
        text = transcribe()
        # Apply optional rewrite
        if req.prompt and req.prompt.strip():
            result = rewrite_text(req.prompt, text)
        else:
            result = text
        return TranscribeResponse(transcription=text, result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import APIRouter, HTTPException
from contrextcue_sidecar.schemas.rewrite import RewriteRequest, RewriteResponse
from contrextcue_sidecar.llm_runner import rewrite_text

router = APIRouter()

@router.post("/", 
            response_model=RewriteResponse, 
            summary="Process text input with a specified prompt using the local LLM",
            description="""
            Takes user text input and a prompt template, then processes it with the local LLM.
            
            The endpoint handles:
            - Applying the prompt template to the raw input
            - Processing the combined text through the local LLM (Rene)
            - Returning the LLM's response for insertion at cursor or clipboard
            
            The request includes metadata about how to handle the output (append/replace, clipboard/paste).
            """
)
async def rewrite(req: RewriteRequest):
    try:
        output = rewrite_text(req.prompt, req.input)
        return RewriteResponse(result=output)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

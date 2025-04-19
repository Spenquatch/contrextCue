from pydantic import BaseModel, Field

class LLMInfo(BaseModel):
    model: str = Field(..., description="Name and version of the loaded language model")
    loaded: bool = Field(..., description="Whether the LLM is successfully loaded and ready for inference")

class STTInfo(BaseModel):
    engine: str = Field(..., description="Name of the speech-to-text engine being used (e.g., 'whisper.cpp')")
    model: str = Field(..., description="Name of the specific STT model loaded (e.g., 'tiny.en')")

class StatusResponse(BaseModel):
    llm: LLMInfo = Field(..., description="Status information about the language model")
    stt: STTInfo = Field(..., description="Status information about the speech-to-text engine")
    hotkey: str = Field(..., description="Currently configured submission hotkey combination")
    warmUpEnabled: bool = Field(..., description="Whether the LLM warm-up on startup feature is enabled")

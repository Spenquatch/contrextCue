from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

class Mode(str, Enum):
    append = "append"
    replace = "replace"

class TranscribeRequest(BaseModel):
    trigger: str = Field(..., description="The user-defined trigger name (typically 'talk') that activated speech-to-text recording")
    prompt: Optional[str] = Field("", description="Optional prompt template to apply to the transcribed text for post-processing")
    mode: Mode = Field(..., description="The insertion mode determining how output text should be placed ('append' or 'replace')")
    clipboard: bool = Field(True, description="Whether to copy the resulting transcription to the clipboard")
    autoPaste: bool = Field(True, description="Whether to automatically paste the result at the cursor position")

class TranscribeResponse(BaseModel):
    transcription: str = Field(..., description="The raw transcribed text from the speech-to-text engine")
    result: str = Field(..., description="The final output text, which may be the raw transcription or its rewritten version if a prompt was provided")

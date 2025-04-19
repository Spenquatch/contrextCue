from pydantic import BaseModel, Field
from enum import Enum

class Mode(str, Enum):
    append = "append"
    replace = "replace"

class RewriteRequest(BaseModel):
    trigger: str = Field(..., description="The user-defined trigger name (e.g., 'rewrite', 'email') that activated this request")
    prompt: str = Field(..., description="The prompt template to apply to the input text before sending to the LLM")
    input: str = Field(..., description="The raw text input that needs to be processed by the LLM")
    mode: Mode = Field(..., description="The insertion mode determining how output text should be placed ('append' or 'replace')")
    clipboard: bool = Field(True, description="Whether to copy the result to the clipboard")
    autoPaste: bool = Field(True, description="Whether to automatically paste the result at the cursor position")

class RewriteResponse(BaseModel):
    result: str = Field(..., description="The processed text output from the LLM after applying the prompt to the input")

from pydantic import BaseModel, Field
from typing import Dict, Literal

class Behaviors(BaseModel):
    clipboard: bool = Field(True, description="Global setting to enable/disable copying results to clipboard")
    autoPaste: bool = Field(True, description="Global setting to enable/disable automatic pasting of results at cursor position")
    pasteDelayMs: int = Field(0, description="Delay in milliseconds before auto-pasting, useful for slow or complex editors")

class AdvancedSettings(BaseModel):
    warmUpOnLaunch: bool = Field(True, description="Whether to preload the LLM with a dummy prompt on startup to reduce first-run latency")
    debugLogging: bool = Field(False, description="Enable verbose logging for troubleshooting")

class SettingsRequest(BaseModel):
    prompts: Dict[str, str] = Field(..., description="Mapping of trigger names to their corresponding prompt templates")
    modes: Dict[str, Literal["append", "replace"]] = Field(..., description="Default insertion modes for each trigger or globally")
    behaviors: Behaviors = Field(..., description="Global clipboard and auto-paste behavior settings")
    advanced: AdvancedSettings = Field(..., description="Advanced configuration options including model warm-up and logging")

class SettingsResponse(SettingsRequest):
    """Same fields as SettingsRequest for GET and POST."""
    pass

from fastapi import APIRouter, HTTPException, status
from contrextcue_sidecar.schemas.settings import SettingsRequest, SettingsResponse

router = APIRouter()

# In‑memory placeholder; swap for persistent storage in prod
_current = SettingsResponse(
    prompts={},
    modes={"default": "append"},
    behaviors={},
    advanced={}
)

@router.get("/", 
           response_model=SettingsResponse,
           summary="Retrieve current application settings",
           description="""
           Retrieves the complete current settings configuration from the application state.
           
           Returns all settings categories:
           - Custom prompts and their mapping to triggers
           - Default insertion modes (append/replace)
           - Clipboard and auto-paste behaviors
           - Advanced settings including warm-up and logging options
           
           Used by the settings UI to display current configuration.
           """
)
async def get_settings():
    return _current

@router.post("/", 
            status_code=status.HTTP_204_NO_CONTENT,
            summary="Update application settings",
            description="""
            Updates the application's settings with the provided configuration.
            
            Handles updating all settings categories:
            - Custom trigger-to-prompt mappings
            - Default insertion modes
            - Clipboard and auto-paste behavior settings
            - Advanced settings like model warm-up and debugging options
            
            Returns no content on success; settings are applied immediately.
            """
)
async def update_settings(req: SettingsRequest):
    try:
        # Overwrite all fields
        for field, value in req:
            setattr(_current, field, value)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

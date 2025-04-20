All processing routes are exposed via a local FastAPI server that the Tauri frontend consumes.

You can explore and test them interactively at:
- Swagger UI:  `/api/v1/docs`  
- OpenAPI spec: `/api/v1/openapi.json`  
- ReDoc (optional): `/api/v1/redoc`  

---

### POST /api/v1/rewrite

**Summary:** Rewrite a block of text using a specific prompt.

**Request** (`application/json`):

```json
{
  "trigger": "rewrite",
  "prompt": "Rewrite for clarity and tone:",
  "input": "I want to say this better but don’t know how.",
  "mode": "replace",
  "clipboard": true,
  "autoPaste": true
}
```

**Response** (200 OK):
```json
{
  "result": "I would like to express this more clearly..."
}
```

### POST /api/v1/transcribe
Records a short audio clip and returns its transcription (and optional rewrite).

**Summary:** Transcribe speech in real time, then optionally rewrite it.

**Request** (`application/json`):
```json
{
  "trigger": "talk",
  "prompt": "Rewrite for clarity and tone:",
  "mode": "append",
  "clipboard": true,
  "autoPaste": false
}
```

**Server Flow:**
1. Real‑time streaming transcription via `whisper.cpp`
2. Buffer transcript until user types `/end` + hotkey
3. If a `prompt` is provided, send transcript through `/rewrite`
4. Return both raw `transcription` and final `result`

**Response** (200 OK):
```json
{
  "transcription": "This is what I said.",
  "result": "This is a refined version of what I said."
}
```

### GET /api/v1/status
Returns health and configuration status.

**Summary:** Health and configuration status.

**Response** (200 OK):
```json
{
  "llm": {
    "model": "rene-v0.1-1.3b",
    "loaded": true
  },
  "stt": {
    "engine": "whisper.cpp",
    "model": "tiny.en"
  },
  "hotkey": "Ctrl+Shift+Enter",
  "warmUpEnabled": true
}
```

### GET /api/v1/settings
**Summary:** Fetch current user settings.

**Response** (200 OK):
```json
{
  "prompts": {
    "rewrite": "Rewrite for clarity and tone:",
    "summarize": "Summarize the following:",
    "email": "Rewrite in professional tone:"
  },
  "modes": {
    "default": "append"
  },
  "behaviors": {
    "clipboard": true,
    "autoPaste": true,
    "pasteDelayMs": 0
  },
  "advanced": {
    "warmUpOnLaunch": true,
    "debugLogging": false
  }
}
```

### POST /api/v1/settings
**Summary:** Update user settings (triggers, behaviors, advanced).

**Request** (`application/json`):
```json
{
  "prompts": { ... },
  "modes": { ... },
  "behaviors": { ... },
  "advanced": { ... }
}
```

**Response**:
- 204 No Content on success.

**Notes:**
- All endpoints are local-only and do not require an internet connection.
- The frontend should verify cursor context before auto-pasting; fallback is copy-to-clipboard only.
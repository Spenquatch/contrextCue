All processing routes are exposed via a local FastAPI server that the Tauri frontend consumes.

### POST /rewrite
Processes text input with the specified prompt.

**Request** (application/json):
```json
{
  "trigger": "rewrite",           // The user-defined trigger name
  "prompt": "Rewrite for clarity and tone:",
  "input": "I want to say this better but don’t know how.",
  "mode": "replace",             // "append" or "replace"
  "clipboard": true,               // Copy result to clipboard
  "autoPaste": true                // Paste result at cursor if valid
}
```

**Response** (200 OK):
```json
{
  "result": "I would like to express this more clearly..."
}
```

### POST /transcribe
Records a short audio clip and returns its transcription (and optional rewrite).

**Request** (application/json):
```json
{
  "trigger": "talk",             // Typically "talk"
  "prompt": "Rewrite for clarity and tone:",
  "mode": "append",
  "clipboard": true,
  "autoPaste": false
}
```

**Server Flow**:
1. Capture audio (in-memory or temp file).
2. Run `whisper.cpp` on the recording.
3. If a prompt is provided, send transcription to `/rewrite` logic.
4. Return transcription or rewritten text.

**Response** (200 OK):
```json
{
  "transcription": "This is what I said.",
  "result": "This is a refined version of what I said."
}
```

### GET /status
Returns health and configuration status.

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

### GET /settings
Fetches current settings for UI display.

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

### POST /settings
Update user settings (triggers, behaviors, advanced options).

**Request** (application/json):
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
**ContrextCue** is a lightweight, cross-platform desktop application for on-device text rewriting and speech-to-text transcription. Built with **Tauri** (Rust + React) and a **Python** sidecar, it lets users define keyboard or voice triggers to process input via local AI models and apply a range of user-configurable behaviors.

### Core Features

1. **Trigger-Based Rewrite**
    - Custom triggers (e.g., `\rewrite`, `\email`, `\summarize`) capture user input when followed by text.
    - A configurable hotkey (default: Ctrl + Shift + Enter) submits the input.
    - The trigger determines which prompt template to apply before sending text to the local LLM (Rene).
    - Processed output is inserted or copied according to user settings.
2. **Speech-to-Text + Rewrite**
	- A customizable trigger (e.g., `\talk`) activates listening mode:
	    - The trigger text is replaced with the words **"Listening..."** to indicate active recording.
	    - Audio is continuously processed(but not returned to the user) in real time by `whisper.cpp` (tiny.en model), producing incremental transcript updates.
	    - The transcript is buffered as text rather than buffering raw audio.
	- Recording and real-time transcription continue until the user types a customizable end trigger (e.g., `/end`) followed by the submission hotkey (e.g., Ctrl + Shift + Enter).
	- Once the end trigger is detected, the final buffered transcription is available immediately and may optionally be routed through the LLM pipeline using the configured prompt.
	- Transcribed or rewritten output follows the same insertion and clipboard rules as other text triggers
3. **Prompt-to-Output Insertion Modes**
    - **Append**: Inserts the output after the original input.
    - **Replace**: Deletes the original trigger and input, then pastes the processed output.
        - Deletion uses character-count-based backspacing limited to the scope of the trigger and input.
        - For contexts where cursor location cannot be determined, it falls back to copying to the clipboard only.
4. **Clipboard and Insertion Control**
    - Global and per-prompt toggles for:
        - Automatic paste at cursor
        - Copy to clipboard
        - Both
5. **Custom Prompt Mapping**
    - Create, edit, and delete custom trigger-to-prompt mappings via the settings UI.
    - Each mapping includes behavior settings (append/replace, clipboard/paste options).
6. **Settings UI**
    - Accessible from a system tray icon on Windows, macOS, and Linux.
    - Built with React and Tailwind; backed by secure local storage (e.g., Zustand or Tauri API).
    - User controls:
        - Define and manage custom prompts and triggers
        - Configure insert mode (append or replace)
        - Enable/disable clipboard copy and auto-paste
        - Set submission hotkey combinations
        - Toggle STT and LLM modules on or off
7. **Selected v1 Enhancements**
    - **Playground Panel**: Live prompt tester in settings; send ad-hoc input to `/rewrite` and preview results.
    - **Paste Delay (ms)**: Configurable delay before auto-pasting output to accommodate slow or complex editors.
    - **Advanced Panel**: Contains:
        - System-check button (verify model and STT availability)
        - Toggle for startup model warm-up
        - Toggle for debug logging
    - **Model Warm-Up on Launch**: Preload the LLM with a silent dummy prompt if enabled, reducing first-run latency.
    - **Smart Input Fallback**: Before pasting, verify the cursor is in an editable field; otherwise, only copy to clipboard.
8. **Modular Sidecar Backend**
    - Python-based service communicating via FastAPI.
    - Exposes endpoints for text rewriting, transcription, status, and settings queries.
    - Encapsulated runners (`llm_runner.py`, `stt_runner.py`) allow easy swapping of inference engines.

---
### 💻 Tech Stack

#### 🖥️ **Frontend (Tauri + React)**

| Component                   | Tech                                                      |
| --------------------------- | --------------------------------------------------------- |
| UI Framework                | **React / Shadcn/ui**                                     |
| Styling                     | **Tailwind CSS**                                          |
| State Management            | **Zustand** or **TanStack Store**                         |
| Desktop Shell               | **Tauri** (Rust)                                          |
| Tray/Native Integration     | **Tauri API (Rust)**                                      |
| Hotkey Registration         | **tauri-plugin-global-shortcut** (or Rust-based listener) |
| Storage (Settings)          | **Tauri secure storage API** or Zustand-persist           |
| Inter-process Communication | **Tauri Command Bridge (HTTP via FastAPI)**               |


---

#### 🧠 **Local Processing Sidecar (Python)**

| Component                   | Tech                                                                                                                   |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Language                    | **Python 3.11+**                                                                                                       |
| Task Queue / Command Router | **FastAPI** (serves as the local API interface to Tauri)                                                               |
| LLM Engine                  | llama.cpp running [Rene-v0.1-1.3b-pytorch](https://huggingface.co/cartesia-ai/Rene-v0.1-1.3b-pytorch) (quantized GGUF) |
| STT Engine                  | [`whisper.cpp`](https://github.com/ggerganov/whisper.cpp) with `tiny.en` model                                         |
| Audio Recording             | `sounddevice`, `pyaudio`, or CLI to temporary `.wav` file                                                              |
| Clipboard Control           | `pyperclip` or system-native fallbacks                                                                                 |
| Input Routing               | FastAPI endpoints for `transcribe`, `rewrite`, `status`, and `settings`                                                |
| Output Simulation           | `pyautogui`, `keyboard`, or Rust-based alternative for cursor-aware replacement                                        |
| Modular Wrappers            | `llm_runner.py` and `stt_runner.py` to encapsulate logic and support future engine swaps                               |


---

![[Environment Setup#📂 Folder Layout]]


---

#### ⌨️ **Keyboard Control & Output Insertion**

| Component                     | Tech                                                                               |
| ----------------------------- | ---------------------------------------------------------------------------------- |
| Key Listener                  | Rust: **tauri-plugin-global-shortcut**, or Python: `keyboard` / `pynput`           |
| Output Injection              | Python: `pyautogui`, `keyboard`, or `xdotool` (Linux)                              |
| Cursor-aware Text Replacement | Simulated keystrokes (backspace count) OR position-based, depending on app context |
| Clipboard                     | `pyperclip`, `clipboard`, or platform-native via Tauri/Python                      |


---

### 📝 Notes
- 🧩 System is modular and can replace `llama.cpp` or `whisper.cpp` with newer tools as they evolve or fallback to API calls.
- 🔒 All settings should be managed in app state (Zustand/store) and persisted via Tauri—not flat files.
- ⚙️ Architecture should support **real-time insertion at cursor** and **global hotkey triggering**, designed with the assumption that this will be a plugin-capable companion to **Contrext**.



### 📄 Deliverables
-  Cross-platform desktop app using Tauri (Windows/Linux/macOS)
-  whisper.cpp integration for local STT
-  llama.cpp integration for local LLM (Rene-SLM)
-  Trigger detection and hotkey capture system
-  Modular output logic (append/replace, clipboard behavior)
-  Minimal settings UI for managing triggers, hotkeys, and preferences
-  Fully documented codebase with setup + usage instructions
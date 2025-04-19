This document outlines the local development environment for ContrextCue, including prerequisites, recommended tools, directory layout, and step-by-step setup instructions.
### Prerequisites

- **Node.js** (v22.14.0+ recommended)  
  _Manage via [nvm](https://github.com/nvm-sh/nvm) for version control._

- **Rust toolchain** (via [rustup](https://rustup.rs/))  
  _Includes `cargo` for compiling native dependencies (required for Tauri)._

- **Python 3.12.10+**  
  Install via [pyenv](https://github.com/pyenv/pyenv) or system package manager.

### Recommended

- **uv** (Python project manager and dependency tool)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
# or via pip
pip install uv
```


---

### Frontend Setup

```bash
cd contrextCue/frontend
npm install      # install dependencies
npm run dev      # start the Vite + Tauri dev server
```
- Development UI available in browser and as Tauri window


---

### Rust Backend Setup

```bash
cd ContrextCue/src-tauri
rustup override set stable
cargo build                   # compile native shell\cargo tauri dev
```


---

### Python Sidecar Setup

### Using uv (preferred)

```bash
cd ContrextCue/sidecar
uv venv --python 3.12         # create & activate .venv

#Activate virtual Environment
#linux
source .venv/bin/activate      
#windows cmd 
.venv\Scripts\activate
#windows PowerShell 
.venv\Scripts\Activate.ps1

# install dependencies and run FastAPI
uv pip install .  # Install all project dependencies 
uv run start  # start FastAPI with autoreload
```

### Without uv (venv + pip)

```bash
cd ContrextCue/sidecar
python -m venv .venv         # create virtual environment
source .venv/bin/activate     # activate environment
pip install -r requirements.txt  # install dependencies
uv run start        # run FastAPI with autoreload
```


---

### 7. Running the Full Stack

Open three terminals:

1. **Sidecar**
```bash
cd ContrextCue/sidecar
uv run uvicorn main:app --reload
```

1. **Sidecar**
```bash
cd ContrextCue/frontend
npm run dev
```

```bash
cd ContrextCue/src-tauri
cargo tauri dev
```


---

## 8. Additional Tips

- Confirm endpoints at `http://localhost:8000/docs`
- Use the **Playground** in settings UI to test prompts live
- Check console logs in each terminal for errors


---

####  📂 Folder Layout

```js
contrextCue/
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── TriggerManager.tsx
│   │   │   ├── HotkeyConfigurator.tsx
│   │   │   ├── ClipboardToggle.tsx
│   │   │   └── ModuleToggles.tsx
│   │   ├── stores/
│   │   │   ├── promptsStore.ts
│   │   │   └── uiStore.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── tauri.conf.json
│   └── package.json
│
├── src-tauri/
│   ├── Cargo.toml
│   └── src/
│       ├── main.rs
│       ├── keylistener.rs
│       └── sidecar_launcher.rs
│
├── sidecar/
│   ├── uv.lock  
│   ├── pyproject.toml
│   └── src/contrextcue_sidecar/  
│       ├── main.py
│       ├── llm_runner.py
│       ├── stt_runner.py
│       ├── utils.py
│       ├── routers/
│       │   ├── rewrite.py
│       │   ├── transcribe.py
│       │   ├── settings.py
│       │   └── status.py
│       ├── schemas/
│       │   ├── rewrite.py
│       │   ├── transcribe.py
│       │   ├── settings.py
│       │   └── status.py
│       └── models/
│           └── prompts.yaml
├── .gitignore
├── README.md
├── LICENSE
├── .env
└── .github/workflows/ci.yml
```

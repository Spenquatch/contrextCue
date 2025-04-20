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
cd contrextCue/src-tauri
rustup override set stable
cargo build                        # compile native shell
cargo tauri dev                    # run in dev mode
```


---

### Python Sidecar Setup

### Using uv (preferred)

```bash
cd contrextCue/sidecar
uv venv --python 3.12         # create & activate .venv

#Activate virtual Environment
#linux
source .venv/bin/activate      
#windows cmd 
.venv\Scripts\activate
#windows PowerShell 
.venv\Scripts\Activate.ps1

# install dependencies and run FastAPI
uv pip install .                    # install runtime deps
uv install --group dev              # install dev tools (ruff, pytest)
uv run start  # start FastAPI with autoreload
```


---

### 7. Running the Full Stack

Open three terminals:

1. **Sidecar**

```bash
cd contrextCue/sidecar
uv run start
```

2. **Frontend + Tauri**

```bash
cd ContrextCue/frontend
npm run dev
```

3. **Rust Shell**

```bash
cd ContrextCue/src-tauri
cargo tauri dev
```


---

## 8. Additional Tips

- Swagger UI: [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)
- OpenAPI JSON: [http://localhost:8000/api/v1/openapi.json](http://localhost:8000/api/v1/openapi.json)
- ReDoc: [http://localhost:8000/api/v1/redoc](http://localhost:8000/api/v1/redoc)
- Use `scripts/generate-openapi.sh` to refresh your TS client locally
- Keep `uv.lock`, `package-lock.json`, and `Cargo.lock` committed


---

####  📂 Folder Layout - High Level

```text
ContrextCue/
├── frontend/        # Tauri + React
├── src-tauri/       # Rust shell
├── sidecar/         # Python FastAPI service (src/…)
├── scripts/         # helper scripts (e.g. generate-openapi.sh)
└── .github/         # CI workflows
```


####  📂 Folder Layout - Detail

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


This document covers the DevOps and CI/CD practices for ContrextCue, including licensing, project initialization, continuous integration, release packaging, and repository conventions.

---

## 1. License

Include an `LICENSE` file at the project root. We recommend the MIT License. Create a file named `LICENSE` with the following content:

```text
MIT License

Copyright (c) 2025 Spenser McConnell

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

For full text, see [https://opensource.org/licenses/MIT](https://opensource.org/licenses/MIT).

---

## 2. Project Initialization

### Frontend (Tauri + React)

1. Create a `package.json` and install production and dev dependencies:

```bash
cd contrextCue/frontend
npm init -y
npm install react react-dom @tauri-apps/api tailwindcss zustand axios
npm install --save-dev typescript @types/react @types/node vite eslint prettier jest
npm install --save-dev typescript @types/react @types/node vite eslint prettier jest @openapitools/openapi-generator-cli
```

2. Define npm scripts in `package.json`:

```json
"scripts": {
    "dev": "vite",
    "build": "vite build",
    "lint": "eslint src --ext .tsx,.ts",
    "pretty": "prettier --write \"src/**/*.{ts,tsx,js,jsx,json,css,md}\"",
    "test": "jest",
    "dev:ci": "npm run pretty && npm run lint && npm run dev",
    "build:ci": "npm run pretty && npm run lint && npm run build"
}
```

3. Create a `scripts/` folder at the repo root with `generate-openapi.sh` to dump and regenerate your TS client.

```bash
#!/usr/bin/env bash
set -e

# Ensure sidecar spec is up to date
pushd sidecar
uv run start --reload &   # or however you spin it up
PID=$!
sleep 2                    # wait for the server
popd

# Dump the spec
curl http://localhost:8000/api/v1/openapi.json -o docs/openapi.json
  
# Kill the sidecar
kill $PID

# Generate the TS client
pushd frontend
npx openapi-generator-cli generate \
  -i ../docs/openapi.json \
  -g typescript-axios \
  -o src/api-client \
  --additional-properties=supportsES6=true,withSeparateModelsAndApi=true,apiPackage=api,modelPackage=models
popd
```

### Sidecar (Python + uv)

1. Initialize the project and virtual environment with uv:

```bash
cd ContrextCue/sidecar
uv init .
uv venv --python 3.12
```

2. Declare dependencies in `pyproject.toml`:

```toml
[project]
name = "contrextcue_sidecar"
version = "0.1.0"
description = "ContrextCue is a lightweight, cross-platform desktop application for on-device text rewriting and speech-to-text transcription."
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
  "fastapi>=0.115.12",
  "uvicorn>=0.34.1",
  "pyperclip>=1.8",
  "pynput>=1.8.1"
]

[project.optional-dependencies]
dev = [
  "ruff",
  "pytest"
]

[project.scripts]
start = "contrextcue_sidecar.main:start"
```

3. Install:

```bash
uv pip install .
uv run start
```


---

## 3. Continuous Integration (GitHub Actions)

All CI pipelines live under `.github/workflows/ci.yml`. This workflow runs linters, tests, and builds for each major component.

### Caching

- Frontend: cache `~/.npm` between runs
- Python: cache `sidecar/.venv` if uv supports caching the venv directory
- Rust: cache `~/.cargo/registry` and `~/.cargo/git`

---

## 4. Release Packaging

Release builds produce native installers for Windows, macOS, and Linux.

1. **Tauri Build**

```bash
cd frontend && npm ci --production
cd src-tauri
cargo tauri build
```

- Outputs located in `src-tauri/target/release/bundle`
	- Windows: `.exe` NSIS or MSI
	- macOS: `.app` and `.dmg`
	- Linux: AppImage, `.deb`, `.rpm`
2. **Python Sidecar**
    - **Option A: Vendored venv**
        - Include `sidecar/.venv` directory in the bundle resources.
    - **Option B: PyInstaller**
    - Copy `dist/contrextcue_sidecar` into Tauri `bundle.resources`.

```bash
cd sidecar
uv run pyinstaller --onefile --name contrextcue_sidecar main.py
```

3. **Automated Releases**
    - Create a GitHub Action on `push: tags: ['v*']` to:
        - Run CI pipeline
        - Build production bundles
        - Upload artifacts as GitHub Releases

---

## 5. Repository Conventions

- Commit lockfiles: `uv.lock`, `package-lock.json`, `Cargo.lock`
- **.gitignore:**
```bash
# Node (frontend)

frontend/node_modules/
frontend/src/api-client
frontend/.vite/
frontend/.next/
frontend/dist/
frontend/.output/


# Rust (src-tauri)
src-tauri/target/
src-tauri/.cargo/
src-tauri/Cargo.lock
  
# Python (sidecar)
sidecar/build
sidecar/src/contrextcue_sidecar.egg-info
sidecar/.venv/
sidecar/__pycache__/
sidecar/.mypy_cache/
sidecar/.pytest_cache/
sidecar/*.pyc

# VS Code project files (optional)

.vscode/
*.code-workspace

# System files
.DS_Store
Thumbs.db

# Logs and build junk
*.log
*.bak
*.swp
.env
```

- No secrets in repo; use GitHub Secrets
- Documentation files live under `docs/`

---

## 6. Next Steps

- **Bootstrap & verify the frontend**
    - Install dependencies and run Vite to confirm the React app renders at `localhost:3000`
    - Add a simple component that calls the generated Status API and displays its response
- **Initialize Tauri integration**
    - Scaffold the Tauri config so your Vite dev server becomes the desktop window
    - Expose a placeholder Rust command and invoke it from React to validate the command bridge
- **Wire up core features in React**
    - Build the **TriggerManager** component that uses the Rewrite API to transform user input
    - Integrate the **Transcribe** flow into a UI control that records and displays transcripts
    - Hook the **Settings** panel to the `/settings` endpoints for live prompt and behavior changes
- **Global shortcut support**
    - Configure `tauri-plugin-global-shortcut` in the Rust shell to listen for your hotkey combo
    - Map the shortcut to invoke the appropriate React action (rewrite or transcribe)
- **Enhance CI/CD with coverage and security**
    - Add frontend and Python coverage reporting to your GitHub Actions and publish to Codecov
    - Enable Dependabot updates and CodeQL security scans on the repo
    - Wire up semantic‑release to automate version bumps and changelog generation
- **Release automation**
    - Extend CI to trigger on `v*` tags, build Tauri bundles and sidecar executables
    - Publish installers and sidecar artifacts as GitHub Release assets
- **Polish & iteration**
    - Build the “Playground” test page for ad‑hoc prompt experimentation
    - Refine settings persistence (secure local storage) and UI validation
    - Begin swapping stub runners for production Whisper/llama logic and real‑time streaming
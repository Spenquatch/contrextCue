
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
npm install react react-dom @tauri-apps/api tailwindcss zustand
npm install --save-dev typescript @types/react @types/node vite eslint prettier jest
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

### Sidecar (Python + uv)
1. Initialize the project and virtual environment with uv:

```bash
cd contrextCue/sidecar
uv init .
```

2. Declare dependencies in `pyproject.toml`:

```toml
[project]
name = "contrextcue-sidecar"
version = "0.1.0"
description = "ContrextCue is a lightweight, cross-platform desktop application for on-device text rewriting and speech-to-text transcription."
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
  "fastapi",
  "uvicorn",
  "pyperclip>=1.8",
  "pynput>=1.8.1"
]

[project.optional-dependencies]
dev = [
  "ruff",
  "pytest"
]
```


---

## 3. Continuous Integration (GitHub Actions)

All CI pipelines live under `.github/workflows/ci.yml`. This workflow runs linters, tests, and builds for each major component.

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v3
        with: node-version: 18
      - run: |
          cd frontend
          npm ci
          npm run lint
          npm test
  rust:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-rust@v1
        with: rust-version: stable
      - run: |
          cd src-tauri
          cargo fmt -- --check
          cargo clippy -- -D warnings
          cargo build --release
  python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with: python-version: 3.11
      - run: |
          pip install uv
          cd sidecar
          uv venv --python 3.11
          uv pip sync requirements.txt
          uv run ruff .
          uv run pytest
```

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
/frontend/node_modules
/src-tauri/target
/sidecar/.venv
uv.lock
__pycache__/
*.py[cod]
```
- No secrets in repo; use GitHub Secrets
- Documentation files live under `docs/`

---

## 6. Next Steps

- **Formalize the Sidecar API**
    - Split `main.py` into modular FastAPI routers (`routers/…`)
    - Define Pydantic request/response schemas in `schemas/…`
- **Publish & Document the API**
    - Enable OpenAPI generation (e.g. expose at `/api/v1/openapi.json`)
    - Wire up Swagger UI at `/api/v1/docs` and optionally ReDoc at `/api/v1/redoc`
- **Generate & Integrate Client SDKs**
    - Use the OpenAPI spec to auto‑generate a TypeScript client for your frontend
    - (Optionally) generate a Python client for other integrations
- **Strengthen CI/CD**
    - Add code‑coverage reporting (frontend + Python) and push reports to Codecov or Coveralls
    - Configure dependency‑scan bots (Dependabot for JS/Python, CodeQL for security)
    - Wire up semantic‑release (or similar) to bump versions, update `CHANGELOG.md`, and tag releases
- **Automate Releases**
    - Extend your GitHub Actions to build & bundle installers on tag pushes (`v*`)
    - Publish artifacts automatically to GitHub Releases

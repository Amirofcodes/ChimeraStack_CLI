# 📝 ChimeraStack CLI Sprint Board

_Updated May 3 2025_

Keep it lightweight: tick a box, push, repeat.

---

## 🟢 Sprint 1 — Packaging & CI Cleanup (aim v0.2.4)

### 1 · Packaging

- [x] Remove `setup.py` & `setup.cfg`
- [x] Add **setuptools‑scm**; mark `dynamic = ["version"]` in _pyproject.toml_
- [x] Surface `__version__` in `src/chimera/__init__.py`

### 2 · CI / Release Pipeline

- [ ] Replace `python setup.py …` with `pipx run build`
- [ ] Upload wheel + sdist to PyPI on tag
- [ ] Build & push Docker image `ghcr.io/chimera/cli:<tag>`
- [ ] Build PyInstaller bundles (macOS & Linux) → attach to GitHub Release

### 3 · Repo Hygiene

- [ ] Purge historical binaries via _git filter‑repo_
- [ ] Add `releases/` & `dist/` to `.gitignore`

### 4 · Test Pyramid Foundation

- [ ] Unit tests mock Docker (PortAllocator, TemplateManager)
- [ ] Snapshot tests for rendered compose/env files
- [ ] Smoke test: `chimera create … && docker compose config`

---

## 🟡 Sprint 2 — ComposeGraph Refactor + Sentinel Templates (aim v0.2.5)

### 5 · Core Graph

- [ ] Implement `compose_graph.py`
- [ ] Integrate `PortAllocator.allocate()` into graph nodes
- [ ] Refactor `TemplateManager` to build graph then render

### 6 · Sentinel Templates

- [ ] **frontend/react-static** – add Chimerastack welcome page elements
- [ ] **backend/php-web** – ensure Nginx + 3 DB variants; welcome page shows port links
- [ ] **fullstack/react-php** – verify against new graph, fix any schema drift

### 7 · Project Stamp

- [ ] Write `.chimera.yml` (`cli_version`, `created_at`) into generated projects

### 8 · Docs

- [ ] Update README & authoring docs for new graph flow
- [ ] CONTRIBUTING: how to run tests without Docker

---

## 🟠 Sprint 3 — Plugin MVP (aim v0.3.0)

### 9 · Plugin API

- [ ] Define `chimera.plugin_api` base class
- [ ] Entry‑point discovery (`[chimera.plugins]` in `pyproject.toml`)
- [ ] Typer auto‑mount: `chimera add <plugin>`

### 10 · Sample Plugins

- [ ] **Redis** (single service)
- [ ] **Netdata** (monitoring stack)

### 11 · Validation

- [ ] Conflict & port‑collision checker after plugin mutations
- [ ] Snapshot tests for plugin‑augmented compose output

---

## 🟣 Sprint 4 — Template Expansion A (aim v0.3.1)

- [ ] `fullstack/django-react-postgres`
- [ ] Document community submission workflow
- [ ] Integrate first community template (stretch)

---

## 🔮 Backlog / Nice‑to‑Have

- [ ] Port lockfile persistence (`~/.chimera/ports.json`)
- [ ] `chimera update` to bump an existing project’s stack
- [ ] VS Code devcontainer generator

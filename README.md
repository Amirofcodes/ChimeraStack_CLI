# ChimeraStack CLI

> Legacy CLI for template-based Docker development environments.

[![PyPI](https://img.shields.io/pypi/v/chimera-stack-cli)](https://pypi.org/project/chimera-stack-cli)
[![CI](https://github.com/Amirofcodes/ChimeraStack_CLI/actions/workflows/ci.yml/badge.svg)](https://github.com/Amirofcodes/ChimeraStack_CLI/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Project status

**Maintenance mode.**

`chimera-stack-cli` remains available on PyPI and can still be used for existing workflows.
The project is no longer the primary product focus.

### Strategic pivot

The Smart Port Allocation capability from ChimeraStack is being evolved into a dedicated project:

➡️ **[smart-port-allocator](https://github.com/Amirofcodes/smart-port-allocator)**

If your main need is preventing local port conflicts (`address already in use`), use and follow that repository.

---

## What ChimeraStack still provides

- Template-based local environment scaffolding
- Docker Compose-oriented project generation
- Existing command workflows for legacy users

---

## Install

```bash
pipx install chimera-stack-cli
# or
pip install chimera-stack-cli
```

---

## Migration guidance

- Existing users: you can continue using ChimeraStack as-is.
- New users focused on local networking/ports: start with `smart-port-allocator`.
- Long-term direction: port-conflict tooling and reliability utilities are developed in the new repo.

---

## Legacy docs

For historical docs and previous feature scope, browse the repository history and `docs/` folder.

---

## License

MIT

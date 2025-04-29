# 🛣️ ChimeraStack CLI Roadmap

This roadmap outlines the planned evolution of the ChimeraStack CLI from v0.1.0 onward. The goal is to make the CLI more modular, extensible, and powerful for developers who need production-ready local development environments with zero configuration and dynamic port allocation.

---

## ✅ v0.2.0 – Template Refactor & Structure Redesign

**Objective:** Migrate template structure to support clearer categories and future expansion.

### Tasks

- [ ] Refactor templates into:
  - `frontend/`
  - `backend/`
  - `fullstack/`
- [ ] Update `template.yaml` format:
  - Add `category`, `tags`, `description`
- [ ] Update `chimera list` command to support new structure
- [ ] Update `chimera create` logic to support new categories
- [ ] Add backward compatibility for legacy paths (temporary)
- [ ] Update documentation and GitHub release

---

## 🔌 v0.3.0 – Plugin System

**Objective:** Introduce plugin-style services (e.g., monitoring, logging) that can be dynamically added.

### Tasks

- [ ] Define plugin system (YAML fragments + compose merge)
- [ ] Create `chimera add service <plugin>` command
- [ ] Implement first plugins:
  - Monitoring (e.g., Netdata)
  - Logging (e.g., Loki/Grafana)
  - Redis
- [ ] Ensure dynamic ports are allocated for plugins
- [ ] Add plugin documentation + examples

---

## 🔀 v0.4.0 – Mix & Match Composition

**Objective:** Allow users to build environments from selected components.

### Tasks

- [ ] Add `chimera init` with:
  ```bash
  chimera init my-app --frontend react --backend php --db mysql
  ```

````

- [ ] Add service-to-template mapping logic
- [ ] Compose Docker Compose files from modular parts
- [ ] Add fallback interactive wizard

---

## ☁️ v0.5.0 – Deployments (Coolify or Generic)

**Objective:** Allow deploying Chimera environments to remote hosts like Coolify or via SSH.

### Tasks

- [ ] Add `chimera deploy` command
- [ ] Integrate with Coolify via webhook or Git
- [ ] Optional SSH + Docker deployment
- [ ] Add project-level config: `.chimera/project.yaml`
- [ ] Add domain + SSL prompts (for Coolify)

---

## 🧪 Optional Enhancements (Parallel or Future Work)

- [ ] `chimera test template` command for verifying a template’s structure and health
- [ ] `chimera update templates` to pull remote or latest templates
- [ ] Template marketplace (public repo integration)
- [ ] VSCode `.devcontainer` auto-generation
- [ ] Documentation portal + live template browser

---

## 🔖 Version Tags Summary

| Version  | Milestone                                      |
| -------- | ---------------------------------------------- |
| `v0.2.0` | Template refactor (frontend/backend/fullstack) |
| `v0.3.0` | Plugin system                                  |
| `v0.4.0` | Mix & Match environments                       |
| `v0.5.0` | Deployment support                             |

---

## 💬 Contributions & Feedback

If you'd like to contribute to any part of this roadmap or suggest ideas, open a discussion or issue on GitHub.

---

```

```
````

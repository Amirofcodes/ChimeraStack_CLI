# 📝 ChimeraStack CLI – Pre-v0.3.0 Cleanup Checklist

> Goal: tidy up the template engine and project generator so that new
> roadmap features (plugin system, mix-&-match composition, deployments…)
> can be implemented without fighting legacy quirks.

---

## 1. Template Specification & Validation

- [x] Draft JSON-Schema for `template.yaml` (stack, component, core).
- [x] Add schema validation step in `TemplateManager` (fail fast with
      helpful error).
- [x] Create `scripts/validate_templates.py` to walk templates and validate.
- [x] Wire validation into local pre-commit hook.
- [ ] Wire validation into GitHub Actions.

## 2. Rendering Pipeline

- [x] Introduce Jinja2 rendering helper (`utils/render.py`).
- [x] Migrate variable substitution from ad-hoc `str.replace` to Jinja2
      (start with `README.md`, `.env`, then `docker-compose.yml`).
- [x] Remove legacy `_process_yaml_file`, `_process_template_file`
      string-replace blocks once migration complete.

## 3. Docker-Compose Strategy

- [x] Adopt single canonical compose file per stack:
      `docker-compose.<variant>.yml` (no `.override`, no `.base`).
- [x] Adopted for backend/php-web and fullstack/react-php stacks.
- [x] Remaining stacks (if any) to migrate. _(None left)_
- [x] Flatten compose generation logic – drop heuristic scan in
      `_allocate_service_ports()`.
- [ ] Move compose fragments that belong to components into
      `base/<component>/compose/<service>.yml` (to be included by Jinja2).

## 4. Port Allocation Refactor

- [x] Extract port range mapping to `config/ports.yaml`.
- [x] Make `PortAllocator` read ranges from config.
- [x] Remove fallback scan over all compose files.

## 5. Cleanup Mechanism

- [x] Replace monolithic `_cleanup_project_structure()` with
      per-component `post_copy` tasks declared in `template.yaml`.
- [x] Provide helper that executes these tasks after copy.

## 6. Directory / Naming Conventions

- [x] Ensure all stacks & components use kebab-case IDs (verified and enforced).
- [x] Standardise variant files naming (`mysql`, `mariadb`, `postgresql`).
- [x] Remove stray `.override` and `.base` files after new pipeline is
      in place.

## 7. Tests & CI

- [x] Unit tests for `TemplateManager.create_project()` covering
      each stack + variant.
- [x] Integration test: `chimera create temp-proj -t backend/php-web -v
postgresql` then `docker compose config` must be valid.
- [x] GitHub Actions job running tests + schema validation.

### Additional Test Coverage:

1. Unit Tests:

   - [ ] Test template validation
   - [ ] Test port allocation edge cases
   - [ ] Test cleanup mechanisms
   - [ ] Test error handling scenarios

2. Integration Tests:

   - [ ] Test project creation with all variants
   - [ ] Test custom configurations
   - [ ] Test database initialization
   - [ ] Test project cleanup

3. CI Improvements:
   - [ ] Add test coverage reporting
   - [ ] Add linting checks (flake8, black)
   - [ ] Add schema validation for all templates
   - [ ] Add dependency security scanning

## 8. Developer Documentation

- [x] `docs/authoring-templates.md`: how to author a component/stack.
- [x] Update `README.md` with new contribution guidelines.

---

### Nice-to-Have (can slip to later)

- [ ] Switch to `ruamel.yaml` for preserving comments/order when writing
      YAML files.
- [ ] Provide `chimera test template` (see Roadmap Optional Enhancements).

---

_Once all boxes above are checked we can confidently move on to v0.3.0
plugin system work without legacy friction._

## 9. House-keeping after §1-3 refactor (added later)

- [ ] Trim unused `docker-compose.*.yml` files after project generation so a
      created project only contains the canonical variant file it actually
      uses.
- [ ] Inject `ADMIN_PORT` into the PHP service environment so the welcome page
      can display the correct DB-admin link without triggering
      `htmlspecialchars(false)`.
- [ ] Add a small retry/back-off loop (or delayed attempt) in
      `src/pages/home.php` before the first DB connection to avoid transient
      _SQLSTATE[HY000] [2002] Connection refused_ on fresh `docker-compose up`.

# 10. Noise-reduction follow-ups

- [ ] Silence placeholder-render warnings by executing `post_copy` **before** the YAML-processing pass or by narrowing the compose-file glob to only the canonical `docker-compose.yml`.
- [ ] Delete empty `config/` directories via stack/component `post_copy` once no longer needed.

_SQLSTATE[HY000] [2002] Connection refused_ on fresh `docker-compose up`.

## 11. Optional Hardening Tasks (post-0.2.0)

- [ ] Audit all stack `template.yaml` files – ensure each declares a `README.md` in its `files:` block (`grep -R "files:" src/chimera/templates/stacks | …`).
- [ ] Refactor `TemplateManager._create_readme()` so it executes **after** `post_copy` tasks when a README is still missing (safety-net fallback).
- [ ] Ensure each template's `welcome_page.sections` covers every exposed service so the CLI summary prints correct ports.

## 12. Template Expansion Tasks (v0.2.5)

> Follow the step-by-step process described in `docs/authoring-templates.md` for every new **stack** listed below. Each bullet maps to a subsection of the Authoring Guide (Directory Layout → template.yaml → Compose & Jinja2 → post_copy → Validation & Testing → Publishing).

### Phase A — Minimum Effort, Biggest Reach

#### 12.1 `beginner/php-static-site-sqlite`

- [ ] Create folder `templates/stacks/beginner/php-static-site-sqlite/`.
- [ ] Draft `template.yaml` (name, version, id, description, tags, variables).
- [ ] Copy `backend/php-web` component include + add `database/sqlite` component.
- [ ] Write `docker-compose.yml.j2` (no ports → relies on PortAllocator; use volume for SQLite file).
- [ ] Declare `post_copy` to rename `.env.example` → `.env`.
- [ ] Add **welcome_page** sections so port summary prints correctly.
- [ ] Unit test: ensure schema validation passes & PortAllocator assigns default HTTP port.
- [ ] Integration smoke test: `chimera create demo -t beginner/php-static-site-sqlite` followed by `docker compose config`.
- [ ] Add entry to catalogue if maintained.

#### 12.2 `frontend/react-static`

- [ ] Folder `templates/stacks/frontend/react-static/`.
- [ ] Provision `template.yaml` (id `frontend/react-static`).
- [ ] Bundle a Vite `Dockerfile` or use `node:lts` image with hot-reload.
- [ ] Compose exposes `:5173` (dev server) via PortAllocator.
- [ ] Add variables (`project_name`, `ports.web`).
- [ ] post_copy: delete `docker-compose.dev.yml` placeholder.
- [ ] Tests: schema, create, docker compose config.

#### 12.3 `fullstack/django-react-postgres`

- [ ] Components: `backend/django`, `frontend/react-static`, `database/postgresql`.
- [ ] Multi-compose setup: React dev server proxied to Django API.
- [ ] Ensure Django `settings.py` uses env vars substituted by Jinja2.
- [ ] Healthchecks for Django + Postgres.
- [ ] Seed Postgres with demo user inside post_copy (`command` task).
- [ ] Add unit/integration tests (including DB migration).

### Phase B

#### 12.4 `backend/fastapi-celery-postgres`

- [ ] Stack directory `backend/fastapi-celery-postgres`.
- [ ] Services: FastAPI (uvicorn), Celery worker, Celery Beat, Redis, Postgres, Flower dashboard.
- [ ] Compose fragments under `compose/` for clearer includes.
- [ ] Swagger URL printed in welcome page.
- [ ] Tests: ensure Celery worker service and API both healthy.

#### 12.5 `backend/node-express`

- [ ] Starter Express API with nodemon.
- [ ] Optional MongoDB variant reserved for later; initial version uses SQLite or Postgres.
- [ ] Example endpoint & Jest tests scaffold in template.

#### 12.6 `fullstack/laravel-vue-mysql`

- [ ] Use `backend/laravel` component + `frontend/vue` component + `database/mysql`.
- [ ] Sail-like setup for Laravel queue & scheduler.
- [ ] Post_copy tasks: generate Laravel APP_KEY, run `npm install && npm run build` for Vue.

---

**General Checklist for Each New Template** (reuse across items above):

1. Directory skeleton created.
2. Valid `template.yaml` committed.
3. At least one `.j2` file renders without placeholders.
4. `README.md` inside template explaining usage & gotchas.
5. Ports allocated via `PortAllocator`, no hard-coded numbers.
6. Unit test + integration smoke test added.
7. Catalogue (`templates.yaml` or CLI list) updated.
8. Docs snippet added to main README (commands & description).

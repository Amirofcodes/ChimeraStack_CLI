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

- [ ] Ensure all stacks & components use kebab-case IDs.
- [ ] Standardise variant files naming (`mysql`, `mariadb`, `postgresql`).
- [ ] Remove stray `.override` and `.base` files after new pipeline is
      in place.

## 7. Tests & CI

- [ ] Unit tests for `TemplateManager.create_project()` covering
      each stack + variant.
- [ ] Integration test: `chimera create temp-proj -t backend/php-web -v
postgresql` then `docker compose config` must be valid.
- [ ] GitHub Actions job running tests + schema validation.

## 8. Developer Documentation

- [ ] `docs/templates.md`: how to author a component/stack.
- [ ] Update `README.md` with new contribution guidelines.

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

# React PHP Fullstack Template

Welcome to your ChimeraStack-generated full-stack development environment! This stack gives you:

- **Modern Frontend**: React (TypeScript) with Vite and Tailwind CSS
- **Production-ready Backend**: PHP-FPM with API routing through Nginx
- **Database Options**: MySQL, MariaDB, or PostgreSQL (configured via variant)
- **Administrative Tools**: phpMyAdmin or pgAdmin depending on your database

---

## Getting started

```bash
# start containers in the background
$ docker compose up -d

# tail logs (optional)
$ docker compose logs -f --tail=50
```

After the containers are **healthy** you can visit:

| Service                     | URL                               |
| --------------------------- | --------------------------------- |
| Frontend (React SPA)        | http://localhost:${WEB_PORT}      |
| React Dev Server (optional) | http://localhost:${FRONTEND_PORT} |
| Backend API                 | http://localhost:${WEB_PORT}/api  |
| Database Admin Console      | http://localhost:${ADMIN_PORT}    |

---

## Development workflow

### Frontend

The frontend uses Vite for blazing-fast HMR (Hot Module Replacement) and Tailwind CSS for styling:

```bash
# inside container (one-off commands)
$ docker compose exec frontend sh

# Install dependencies
/app $ npm install <package>

# Build for production (already in Dockerfile)
/app $ npm run build
```

Edit files in `frontend/src/` to see immediate updates in the browser. The frontend is pre-configured with:

- TypeScript support
- Tailwind CSS integration
- Vite development server
- API connection setup

### Backend

PHP files live under `backend/`. The web root is `backend/public/` and API routes are served from `backend/public/api`.

- Add new endpoints in `backend/public/api/`.
- Use `backend/bootstrap.php` for shared setup (autoloading, env, db).
- Live reload isn't required – Nginx + PHP-FPM auto-serve the updated files.

### Database

Database connection details are injected via environment variables. Default credentials:

```
DB_USER=${DB_USERNAME}
DB_PASSWORD=${DB_PASSWORD}
DB_DATABASE=${DB_DATABASE}
DB_HOST=db
DB_PORT={{ "5432 for PostgreSQL" if DB_ENGINE == 'postgresql' else "3306 for MySQL/MariaDB" }}
```

Use the appropriate admin tool (phpMyAdmin or pgAdmin) at http://localhost:${ADMIN_PORT}.

{% if DB_ENGINE == 'postgresql' %}
Connect to PostgreSQL directly with: `docker compose exec db psql -U $DB_USERNAME -d $DB_DATABASE`
{% else %}
Connect to {{ "MySQL" if DB_ENGINE == 'mysql' else "MariaDB" }} directly with: `docker compose exec db mysql -u$DB_USERNAME -p$DB_PASSWORD $DB_DATABASE`
{% endif %}

---

## Infrastructure

The template uses:

- Nginx as a reverse proxy (routing API calls to PHP backend, other traffic to frontend)
- Docker volumes for database persistence
- Environment variables for configuration
- Healthchecks for container dependencies

---

## Customising ports

The CLI auto-selects free ports at project creation. Edit `.env` if you need to change them after setup.

---

## Useful commands

```bash
# stop and remove containers
$ docker compose down

# rebuild images after Dockerfile changes
$ docker compose build --no-cache

# view frontend logs
$ docker compose logs -f frontend

# execute composer commands in backend
$ docker compose exec backend composer require <package>
```

---

Happy coding! 🚀

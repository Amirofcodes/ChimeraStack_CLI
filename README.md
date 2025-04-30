# ChimeraStack CLI

A powerful development environment manager that helps you quickly set up and manage local development environments using pre-configured templates.

## Features

- 🚀 Zero-configuration development environments
- 🔄 Dynamic port allocation
- 📦 Pre-configured templates for various stacks
- 🛠️ Customizable and extensible
- 🔌 Plugin system (coming soon)

## Installation

```bash
pip install chimera-cli
```

## Usage

### Create a New Project

```bash
# Interactive mode
chimera create my-project

# Using a specific template
chimera create my-project -t backend/php/nginx-mysql
```

### List Available Templates

```bash
# List all templates
chimera list

# Search templates
chimera list -s mysql

# List templates by category
chimera list -c backend
```

## Template Categories

Templates are organized into the following categories:

### Frontend Templates

- React applications
- Vue.js applications
- Angular applications
- Static sites

### Backend Templates

- PHP/MySQL stacks
- Python/PostgreSQL stacks
- Node.js/MongoDB stacks
- Ruby on Rails setups

### Fullstack Templates

- MERN stack (MongoDB, Express, React, Node.js)
- LAMP stack (Linux, Apache, MySQL, PHP)
- React + PHP + MySQL
- Vue.js + Python + PostgreSQL

## Template Structure

Templates are organized in a hierarchical structure:

```
templates/
├── base/
│   ├── core/
│   │   └── welcome/          # Common welcome page
│   ├── backend/
│   │   └── php/             # PHP-FPM configuration
│   └── database/
│       ├── mysql/           # MySQL configuration
│       ├── postgresql/      # PostgreSQL configuration
│       └── mariadb/         # MariaDB configuration
└── stacks/
    └── backend/
        └── php-web/         # PHP web stack with DB choice
            ├── docker-compose.base.yml
            ├── docker-compose.mysql.yml
            ├── docker-compose.postgresql.yml
            └── docker-compose.mariadb.yml
```

### Template Configuration

Each template must include a `template.yaml` file that defines its configuration. Here's an example:

```yaml
name: "PHP MySQL Development"
version: "1.0.0"
description: "PHP development environment with MySQL database"

tags:
  - php
  - mysql
  - development

services:
  web:
    port_range: "8000-8999"
  db:
    port_range: "3306-3399"
# See template.yaml.example for full configuration options
```

For a complete example of template configuration, see `templates/template.yaml.example`.

## Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🚀 Why ChimeraStack?

Whether you're building APIs, fullstack apps, or just want a production-ready local dev environment, ChimeraStack gives you:

- ✅ Smart dynamic port allocation (run many projects at once)
- ✅ Fully containerized
- ✅ Ready-to-use templates: React, PHP, MySQL, PostgreSQL, and more comming
- ✅ CLI simplicity + growing web integration
- ✅ Plugin-ready, modular architecture (coming soon)

---

## 🧩 Project Structure

ChimeraStack CLI is part of the **ChimeraStack ecosystem**, which includes:

- **CLI Tool**: Generate, run, and extend dev environments from your terminal
- **Web Platform**: [chimerastack.com](https://www.chimerastack.com)
  - Browse templates
  - Download CLI
  - Manage downloads
  - Support the project

---

## 🛠️ Prerequisites

- Python 3.8+
- Docker and Docker Compose installed and running
- `pip` (Python package manager)

---

## ✨ Features

### ✅ Template-Based Environment Creation

- Create projects from pre-defined, production-ready stacks

### 🔄 Dynamic Port Allocation

- Avoid port conflicts by auto-assigning based on service type:
  - Frontend (React): `3000–3999`
  - Backend (PHP/Node): `8000–8999`
  - MySQL: `3300–3399`
  - PostgreSQL: `5432–5632`
  - MariaDB: `3400–3499`
  - Admin tools: `8081+`

### 📦 Available Stacks (v0.1.0)

- PHP/Nginx with:
  - MySQL
  - PostgreSQL
  - MariaDB
- React + PHP Fullstack (with MySQL)

---

## ⚡ Quick Start

### Install ChimeraStack CLI

#### Option 1: PyPI (Recommended)

```bash
pip install chimera-stack-cli
```

#### Option 2: Prebuilt Binaries

Download for [Linux/macOS](https://www.chimerastack.com/download), then:

```bash
chmod +x chimera-stack-cli-*
./chimera-stack-cli-macos
```

---

### Create a Project

```bash
chimera create my-project
```

You'll be prompted to choose:

```
? Choose a category:
❯ Backend
  Frontend
  Fullstack
? Choose a template:
❯ backend/php/mysql
  fullstack/react-php/mysql
```

Then:

```bash
cd my-project
docker-compose up -d
```

Done. Your services are up and running on dynamic, non-conflicting ports.

---

## 🔮 Roadmap

| Version  | Milestone                                                             |
| -------- | --------------------------------------------------------------------- |
| `v0.2.0` | Template refactor: `frontend/`, `backend/`, `fullstack/`              |
| `v0.3.0` | Plugin support: `chimera add monitoring`, logging, Redis, etc.        |
| `v0.4.0` | Mix & Match: `chimera init --frontend react --backend php --db mysql` |
| `v0.5.0` | Deploy to Coolify or Docker VPS (`chimera deploy`)                    |
| `v1.0.0` | Stable release with web CLI sync, versioning, and DevOps tools        |

---

## 💡 Coming Soon

- Node.js backend templates
- Python (Flask/FastAPI) templates
- Vue/Svelte frontend stacks
- Redis & RabbitMQ plugin support
- `chimera deploy` (Coolify, Docker VPS)

---

## 🤝 Contributing

Want to contribute a template or core feature?

- Fork the repo
- Follow the [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Use semantic commits (`feat:`, `fix:`, `chore:`)
- Submit a PR

---

## 🧑‍💻 Support & Community

- 🌍 [ChimeraStack Web Platform](https://www.chimerastack.com)
- 🐙 [GitHub Issues](https://github.com/Amirofcodes/ChimeraStack_CLI/issues)
- 🛠️ Docs, changelog, and CLI binaries
- 💬 Feature requests always welcome

---

## 📄 License

MIT License — [LICENSE](LICENSE)

---

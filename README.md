# ChimeraStack CLI

A powerful, template-based development environment manager that simplifies the setup of Docker-based development environments.

## Features

✨ **Ready-to-Use Templates**
- **PHP/Nginx Stacks**
  - MySQL (ports: 8080, 8081)
  - PostgreSQL (ports: 8090, 8091)
  - MariaDB (ports: 8093, 8092)
- **Fullstack Environments**
  - React + PHP + MySQL (ports: 3003, 8094, 8095)

🚀 **Coming Soon**
- Python development environments
- Node.js stacks
- More frontend frameworks
- Additional database options

## Quick Start

### Installation

```bash
pip install chimera-cli
```

### Create a Project

1. Create a new project:
```bash
chimera create my-project
```

2. Choose your template using the interactive arrow-key menu:
```
? Choose a template: (Use arrow keys)
❯ php/nginx/mysql - PHP development environment with Nginx web server and MySQL database
  php/nginx/postgresql - PHP development environment with Nginx web server and PostgreSQL database
  php/nginx/mariadb - PHP development environment with Nginx web server and MariaDB database
  fullstack/react-php/mysql-nginx - Complete fullstack development environment with React, PHP backend, and MySQL database
```

3. Navigate to your project:
```bash
cd my-project
```

4. Start your development environment:
```bash
docker-compose up -d
```

## Key Benefits

- 🎯 **Zero Configuration**: Pre-configured development environments that work out of the box
- 🔄 **Consistent Environments**: Ensure your team uses the same development setup
- 🛠️ **Development Ready**: Hot-reload, debugging tools, and development utilities included
- 🔌 **Port Isolation**: Run multiple projects simultaneously without conflicts
- 🔒 **Secure Defaults**: Security best practices configured by default

## Available Templates

### PHP/Nginx/MySQL Stack
- Web server: localhost:8080
- phpMyAdmin: localhost:8081
- MySQL: localhost:3306

### PHP/Nginx/PostgreSQL Stack
- Web server: localhost:8090
- pgAdmin: localhost:8091
- PostgreSQL: localhost:5432

### PHP/Nginx/MariaDB Stack
- Web server: localhost:8093
- phpMyAdmin: localhost:8092
- MariaDB: localhost:3307

### Fullstack React/PHP/MySQL Stack
- React frontend: localhost:3003
- PHP backend: localhost:8094
- phpMyAdmin: localhost:8095
- MySQL: localhost:3306

## Status

ChimeraStack CLI is under active development. We're continuously adding new templates and features to support more development scenarios. Stay tuned for upcoming templates including Python, Node.js, and additional frontend frameworks.

## Support

For issues, feature requests, or questions:
- Create an issue on GitHub
- Check our documentation
- Join our community discussions

## License

This project is licensed under the MIT License - see the LICENSE file for details.
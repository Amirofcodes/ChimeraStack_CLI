# ChimeraStack CLI

A powerful, template-based development environment manager that simplifies the setup of Docker-based development environments using dynamic port allocation.

## Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose (must be running)
- pip (Python package manager)

## Features

✨ **Ready-to-Use Templates**

- **PHP/Nginx Stacks**
  - MySQL
  - PostgreSQL
  - MariaDB
- **Fullstack Environments**
  - React + PHP + MySQL

🔄 **Dynamic Port Allocation**

- Automatic port assignment to avoid conflicts
- Run multiple projects simultaneously
- Smart port range management:
  - Frontend (React): 3000-3999
  - Backend (PHP/Node): 8000-8999
  - Databases:
    - MySQL: 3300-3399
    - MariaDB: 3400-3499
    - PostgreSQL: 5432-5632
  - Admin Tools:
    - phpMyAdmin: 8081-8180
    - pgAdmin: 8181-8280

🚀 **Coming Soon**

- Python development environments
- Node.js stacks
- More frontend frameworks
- Additional database options

## Quick Start

### Installation

#### Install and run Docker
```bash
# macOS and Windows
# Download and install Docker Desktop from https://www.docker.com/products/docker-desktop/

# Start Docker Desktop from your applications menu

# Ubuntu
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER  # Log out and back in after this
```

#### Install ChimeraStack CLI
### Option 1: Using pip
```bash
pip install chimera-stack-cli
```
### Option 2: Pre-built binaries
Download the appropriate binary for your platform from [GitHub Releases](https://github.com/Amirofcodes/ChimeraStack_CLI/releases)

#### Linux
```bash
wget https://github.com/Amirofcodes/ChimeraStack_CLI/releases/download/v0.1.0/chimera-stack-cli-linux-x64
chmod +x chimera-stack-cli-linux-x64
sudo mv chimera-stack-cli-linux-x64 /usr/local/bin/chimera
```

#### macOS
```bash
curl -L https://github.com/Amirofcodes/ChimeraStack_CLI/releases/download/v0.1.0/chimera-stack-cli-macos -o chimera
chmod +x chimera
sudo mv chimera /usr/local/bin/
```

### Create a Project
1. Create a new project:
```bash
chimera create my-project
```
2. Choose your template using the interactive arrow-key menu:
```
? Choose a category:
❯ PHP Development
 Fullstack Development
? Choose a template:
❯ php/nginx/mysql - PHP development environment with Nginx web server and MySQL database
 php/nginx/postgresql - PHP development environment with Nginx web server and PostgreSQL database
 php/nginx/mariadb - PHP development environment with Nginx web server and MariaDB database
 fullstack/react-php/mysql-nginx - Complete fullstack development environment with React, PHP backend, and MySQL database
```
3. Navigate to your project and start:
```bash
cd my-project
docker-compose up -d
```

## Templates

### PHP Development

#### PHP/Nginx/MySQL Stack

- Web server (Nginx + PHP-FPM)
- MySQL Database
- phpMyAdmin
- Pre-configured for PHP development

#### PHP/Nginx/PostgreSQL Stack

- Web server (Nginx + PHP-FPM)
- PostgreSQL Database
- pgAdmin
- Pre-configured for PHP development

#### PHP/Nginx/MariaDB Stack

- Web server (Nginx + PHP-FPM)
- MariaDB Database
- phpMyAdmin
- Pre-configured for PHP development

### Fullstack Development

#### React/PHP/MySQL Stack

- React Frontend with hot reload
- PHP Backend (Nginx + PHP-FPM)
- MySQL Database
- phpMyAdmin
- Pre-configured API connectivity

## Key Benefits

- 🎯 **Zero Configuration**: Pre-configured development environments that work out of the box
- 🔄 **Dynamic Ports**: Smart port allocation to avoid conflicts between projects
- 🔌 **Project Isolation**: Run multiple projects simultaneously
- 🛠️ **Development Ready**: Hot-reload, debugging tools, and development utilities included
- 🔒 **Secure Defaults**: Security best practices configured by default
- 🔄 **Consistent Environments**: Ensure your team uses the same development setup

## Status

ChimeraStack CLI is under active development. We're continuously adding new templates and features to support more development scenarios.

## Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Support

For issues, feature requests, or questions:

- Create an issue on GitHub
- Check our documentation
- Join our community discussions

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


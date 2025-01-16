# ChimeraStack CLI

A template-based development environment manager that simplifies the setup of Docker-based development environments.

## Features

- Template-based project generation
- Pre-configured development environments
- Cross-platform compatibility (Linux, macOS, Windows)
- Interactive and command-line interfaces
- Supports PHP and Full-stack development environments

## Development Setup

You can develop ChimeraStack CLI either inside a Docker container (recommended) or directly on your local machine.

### Option 1: Development Inside Docker (Recommended)

This is the recommended approach as it ensures a consistent development environment across all platforms.

1. Prerequisites:
   - Docker
   - Docker Compose
   - Git

2. Clone and Setup:
```bash
# Clone the repository
git clone https://github.com/Amirofcodes/ChimeraStack_CLI.git
cd ChimeraStack_CLI

# Start the development container
docker-compose up -d

# Enter the container
docker exec -it chimerastack_cli-cli-dev-1 bash

# Inside container: Install the package in development mode
pip install -e .
```

3. Development Workflow:
   - Code files are synced between your host machine and the container
   - Edit files using your preferred editor on your host machine
   - Run tests and CLI commands inside the container
   - The virtual environment and dependencies are managed inside the container

### Option 2: Local Development

If you prefer developing directly on your machine:

1. Prerequisites:
   - Python 3.11+
   - pip
   - virtualenv or venv

2. Setup:
```bash
# Clone the repository
git clone https://github.com/Amirofcodes/ChimeraStack_CLI.git
cd ChimeraStack_CLI

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies and package in development mode
pip install -r requirements.txt
pip install -e .
```

## Development Commands

Common commands for both development approaches:

```bash
# Run tests
pytest

# Run the CLI
chimera --help

# Create a new project
chimera create <project-name> --template <template-name>
```

## Available Templates

1. PHP/Nginx Configurations:
   - mysql (ports: 172.18.0.x:80xx)
   - postgresql (ports: 172.19.0.x:80xx)
   - mariadb (ports: 172.20.0.x:80xx)

2. Fullstack Configurations:
   - react-php/mysql-nginx (ports: 172.21.0.x:80xx)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT
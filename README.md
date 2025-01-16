# ChimeraStack CLI

A template-based development environment manager that simplifies the setup of Docker-based development environments.

## Features

- Template-based project generation
- Pre-configured development environments
- Cross-platform compatibility (Linux, macOS, Windows)
- Interactive and command-line interfaces
- Supports PHP and Full-stack development environments

## Installation

For development:

```bash
# Clone the repository
git clone https://github.com/Amirofcodes/ChimeraStack_CLI.git
cd ChimeraStack_CLI

# Start the development environment
docker-compose up -d

# Enter the container
docker exec -it chimerastack_cli-dev-1 bash

# Install the package in development mode
pip install -e .
```

## Usage

```bash
# List available templates
chimera list

# Create a new project
chimera create <project-name> --template <template-name>

# Interactive mode
chimera create
```

## Development

```bash
# Run tests
pytest

# Format code
black .

# Check types
mypy .
```

## License

MIT

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
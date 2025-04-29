# .gitignore

```
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# UV
#   Similar to Pipfile.lock, it is generally recommended to include uv.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#uv.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
#poetry.lock

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#pdm.lock
#   pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it
#   in version control.
#   https://pdm.fming.dev/latest/usage/project/#working-with-version-control
.pdm.toml
.pdm-python
.pdm-build/

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/

# PyPI configuration file
.pypirc

codebase.md
.aidigestignore
gitloghistory.txt

```

# build_executables.sh

```sh
#!/bin/bash
# Build executables for all platforms

# Ensure PyInstaller is installed
pip install pyinstaller

# Clean previous PyInstaller builds without removing PyPI packages
if [ -d "build" ]; then
  rm -rf build
fi

if [ -d "dist" ]; then
  # Remove only executable files, not wheel (.whl) or source (.tar.gz) packages
  find dist -type f -not -name "*.whl" -not -name "*.tar.gz" -delete
fi

# Build for current platform
echo "Building executable for $(uname -s)"
pyinstaller chimera-stack-cli.spec

# Create release directory
mkdir -p releases
cp dist/chimera-stack-cli* releases/

echo "Build complete! Executables are in the 'releases' directory."
```

# chimera-stack-cli.spec

```spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/chimera/cli.py'],
    pathex=[],
    binaries=[],
    datas=[('src/chimera/templates', 'chimera/templates')],
    hiddenimports=['questionary.prompts'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='chimera-stack-cli',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

# docker-compose.yml

```yml
services:
  cli-dev:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        # Pass host user's UID/GID to match permissions
        USER_ID: ${UID:-1000}
        GROUP_ID: ${GID:-1000}
    volumes:
      - .:/app
      - ~/.gitconfig:/home/developer/.gitconfig:ro  # For git configuration
      # Mount docker socket to allow CLI to interact with host Docker
      - /var/run/docker.sock:/var/run/docker.sock
    working_dir: /app
    environment:
      - PYTHONPATH=/app
      - PYTHONDONTWRITEBYTECODE=1
      - PYTHONUNBUFFERED=1
    command: /bin/sh -c "while true; do sleep 1; done"  # Keep container running
```

# Dockerfile

```
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    docker.io \
    tree \
    && rm -rf /var/lib/apt/lists/*

# Create and set up a non-root user with specific UID/GID
ARG USER_ID=1000
ARG GROUP_ID=1000
RUN groupadd -g ${GROUP_ID} developer && \
    useradd -u ${USER_ID} -g ${GROUP_ID} -m -s /bin/bash developer && \
    # Add to docker group without creating it (it already exists)
    usermod -aG docker developer

# Create and configure virtual environment
ENV VIRTUAL_ENV=/home/developer/venv
RUN python -m venv $VIRTUAL_ENV && \
    chown -R developer:developer $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install Python dependencies
COPY --chown=developer:developer requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Set up working directory
WORKDIR /app

# Ensure /app is writable by developer
RUN chown developer:developer /app

# Switch to non-root user
USER developer

# Keep container running
CMD ["/bin/sh", "-c", "while true; do sleep 1; done"]
```

# gitloghistory.txt

```txt
commit 19abacb49bdd56bd043138106ceed5e1b9b9242a
Author: Amirofcodes <j.bouddehbine@it-students.fr>
Date:   Thu Mar 13 14:17:12 2025 +0100

    build: add macOS executable version

commit 61958b174a082a42077e4a3e27d9b48ee605a056
Merge: 995c785 ea4563c
Author: Jaouad Bouddehbine <138374972+Amirofcodes@users.noreply.github.com>
Date:   Thu Mar 13 09:38:10 2025 +0100

    build: add PyInstaller configuration and Linux executable
    
    - Add spec file for executable packaging
    - Create build script for generating Linux standalone executable
    - Successfully build Linux x64 binary
    - Preserve PyPI packages during builds
    - Configure proper resource inclusion for templates

commit ea4563c73d966c56ea238600c2b949e11ca12226
Author: Amirofcodes <138374972+Amirofcodes@users.noreply.github.com>
Date:   Thu Mar 13 09:34:51 2025 +0100

    docs: add Docker requirement to README prerequisites
    
    - Add Docker and Docker Compose as required prerequisites
    - Specify that Docker must be running for the CLI to work
    - Add Docker installation instructions for different platforms
    - Update pip install command to use new package name (chimera-stack-cli)

commit 85d540dd088ba72ca9b28c1e13aec19158e5647a
Author: Amirofcodes <138374972+Amirofcodes@users.noreply.github.com>
Date:   Thu Mar 13 09:28:44 2025 +0100

    updated README

commit b8b511fda1cfa460dc064161edeb4f143fff7834
Author: Amirofcodes <138374972+Amirofcodes@users.noreply.github.com>
Date:   Thu Mar 13 07:51:16 2025 +0100

    Add PyPI packaging configuration for chimera-stack-cli
    
    - Updated setup.py with complete metadata, renamed to chimera-stack-cli
    - Created MANIFEST.in to include templates and documentation files
    - Added pyproject.toml with setuptools build configuration
    - Configured package for PyPI distribution with proper classifiers
    - Implemented package discovery with find_packages()
    - Fixed version and dependency specifications
    - Added long_description from README.md for PyPI page

commit 995c7857362ab460fe5d112b270a1361ab3bb0a5
Author: Amirofcodes <j.bouddehbine@it-students.fr>
Date:   Wed Jan 29 08:51:51 2025 +0100

    clean tree

commit 7702f5ee23a3370b0117eb087284a32e8b5259eb
Author: Amirofcodes <j.bouddehbine@it-students.fr>
Date:   Wed Jan 29 08:07:48 2025 +0100

    clean tree

commit 2d8da53e5fe7dc9247d68b1b8a2c954af9216bb3
Merge: 4ae918d f7fcea8
Author: Jaouad Bouddehbine <138374972+Amirofcodes@users.noreply.github.com>
Date:   Wed Jan 29 08:04:22 2025 +0100

    Merge pull request #2 from Amirofcodes/feature/dynamic-port-allocation
    
    Merge pull request #2: Dynamic Port Allocation Implementation
    
    - Implement port management system
    - Add dynamic port allocation to all templates
    - Update frontend environment handling
    - Improve documentation

commit f7fcea85a305834598b040d168f9d88aaac649ee
Author: Amirofcodes <j.bouddehbine@it-students.fr>
Date:   Wed Jan 29 07:56:16 2025 +0100

    Update README

commit 2b23e4e67517e673ec18f8934b5bfeb8ae7e1b60
Author: Amirofcodes <j.bouddehbine@it-students.fr>
Date:   Wed Jan 29 00:45:49 2025 +0100

    feat: complete dynamic port allocation implementation
    
    - Update React frontend to use environment variables correctly
    - Fix environment variable setup in fullstack template
    - Implement proper port handling in all templates
    - Ensure database connectivity and API access with dynamic ports
    - Successfully tested with all four templates
    - Add frontend environment configuration
    - Update Docker Compose configuration for proper port mapping
    
    Templates working with dynamic ports:
    - PHP/Nginx/MySQL
    - PHP/Nginx/PostgreSQL
    - PHP/Nginx/MariaDB
    - Fullstack React/PHP/MySQL

commit 073bd8c9207f3c79ad35cbba01218ea7b892d84d
Author: Amirofcodes <j.bouddehbine@it-students.fr>
Date:   Tue Jan 28 20:40:47 2025 +0100

    fix: improve port detection and allocation
    - Update port scanner to properly detect used ports
    - Optimize port allocator logic
    - Fix port detection in containers' network settings and host config

commit eb41a2dfd98f1c51ac4e3af1de7676856d549bc7
Author: Amirofcodes <j.bouddehbine@it-students.fr>
Date:   Fri Jan 24 09:39:08 2025 +0100

    feat: update mariadb template for dynamic ports
    - Add service type definitions
    - Implement dynamic port allocation
    - Update environment and config files
    - Replace hardcoded ports with variables

commit e5861ae5fd5621368f6d55a2416035ae85114b17
Author: Amirofcodes <j.bouddehbine@it-students.fr>
Date:   Fri Jan 24 09:20:56 2025 +0100

    feat: update postgresql template for dynamic ports
    - Add service type definitions and port ranges
    - Replace hardcoded ports with variables
    - Update configs and environment files
    - Implement dynamic port allocation

commit 374180c992aea2669c087a5688cb9ae3b8e9c599
Author: Amirofcodes <j.bouddehbine@it-students.fr>
Date:   Fri Jan 24 09:05:38 2025 +0100

    feat: update mysql template for dynamic ports
    - Add service type definitions
    - Replace hardcoded ports with variables
    - Update config files for port allocation
    - First template supporting dynamic ports

commit 62def0069af8033ee55e3463ca12fa9133100762
Author: Amirofcodes <j.bouddehbine@it-students.fr>
Date:   Thu Jan 23 10:33:30 2025 +0100

    feat: implement port management system
    - Add port scanner to detect used ports
    - Add port allocator with service ranges
    - Update template manager for dynamic ports
    - Remove hardcoded port assignments

commit 4ae918d9cf25313bb73ef5a441f89848a5eadb98
Merge: fe0e5a0 8132e40
Author: Jaouad Bouddehbine <138374972+Amirofcodes@users.noreply.github.com>
Date:   Fri Jan 17 17:21:25 2025 +0100

    Merge pull request #1 from Amirofcodes/feature/enhanced-cli-organization
    
    Enhanced CLI Organization with Interactive Features

commit 8132e40c82a51d8b55f7adeddb5db4959f4009fe
Author: Amirofcodes <138374972+Amirofcodes@users.noreply.github.com>
Date:   Fri Jan 17 17:16:34 2025 +0100

    fix: template variable substitution in docker config files
    
    - Add YAML file processing for docker-compose.yml and development.yaml
    - Add proper variable substitution in template files
    - Fix volume naming issues and PROJECT_NAME warnings
    - Improve project creation success messaging
    - Add better error handling for file processing

commit b501394f5a0701775c07097287ffa350b44f3dc2
Author: Amirofcodes <138374972+Amirofcodes@users.noreply.github.com>
Date:   Fri Jan 17 16:16:58 2025 +0100

    feat: enhance CLI with interactive template selection
    
    - Add two-step interactive template selection (category -> template)
    - Fix list command with search (-s) and category (-c) filters
    - Improve user feedback and error handling
    - Add ability to cancel selection with Ctrl+C
    - Update command documentation and help messages

commit 7b2b106daa13e92522d0b6d4e0bba2702772f0b7
Author: Amirofcodes <138374972+Amirofcodes@users.noreply.github.com>
Date:   Fri Jan 17 15:20:58 2025 +0100

    fix: update list command to show all available templates
    
    - Use TemplateManager to discover templates dynamically
    - Display all available templates including MySQL, PostgreSQL, MariaDB, and fullstack options
    - Improve table formatting with proper styling
    - Remove hardcoded template entries

commit fe0e5a066026d23a438e525a58e705a9275f3dd6
Author: Amirofcodes <138374972+Amirofcodes@users.noreply.github.com>
Date:   Thu Jan 16 18:34:59 2025 +0100

    docs: comprehensive documentation update
    
    - Separate user and developer documentation
    - Update README with current features and templates
    - Add detailed port mappings and quick start guide
    - Create CONTRIBUTING.md with development guidelines
    - Add template development standards
    - Document port allocation strategy
    - Include commit guidelines and PR process
    - Update project status and upcoming features

commit babe4995976639388e13f81d4952eeb4d0b53473
Author: Amirofcodes <138374972+Amirofcodes@users.noreply.github.com>
Date:   Thu Jan 16 18:20:25 2025 +0100

    feat: add React/PHP/MySQL fullstack template
    
    - Add complete fullstack development environment template with proper port mappings
      (3003, 8094, 8095, 3306)
    - Configure React frontend with development settings and hot reload
    - Set up PHP/Nginx backend with API endpoints
    - Add MySQL database with initialization script
    - Configure development tools (phpMyAdmin)
    - Include proper health checks for all services
    - Set up CORS and proxy configuration for frontend-backend communication
    - Add comprehensive documentation and example components
    - Test full stack deployment and container orchestration

commit 0fc09572de434b912bb4c0e66e4a972c9a5ef55d
Author: Amirofcodes <138374972+Amirofcodes@users.noreply.github.com>
Date:   Thu Jan 16 15:29:53 2025 +0100

    feat: add PostgreSQL template
    
    - Add complete PostgreSQL stack template with proper port mappings (8090, 8091, 5432)
    - Configure PostgreSQL with Alpine-based image and initialization script
    - Add pgAdmin as database management interface
    - Update PHP configuration with PostgreSQL extensions
    - Configure proper database connection strings and PDO settings
    - Maintain consistent template structure with MySQL/MariaDB variants
    - Test template creation and container deployment

commit dd228d7bd6bd73ce0f64a5a8d335198c88c0152b
Author: Amirofcodes <138374972+Amirofcodes@users.noreply.github.com>
Date:   Thu Jan 16 15:05:58 2025 +0100

    feat: add MariaDB template
    
    - Add complete MariaDB stack template with proper port mappings (8093, 8092, 3307)
    - Configure custom MariaDB settings and optimizations
    - Maintain consistent template structure with MySQL variant
    - Ensure proper variable substitution and environment configuration
    - Update template discovery to include MariaDB option
    - Test template creation and container deployment

commit 91dbd2ee56a2f4db900dd886cbf26e67a9b7219a
Author: Amirofcodes <138374972+Amirofcodes@users.noreply.github.com>
Date:   Thu Jan 16 14:12:20 2025 +0100

    feat: implement template processing and project creation
    
    - Add environment variables substitution
    - Process YAML files (docker-compose.yml, development.yaml)
    - Add proper error handling and feedback
    - Support project name variables across all files
    - Clean up target directory on failure
    - Add progress indicators with rich console
    
    Tested and working with php/nginx/mysql template:
    - Variables properly replaced in .env
    - Container names and networks correctly configured
    - All services start successfully

commit ade7a894e237b4252ca4c32c21dde6f27a62b1b6
Author: Amirofcodes <138374972+Amirofcodes@users.noreply.github.com>
Date:   Thu Jan 16 10:56:57 2025 +0100

    Update readme

commit ca41d6ad73ae4e775bb4a57f89d1713afb032ea2
Author: Amirofcodes <138374972+Amirofcodes@users.noreply.github.com>
Date:   Thu Jan 16 10:53:20 2025 +0100

    feat: initial project setup
    
    - Basic project structure
    - Development environment configuration (Docker)
    - Package configuration (setup.py)
    - Project dependencies
    - Basic directory structure for CLI tool

commit e3b5fe054101419bf12e87bf5e1c08a8ac23659c
Author: Jaouad Bouddehbine <138374972+Amirofcodes@users.noreply.github.com>
Date:   Thu Jan 16 09:58:44 2025 +0100

    Initial commit

```

# MANIFEST.in

```in
include LICENSE
include README.md
recursive-include src/chimera/templates *
```

# pyproject.toml

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"
```

# README.md

```md
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
\`\`\`bash
# macOS and Windows
# Download and install Docker Desktop from https://www.docker.com/products/docker-desktop/

# Start Docker Desktop from your applications menu

# Ubuntu
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER  # Log out and back in after this
\`\`\`

#### Install ChimeraStack CLI
\`\`\`bash
pip install chimera-stack-cli
\`\`\`

### Create a Project
1. Create a new project:
\`\`\`bash
chimera create my-project
\`\`\`
2. Choose your template using the interactive arrow-key menu:
\`\`\`
? Choose a category:
❯ PHP Development
 Fullstack Development
? Choose a template:
❯ php/nginx/mysql - PHP development environment with Nginx web server and MySQL database
 php/nginx/postgresql - PHP development environment with Nginx web server and PostgreSQL database
 php/nginx/mariadb - PHP development environment with Nginx web server and MariaDB database
 fullstack/react-php/mysql-nginx - Complete fullstack development environment with React, PHP backend, and MySQL database
\`\`\`
3. Navigate to your project and start:
\`\`\`bash
cd my-project
docker-compose up -d
\`\`\`

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


```

# releases/chimera-stack-cli-linux-x64

This is a binary file of the type: Binary

# releases/chimera-stack-cli-macos

This is a binary file of the type: Binary

# requirements.txt

```txt
click>=8.0.0
python-dotenv>=0.19.0
pyyaml>=6.0.0
colorama>=0.4.4
docker>=6.0.0
rich>=13.0.0
questionary>=2.0.0
```

# setup.py

```py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="chimera-stack-cli",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "click>=8.0.0",
        "python-dotenv>=0.19.0",
        "pyyaml>=6.0.0",
        "colorama>=0.4.4",
        "docker>=6.0.0",
        "rich>=13.0.0",
        "questionary>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "chimera=chimera.cli:main",
        ],
    },
    python_requires=">=3.8",
    author="Amir",
    author_email="amirofcodes@github.com",
    description="A template-based development environment manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Amirofcodes/ChimeraStack_CLI",
    project_urls={
        "Bug Tracker": "https://github.com/Amirofcodes/ChimeraStack_CLI/issues",
        "Documentation": "https://github.com/Amirofcodes/ChimeraStack_CLI#readme",
        "Source Code": "https://github.com/Amirofcodes/ChimeraStack_CLI",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
```

# src/chimera_cli.egg-info/dependency_links.txt

```txt


```

# src/chimera_cli.egg-info/entry_points.txt

```txt
[console_scripts]
chimera = chimera.cli:main

```

# src/chimera_cli.egg-info/PKG-INFO

```
Metadata-Version: 2.2
Name: chimera-cli
Version: 0.1.0
Summary: A template-based development environment manager
Home-page: https://github.com/Amirofcodes/ChimeraStack_CLI
Author: Amir
Author-email: amirofcodes@github.com
Classifier: Development Status :: 3 - Alpha
Classifier: Intended Audience :: Developers
Classifier: License :: OSI Approved :: MIT License
Classifier: Programming Language :: Python :: 3
Classifier: Programming Language :: Python :: 3.8
Classifier: Programming Language :: Python :: 3.9
Classifier: Programming Language :: Python :: 3.10
Classifier: Programming Language :: Python :: 3.11
Requires-Python: >=3.8
Description-Content-Type: text/markdown
License-File: LICENSE
Requires-Dist: click>=8.0.0
Requires-Dist: python-dotenv>=0.19.0
Requires-Dist: pyyaml>=6.0.0
Requires-Dist: colorama>=0.4.4
Requires-Dist: docker>=6.0.0
Requires-Dist: rich>=13.0.0
Requires-Dist: questionary>=2.0.0
Dynamic: author
Dynamic: author-email
Dynamic: classifier
Dynamic: description
Dynamic: description-content-type
Dynamic: home-page
Dynamic: requires-dist
Dynamic: requires-python
Dynamic: summary

# ChimeraStack CLI

A powerful, template-based development environment manager that simplifies the setup of Docker-based development environments using dynamic port allocation.

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

\`\`\`bash
pip install chimera-cli
\`\`\`

### Create a Project

1. Create a new project:

\`\`\`bash
chimera create my-project
\`\`\`

2. Choose your template using the interactive arrow-key menu:

\`\`\`
? Choose a category:
❯ PHP Development
  Fullstack Development

? Choose a template:
❯ php/nginx/mysql - PHP development environment with Nginx web server and MySQL database
  php/nginx/postgresql - PHP development environment with Nginx web server and PostgreSQL database
  php/nginx/mariadb - PHP development environment with Nginx web server and MariaDB database
  fullstack/react-php/mysql-nginx - Complete fullstack development environment with React, PHP backend, and MySQL database
\`\`\`

3. Navigate to your project and start:

\`\`\`bash
cd my-project
docker-compose up -d
\`\`\`

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

```

# src/chimera_cli.egg-info/requires.txt

```txt
click>=8.0.0
python-dotenv>=0.19.0
pyyaml>=6.0.0
colorama>=0.4.4
docker>=6.0.0
rich>=13.0.0
questionary>=2.0.0

```

# src/chimera_cli.egg-info/SOURCES.txt

```txt
LICENSE
README.md
setup.py
src/chimera/__init__.py
src/chimera/cli.py
src/chimera/commands/__init__.py
src/chimera/commands/create.py
src/chimera/commands/list.py
src/chimera/core/__init__.py
src/chimera/core/port_allocator.py
src/chimera/core/port_scanner.py
src/chimera/core/template_manager.py
src/chimera/templates/__init__.py
src/chimera_cli.egg-info/PKG-INFO
src/chimera_cli.egg-info/SOURCES.txt
src/chimera_cli.egg-info/dependency_links.txt
src/chimera_cli.egg-info/entry_points.txt
src/chimera_cli.egg-info/requires.txt
src/chimera_cli.egg-info/top_level.txt
```

# src/chimera_cli.egg-info/top_level.txt

```txt
chimera

```

# src/chimera/__init__.py

```py
"""
ChimeraStack CLI - A template-based development environment manager.
"""

__version__ = "0.1.0"
__author__ = "Amirofcodes"
__email__ = "amirofcodes20@gmail.com"

```

# src/chimera/cli.py

```py
"""
ChimeraStack CLI entry point.
"""
import click
from rich.console import Console
from rich.traceback import install
import questionary

from chimera import __version__
from chimera.commands.create import create_command
from chimera.commands.list import list_command
from chimera.core import TemplateManager

# Set up rich error handling
install(show_locals=True)
console = Console()

@click.group()
@click.version_option(version=__version__)
def cli():
    """ChimeraStack CLI - A template-based development environment manager.
    
    This tool helps you quickly set up development environments using pre-configured templates.
    """
    pass

@cli.command()
@click.argument('name')
@click.option('--template', '-t', help='Template to use for the project (e.g., php/nginx/mysql)')
def create(name: str, template: str | None = None):
    """Create a new project from a template.
    
    Examples:
    \b
    chimera create myproject                    # Interactive mode
    chimera create myproject -t php/nginx/mysql # Direct template selection
    """
    create_command(name, template)

@cli.command()
@click.option('--search', '-s', help='Search for templates (e.g., mysql, postgresql)')
@click.option('--category', '-c', help='Filter by category (e.g., "PHP Development", "Fullstack Development")')
def list(search: str = None, category: str = None):
    """List available templates.
    
    Examples:
    \b
    chimera list                                  # List all templates
    chimera list -s mysql                         # Search for templates containing "mysql"
    chimera list -c "PHP Development"             # List PHP templates
    chimera list -c "Fullstack Development"       # List fullstack templates
    """
    list_command(search, category)

def main():
    try:
        cli()
    except Exception as e:
        console.print_exception()
        exit(1)

if __name__ == '__main__':
    main()

```

# src/chimera/commands/__init__.py

```py
"""
Command implementations for the ChimeraStack CLI.
"""

from .create import create_command
from .list import list_command

__all__ = ['create_command', 'list_command']

```

# src/chimera/commands/create.py

```py
"""
Implementation of the create command.
"""
import click
import questionary
from rich.console import Console
from chimera.core import TemplateManager

console = Console()

def create_command(name: str, template: str | None = None) -> None:
    """Create a new project from a template."""
    try:
        template_manager = TemplateManager()
        
        if not template:
            # Get all templates first
            templates_by_category = template_manager.get_templates_by_category()
            
            # Step 1: Select category
            categories = list(templates_by_category.keys())
            category = questionary.select(
                "Choose a category:",
                choices=categories,
                use_indicator=True
            ).ask()
            
            if not category:
                console.print("[red]Category selection cancelled[/]")
                return

            # Step 2: Select template from category
            templates = templates_by_category[category]
            choices = [
                {
                    'name': f"{t['id']} - {t['description']}",
                    'value': t['id']
                }
                for t in templates
            ]
            
            selected = questionary.select(
                "Choose a template:",
                choices=choices,
                use_indicator=True
            ).ask()
            
            if not selected:
                console.print("[red]Template selection cancelled[/]")
                return
                
            template = selected

        # Create the project
        if template:
            console.print(f"Creating project [bold blue]{name}[/] using template [bold green]{template}[/]")
            template_manager.create_project(template, name)
        else:
            console.print("[red]No template selected[/]")
            
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")
        raise

```

# src/chimera/commands/list.py

```py
"""
Implementation of the list command.
"""
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from chimera.core import TemplateManager

console = Console()

def list_command(search: str = None, category: str = None) -> None:
    """List all available templates."""
    try:
        template_manager = TemplateManager()
        
        if search:
            templates = template_manager.search_templates(search)
            _display_template_list("Search Results", templates)
            return
            
        if category:
            templates_by_category = template_manager.get_templates_by_category()
            if category in templates_by_category:
                _display_template_list(f"Category: {category}", templates_by_category[category])
            else:
                console.print(f"[yellow]No templates found for category: {category}[/]")
            return
        
        # Display all templates grouped by category
        templates_by_category = template_manager.get_templates_by_category()
        for category, templates in templates_by_category.items():
            _display_template_list(category, templates)
            console.print()  # Add spacing between categories
            
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")
        raise

def _display_template_list(title: str, templates: list) -> None:
    """Display a list of templates in a formatted table."""
    table = Table(title=title, show_header=True)
    table.add_column("Template", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Tags", style="green")
    
    for template in templates:
        tags = ", ".join(template.get('tags', []))
        table.add_row(
            template['id'],
            template.get('description', ''),
            tags
        )
    
    console.print(Panel(table))

```

# src/chimera/core/__init__.py

```py
# src/chimera/core/__init__.py

from .template_manager import TemplateManager
from .port_scanner import PortScanner
from .port_allocator import PortAllocator

__all__ = ['TemplateManager', 'PortScanner', 'PortAllocator']
```

# src/chimera/core/port_allocator.py

```py
"""
Port allocation management for ChimeraStack CLI
"""
from typing import Dict, Optional, Set
from dataclasses import dataclass
from .port_scanner import PortScanner

@dataclass
class PortRange:
    start: int
    end: int
    allocated: Set[int] = None

    def __post_init__(self):
        if self.allocated is None:
            self.allocated = set()

class PortAllocator:
    def __init__(self):
        self.scanner = PortScanner()
        self.ranges = {
            'frontend': {
                'react': PortRange(3000, 3999),
                'vue': PortRange(4000, 4999)
            },
            'backend': {
                'php': PortRange(8000, 8999),
                'node': PortRange(9000, 9999)
            },
            'database': {
                'mysql': PortRange(3300, 3399),
                'mariadb': PortRange(3400, 3499),
                'postgres': PortRange(5432, 5632)
            },
            'admin': {
                'phpmyadmin': PortRange(8081, 8180),
                'pgadmin': PortRange(8181, 8280)
            }
        }

    def get_available_port(self, service_type: str, service_name: str) -> Optional[int]:
        if service_type not in self.ranges:
            return None

        ranges = self.ranges[service_type]
        used_ports = self.scanner.scan()['ports']

        # Find specific range for service
        port_range = None
        for key, range_obj in ranges.items():
            if key in service_name.lower():
                port_range = range_obj
                break

        if port_range is None:
            port_range = next(iter(ranges.values()))

        # Find first available port in range
        for port in range(port_range.start, port_range.end + 1):
            if port not in used_ports:
                return port

        return None

    def release_port(self, port: int) -> None:
        for ranges in self.ranges.values():
            for port_range in ranges.values():
                if port_range.start <= port <= port_range.end:
                    port_range.allocated.discard(port)
                    return
```

# src/chimera/core/port_scanner.py

```py
"""
Docker port and network scanner for ChimeraStack CLI
"""
import docker
from typing import Dict, Set, List

class PortScanner:
    def __init__(self):
        self.docker_client = docker.from_env()
        self.used_ports: Set[int] = set()
        self.container_names: Set[str] = set()
    
    def scan(self) -> Dict[str, Set]:
        self.used_ports.clear()
        self.container_names.clear()

        containers = self.docker_client.containers.list(all=True)
        for container in containers:
            config = container.attrs
            ports = config['NetworkSettings']['Ports'] or {}
            bindings = config['HostConfig']['PortBindings'] or {}
            
            for ports_map in [ports, bindings]:
                for binding in ports_map.values():
                    if binding and binding[0].get('HostPort'):
                        self.used_ports.add(int(binding[0]['HostPort']))
            
            self.container_names.add(container.name)

        return {
            'ports': self.used_ports,
            'names': self.container_names
        }

    def is_port_used(self, port: int) -> bool:
        return port in self.used_ports

    def get_project_containers(self, project_prefix: str) -> List[str]:
        return [name for name in self.container_names 
                if name.startswith(project_prefix)]
```

# src/chimera/core/template_manager.py

```py
"""
Template management system for ChimeraStack CLI.
"""
from pathlib import Path
from typing import Dict, List
import shutil
import yaml
import docker
from rich.console import Console
from .port_scanner import PortScanner
from .port_allocator import PortAllocator

console = Console()

class TemplateManager:
    def __init__(self, templates_dir: Path | str = None):
        if templates_dir is None:
            templates_dir = Path(__file__).parent.parent / 'templates'
        self.templates_dir = Path(templates_dir)
        self.port_allocator = PortAllocator()
        self.port_scanner = PortScanner()
    
    def get_available_templates(self) -> List[Dict[str, str]]:
        """Get list of available templates with metadata."""
        templates = []
        for template_path in self.templates_dir.glob('**/*'):
            if template_path.is_dir() and self._is_valid_template(template_path):
                template_info = self._get_template_info(template_path)
                if template_info:
                    templates.append(template_info)
        return templates

    def get_templates_by_category(self) -> Dict[str, List[Dict[str, str]]]:
        """Get templates grouped by category/type."""
        templates = self.get_available_templates()
        grouped = {}
        for template in templates:
            category = template.get('type', 'Other')
            if category not in grouped:
                grouped[category] = []
            grouped[category].append(template)
        return grouped

    def search_templates(self, query: str) -> List[Dict[str, str]]:
        """Search templates by name, type, or description."""
        templates = self.get_available_templates()
        query = query.lower()
        
        return [
            template for template in templates
            if query in template.get('id', '').lower()
            or query in template.get('type', '').lower()
            or query in template.get('description', '').lower()
            or any(tag.lower() == query for tag in template.get('tags', []))
        ]

    def _is_valid_template(self, path: Path) -> bool:
        """Check if directory contains a valid template."""
        return (
            (path / 'docker-compose.yml').exists() and
            (path / 'template.yaml').exists()
        )

    def _get_template_info(self, path: Path) -> Dict[str, str] | None:
        """Get template metadata from template.yaml."""
        try:
            config_path = path / 'template.yaml'
            if not config_path.exists():
                return None
                
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                
            return {
                'id': str(path.relative_to(self.templates_dir)),
                'name': config.get('name', ''),
                'type': config.get('type', ''),
                'description': config.get('description', ''),
                'tags': config.get('tags', []),
                'path': str(path)
            }
        except Exception as e:
            console.print(f"[red]Error reading template config from {path}: {str(e)}")
            return None

    def create_project(self, template_id: str, project_name: str, target_dir: Path | str = None) -> bool:
        try:
            template_path = self.templates_dir / template_id
            if not self._is_valid_template(template_path):
                console.print(f"[red]Error:[/] Template {template_id} not found or invalid")
                return False

            if target_dir is None:
                target_dir = Path.cwd() / project_name
            else:
                target_dir = Path(target_dir) / project_name

            if target_dir.exists():
                console.print(f"[red]Error:[/] Directory {target_dir} already exists")
                return False

            # Load template configuration
            with open(template_path / 'template.yaml') as f:
                template_config = yaml.safe_load(f)

            # Allocate ports for services
            port_mappings = self._allocate_service_ports(template_config)
            if not port_mappings:
                console.print("[red]Error:[/] Failed to allocate required ports")
                return False

            # Copy template files
            shutil.copytree(template_path, target_dir, ignore=shutil.ignore_patterns('template.yaml'))

            # Define variables for substitution
            variables = {
                'PROJECT_NAME': project_name,
                'DB_DATABASE': project_name,
                'DB_USERNAME': project_name,
                'DB_PASSWORD': 'secret',
                'DB_ROOT_PASSWORD': 'rootsecret',
                **{f"{k.upper()}_PORT": str(v) for k, v in port_mappings.items()}
            }

            # Process files
            self._process_project_files(target_dir, variables)
            
            # Display allocated ports
            self._print_port_mappings(port_mappings)
            
            return True

        except Exception as e:
            console.print(f"[red]Error creating project:[/] {str(e)}")
            if 'target_dir' in locals() and target_dir.exists():
                shutil.rmtree(target_dir)
            return False

    def _allocate_service_ports(self, template_config: dict) -> Dict[str, int]:
        port_mappings = {}
        services = template_config.get('services', {})
        
        # Handle different service types
        for service_name, service_config in services.items():
            port_type = service_config.get('port_type')
            if not port_type:
                continue

            # Get port based on service type and variant
            service_variant = service_config.get('service_variant', '')
            port = self.port_allocator.get_available_port(port_type, service_variant or service_name)
            
            if port is None:
                return {}
                
            port_mappings[service_name] = port

        return port_mappings

    def _process_project_files(self, project_dir: Path, variables: dict) -> None:
        # Process environment file
        env_file = project_dir / '.env.example'
        if env_file.exists():
            self._process_env_file(env_file, project_dir / '.env', variables)

        # Process docker-compose.yml
        compose_file = project_dir / 'docker-compose.yml'
        if compose_file.exists():
            self._process_yaml_file(compose_file, variables, is_compose=True)

        # Process development.yaml
        dev_config = project_dir / 'config/development.yaml'
        if dev_config.exists():
            self._process_yaml_file(dev_config, variables)
    
    def _process_yaml_file(self, file_path: Path, variables: dict, is_compose: bool = False) -> None:
        try:
            with open(file_path) as f:
                content = yaml.safe_load(f)
                
            if is_compose:
                project_name = variables['PROJECT_NAME']
                
                # Update services
                for service_name, service in content.get('services', {}).items():
                    service['container_name'] = f"{project_name}-{service_name}"
                    
                    # Update ports if defined
                    if service_name in variables:
                        port_key = f"{service_name.upper()}_PORT"
                        if 'ports' in service and port_key in variables:
                            service['ports'] = [f"{variables[port_key]}:{service['ports'][0].split(':')[1]}"]

                # Update networks
                if 'networks' in content:
                    for network in content['networks'].values():
                        network['name'] = f"{project_name}_network"

                # Update volumes
                if 'volumes' in content:
                    for volume in content['volumes'].values():
                        if isinstance(volume, dict) and 'name' in volume:
                            volume['name'] = f"{project_name}_{volume['name']}"

            # Replace variables
            content_str = yaml.dump(content)
            for key, value in variables.items():
                content_str = content_str.replace(f"${{{key}}}", str(value))
                content_str = content_str.replace(f"${key}", str(value))

            with open(file_path, 'w') as f:
                f.write(content_str)

            console.print(f"[green]✓[/] Processed: {file_path}")
        except Exception as e:
            console.print(f"[red]Error processing {file_path}:[/] {str(e)}")
            raise

    def _process_env_file(self, src_path: Path, dest_path: Path, variables: dict) -> None:
        """Process environment file, replacing variables."""
        try:
            with open(src_path) as f:
                content = f.read()
            
            for key, value in variables.items():
                content = content.replace(f"${{{key}}}", str(value))
                content = content.replace(f"${key}", str(value))
            
            with open(dest_path, 'w') as f:
                f.write(content)
                
            console.print(f"[green]✓[/] Environment file processed: {dest_path}")
        except Exception as e:
            console.print(f"[red]Error processing environment file:[/] {str(e)}")
            raise

    def _print_port_mappings(self, port_mappings: Dict[str, int]) -> None:
        console.print("\n[bold]Port Allocations:[/]")
        for service, port in port_mappings.items():
            console.print(f"  {service}: [cyan]localhost:{port}[/]")

```

# src/chimera/templates/__init__.py

```py

```

# src/chimera/templates/fullstack/react-php/mysql-nginx/backend/docker-entrypoint.sh

```sh
#!/bin/sh
set -e

# Create required directories and set permissions
mkdir -p /var/log/nginx
mkdir -p /var/log/php
touch /var/log/php/fpm-error.log
chown -R www-data:www-data /var/log/nginx
chown -R www-data:www-data /var/log/php
chmod 755 /var/log/nginx
chmod 755 /var/log/php

# Start PHP-FPM
php-fpm -D

# Wait a moment for PHP-FPM to be ready
sleep 2

# Start Nginx in foreground
nginx -g "daemon off;"

```

# src/chimera/templates/fullstack/react-php/mysql-nginx/backend/Dockerfile

```
FROM php:8.1-fpm

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nginx \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    zip \
    unzip \
    curl \
    && docker-php-ext-install pdo_mysql \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install -j$(nproc) gd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configure PHP and PHP-FPM
RUN mv "$PHP_INI_DIR/php.ini-development" "$PHP_INI_DIR/php.ini"

# Create necessary directories for logs
RUN mkdir -p /var/log/nginx \
    && mkdir -p /var/log/php \
    && touch /var/log/nginx/error.log \
    && touch /var/log/nginx/access.log \
    && touch /var/log/php/fpm-error.log \
    && chown -R www-data:www-data /var/log/nginx \
    && chown -R www-data:www-data /var/log/php \
    && chmod 755 /var/log/nginx \
    && chmod 755 /var/log/php

WORKDIR /var/www/html

# Copy configuration files
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
COPY php/www.conf /usr/local/etc/php-fpm.d/www.conf
COPY php/custom.ini /usr/local/etc/php/conf.d/custom.ini
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Copy source code
COPY src/ /var/www/html/

EXPOSE 80

ENTRYPOINT ["docker-entrypoint.sh"]

```

# src/chimera/templates/fullstack/react-php/mysql-nginx/backend/nginx/default.conf

```conf
server {
    listen 80;
    server_name localhost;
    root /var/www/html;
    index index.php;

    location /api {
        # CORS headers - use actual frontend port, not variable
        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' '*' always;
        add_header 'Access-Control-Allow-Credentials' 'true' always;

        # Handle preflight requests
        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' '*' always;
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS' always;
            add_header 'Access-Control-Allow-Headers' '*' always;
            add_header 'Access-Control-Allow-Credentials' 'true' always;
            add_header 'Content-Type' 'text/plain charset=UTF-8';
            add_header 'Content-Length' 0;
            return 204;
        }

        try_files $uri $uri/ /api.php?$args;
    }

    location ~ \.php$ {
        fastcgi_split_path_info ^(.+\.php)(/.+)$;
        fastcgi_pass 127.0.0.1:9000;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param PATH_INFO $fastcgi_path_info;
    }

    error_log /var/log/nginx/error.log;
    access_log /var/log/nginx/access.log;
}
```

# src/chimera/templates/fullstack/react-php/mysql-nginx/backend/php/custom.ini

```ini
[PHP]
; Development settings
display_errors = On
display_startup_errors = On
error_reporting = E_ALL
log_errors = On
error_log = /var/log/php/errors.log

; Performance settings
memory_limit = 256M
max_execution_time = 30
max_input_time = 60
post_max_size = 8M
upload_max_filesize = 2M

; Security settings
expose_php = Off
session.cookie_httponly = 1
session.use_only_cookies = 1
session.cookie_secure = 1

```

# src/chimera/templates/fullstack/react-php/mysql-nginx/backend/php/www.conf

```conf
[www]
user = www-data
group = www-data
listen = 127.0.0.1:9000
pm = dynamic
pm.max_children = 5
pm.start_servers = 2
pm.min_spare_servers = 1
pm.max_spare_servers = 3
catch_workers_output = yes
php_admin_value[error_log] = /var/log/php/fpm-error.log
php_admin_flag[log_errors] = on

```

# src/chimera/templates/fullstack/react-php/mysql-nginx/backend/src/api.php

```php
<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Get the request path
$request = $_SERVER['REQUEST_URI'];
$path = parse_url($request, PHP_URL_PATH);

// Remove /api prefix
$path = str_replace('/api/', '', $path);

switch ($path) {
    case 'db-status':
        checkDatabaseStatus();
        break;
    default:
        echo json_encode(['message' => 'Welcome to the API!']);
        break;
}

function checkDatabaseStatus()
{
    try {
        $host = getenv('MYSQL_HOST');
        $port = getenv('MYSQL_PORT');
        $db   = getenv('MYSQL_DB');
        $user = getenv('MYSQL_USER');
        $pass = getenv('MYSQL_PASSWORD');

        $dsn = "mysql:host=$host;port=$port;dbname=$db";
        $pdo = new PDO($dsn, $user, $pass);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        // Get MySQL version
        $stmt = $pdo->query("SELECT VERSION() AS version");
        $version = $stmt->fetch(PDO::FETCH_ASSOC)['version'];

        echo json_encode([
            'success' => true,
            'version' => $version,
            'message' => 'Database connection successful',
            'config' => [
                'host' => $host,
                'port' => $port,
                'database' => $db,
                'user' => $user
            ]
        ]);
    } catch (PDOException $e) {
        http_response_code(500);
        echo json_encode([
            'success' => false,
            'error' => $e->getMessage(),
            'config' => [
                'host' => $host,
                'port' => $port,
                'database' => $db,
                'user' => $user
            ]
        ]);
    }
}

```

# src/chimera/templates/fullstack/react-php/mysql-nginx/backend/src/index.php

```php
<?php
echo "Welcome to the backend!";

```

# src/chimera/templates/fullstack/react-php/mysql-nginx/config/development.yaml

```yaml
project:
  name: ${PROJECT_NAME}
  language: fullstack
  framework: react-php
  environment: development

services:
  frontend:
    build:
      context: ./frontend
    ports:
      - ${FRONTEND_PORT}:3000
    environment:
      REACT_APP_API_URL: http://localhost:${BACKEND_PORT}

  backend:
    build:
      context: ./backend
    ports:
      - ${BACKEND_PORT}:80
    environment:
      MYSQL_HOST: ${MYSQL_HOST}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
      MYSQL_DB: ${MYSQL_DB}

  mysql:
    ports:
      - ${MYSQL_PORT}:3306
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DB}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}

  phpmyadmin:
    ports:
      - ${PHPMYADMIN_PORT}:80
    environment:
      PMA_HOST: ${MYSQL_HOST}
      PMA_USER: ${MYSQL_USER}
      PMA_PASSWORD: ${MYSQL_PASSWORD}

```

# src/chimera/templates/fullstack/react-php/mysql-nginx/database/init/init.sql

```sql
-- Create developer user
CREATE USER IF NOT EXISTS 'developer'@'%' IDENTIFIED BY 'devpassword';
GRANT ALL PRIVILEGES ON exampledb.* TO 'developer'@'%';
FLUSH PRIVILEGES;

-- Create tables
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial data
INSERT INTO users (name, email) VALUES ('John Doe', 'john@example.com');

```

# src/chimera/templates/fullstack/react-php/mysql-nginx/docker-compose.yml

```yml
services:
  frontend:
    build:
      context: ./frontend
    ports:
      - "${FRONTEND_PORT}:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    networks:
      - app_network
    environment:
      - REACT_APP_PORT=${FRONTEND_PORT}
      - REACT_APP_BACKEND_PORT=${BACKEND_PORT}
      - REACT_APP_MYSQL_PORT=${MYSQL_PORT}
      - REACT_APP_PHPMYADMIN_PORT=${PHPMYADMIN_PORT}
      - REACT_APP_API_URL=http://localhost:${BACKEND_PORT}
      - WDS_SOCKET_HOST=0.0.0.0
      - WDS_SOCKET_PORT=${FRONTEND_PORT}
      - CHOKIDAR_USEPOLLING=true
      - WATCHPACK_POLLING=true
    depends_on:
      - backend

  backend:
    build:
      context: ./backend
    ports:
      - "${BACKEND_PORT}:80"
    volumes:
      - ./backend/src:/var/www/html
      - ./backend/logs:/var/log
    networks:
      - app_network
    environment:
      - MYSQL_HOST=mysql
      - MYSQL_PORT=3306
      - MYSQL_USER=${MYSQL_USER}
      - MYSQL_PASSWORD=${MYSQL_PASSWORD}
      - MYSQL_DB=${MYSQL_DB}
    depends_on:
      - mysql

  mysql:
    image: mysql:8.0
    ports:
      - "${MYSQL_PORT}:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./database/init:/docker-entrypoint-initdb.d
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DB}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    networks:
      - app_network

  phpmyadmin:
    image: phpmyadmin/phpmyadmin
    ports:
      - "${PHPMYADMIN_PORT}:80"
    environment:
      PMA_HOST: mysql
      PMA_USER: ${MYSQL_USER}
      PMA_PASSWORD: ${MYSQL_PASSWORD}
    networks:
      - app_network
    depends_on:
      - mysql

networks:
  app_network:
    driver: bridge

volumes:
  mysql_data:
    driver: local
```

# src/chimera/templates/fullstack/react-php/mysql-nginx/frontend/.dockerignore

```
node_modules
build
.git
*.log
.env
.env.local
.DS_Store

```

# src/chimera/templates/fullstack/react-php/mysql-nginx/frontend/Dockerfile

```
FROM node:18-alpine

WORKDIR /app

# Install curl for healthcheck
RUN apk add --no-cache curl

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy app source
COPY . .

# Environment variables
ENV NODE_ENV=development
ENV WATCHPACK_POLLING=true
ENV WDS_SOCKET_PORT=0

# Expose port
EXPOSE 3000

# Start development server
CMD ["npm", "start", "--", "--host", "0.0.0.0"]

```

# src/chimera/templates/fullstack/react-php/mysql-nginx/frontend/package.json

```json
{
  "name": "frontend",
  "version": "1.0.0",
  "main": "index.js",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "axios": "^1.6.2",
    "@babel/plugin-proposal-private-property-in-object": "^7.21.11",
    "http-proxy-middleware": "^2.0.6"
  },
  "scripts": {
    "start": "WATCHPACK_POLLING=true react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}

```

# src/chimera/templates/fullstack/react-php/mysql-nginx/frontend/public/index.html

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>React App</title>
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>

```

# src/chimera/templates/fullstack/react-php/mysql-nginx/frontend/src/api.js

```js
import axios from "axios";

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || `http://localhost:${process.env.BACKEND_PORT}/api`,
});

export default api;
```

# src/chimera/templates/fullstack/react-php/mysql-nginx/frontend/src/App.css

```css
.app-container {
    padding: 20px;
    font-family: Arial, sans-serif;
  }
  
  .stack-overview {
    margin: 20px 0;
  }
  
  .status-table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
  }
  
  .status-table th,
  .status-table td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }
  
  .status-table th {
    background-color: #f5f5f5;
  }
  
  .status-indicator {
    padding: 10px;
    border-radius: 5px;
    margin: 10px 0;
  }
  
  .status-success {
    background-color: #d4edda;
    color: #155724;
  }
  
  .status-error {
    background-color: #f8d7da;
    color: #721c24;
  }
  
  .quick-links {
    margin: 20px 0;
  }
  
  .quick-links ul {
    list-style: none;
    padding: 0;
  }
  
  .quick-links li {
    margin: 10px 0;
  }
  
  .quick-links a {
    color: #007bff;
    text-decoration: none;
  }
  
  .quick-links a:hover {
    text-decoration: underline;
  }

```

# src/chimera/templates/fullstack/react-php/mysql-nginx/frontend/src/App.js

```js
import React, { useState, useEffect } from "react";
import "./App.css";

const API_URL = process.env.REACT_APP_API_URL;
const FRONTEND_PORT = process.env.REACT_APP_PORT;
const BACKEND_PORT = process.env.REACT_APP_BACKEND_PORT;
const PHPMYADMIN_PORT = process.env.REACT_APP_PHPMYADMIN_PORT;
const MYSQL_PORT = process.env.REACT_APP_MYSQL_PORT;

const App = () => {
  const [dbStatus, setDbStatus] = useState("Checking...");
  const [dbVersion, setDbVersion] = useState("");
  const [dbConfig, setDbConfig] = useState(null);

  useEffect(() => {
    const checkDatabaseStatus = async () => {
      try {
        const response = await fetch(`${API_URL}/api/db-status`, {
          method: "GET",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
          credentials: "omit",
        });

        const data = await response.json();
        if (data.success) {
          setDbStatus("Connected");
          setDbVersion(data.version);
          setDbConfig(data.config);
        } else {
          setDbStatus(`Error: ${data.error}`);
          setDbConfig(data.config);
        }
      } catch (error) {
        console.error("Error:", error);
        setDbStatus("Error connecting to database");
      }
    };

    checkDatabaseStatus();
  }, []);

  return (
    <div className="app-container">
      <h1>ChimeraStack React + PHP Development Environment</h1>

      <section className="stack-overview">
        <h2>Stack Overview</h2>
        <table className="status-table">
          <thead>
            <tr>
              <th>Component</th>
              <th>Details</th>
              <th>Access</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Frontend</td>
              <td>React</td>
              <td>localhost:{FRONTEND_PORT}</td>
            </tr>
            <tr>
              <td>Backend API</td>
              <td>Nginx + PHP-FPM</td>
              <td>localhost:{BACKEND_PORT}</td>
            </tr>
            <tr>
              <td>Database</td>
              <td>MySQL</td>
              <td>localhost:{MYSQL_PORT}</td>
            </tr>
            <tr>
              <td>Database GUI</td>
              <td>phpMyAdmin</td>
              <td>
                <a
                  href={`http://localhost:${PHPMYADMIN_PORT}`}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  localhost:{PHPMYADMIN_PORT}
                </a>
              </td>
            </tr>
          </tbody>
        </table>
      </section>

      <section className="quick-links">
        <h2>Quick Links</h2>
        <ul>
          <li>
            <a
              href={`${API_URL}/api`}
              target="_blank"
              rel="noopener noreferrer"
            >
              API Status
            </a>
          </li>
          <li>
            <a
              href={`http://localhost:${PHPMYADMIN_PORT}`}
              target="_blank"
              rel="noopener noreferrer"
            >
              phpMyAdmin
            </a>
          </li>
        </ul>
      </section>

      <section>
        <h2>Database Connection Status</h2>
        <div
          className={`status-indicator ${
            dbStatus === "Connected" ? "status-success" : "status-error"
          }`}
        >
          {dbStatus === "Connected" ? (
            <>
              ✓ Connected to MySQL Server {dbVersion}
              <br />
              Database: {dbConfig?.database}
              <br />
              User: {dbConfig?.user}
            </>
          ) : (
            <>
              ✖ {dbStatus}
              {dbConfig && (
                <div className="config-debug">
                  <pre>{JSON.stringify(dbConfig, null, 2)}</pre>
                </div>
              )}
            </>
          )}
        </div>
      </section>
    </div>
  );
};

export default App;
```

# src/chimera/templates/fullstack/react-php/mysql-nginx/frontend/src/index.js

```js
import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';

const container = document.getElementById('root');
const root = createRoot(container);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

```

# src/chimera/templates/fullstack/react-php/mysql-nginx/frontend/src/setupProxy.js

```js
const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = function (app) {
  app.use(
    "/api",
    createProxyMiddleware({
      target: process.env.REACT_APP_BACKEND_URL || `http://localhost:${process.env.BACKEND_PORT}`,
      pathRewrite: {
        "^/api": "/api",
      },
      changeOrigin: true,
    })
  );
};
```

# src/chimera/templates/fullstack/react-php/mysql-nginx/template.yaml

```yaml
name: "React/PHP/MySQL Fullstack Stack"
type: "Fullstack Development"
description: "Complete fullstack development environment with React, PHP backend, and MySQL database"
version: "1.0"
author: "ChimeraStack"
tags: ["react", "php", "mysql", "fullstack"]

services:
  frontend:
    port_type: frontend
    service_variant: react
  backend:
    port_type: backend
    service_variant: php-nginx
  mysql:
    port_type: database
    service_variant: mysql
  phpmyadmin:
    port_type: admin
    service_variant: phpmyadmin

env_template: ".env.example"
env_variables:
  PROJECT_NAME:
    description: "Name of the project"
    default: "${PROJECT_NAME}"
  DB_DATABASE:
    description: "Database name"
    default: "${PROJECT_NAME}"
  DB_USERNAME:
    description: "Database user"
    default: "${PROJECT_NAME}"
  DB_PASSWORD:
    description: "Database password"
    default: "secret"
  DB_ROOT_PASSWORD:
    description: "Database root password"
    default: "rootsecret"

network:
  name: "${PROJECT_NAME}_network"
  driver: bridge

```

# src/chimera/templates/php/nginx/mariadb/config/development.yaml

```yaml
project:
  name: ${PROJECT_NAME}
  language: php
  framework: none
  environment: development

services:
  mariadb:
    image: mariadb:10.6
    environment:
      MYSQL_DATABASE: ${DB_DATABASE}
      MYSQL_USER: ${DB_USERNAME}
      MYSQL_PASSWORD: ${DB_PASSWORD}
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
    ports:
      - "${MARIADB_PORT}:3306"
    volumes:
      - mariadb_data:/var/lib/mysql
    networks:
      - app_network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - ${NGINX_PORT}:80
    volumes:
      - .:/var/www/html:cached
      - ./docker/nginx/conf.d:/etc/nginx/conf.d:ro
    depends_on:
      - php
    networks:
      - app_network
    healthcheck:
      test:
        - CMD
        - wget
        - --quiet
        - --tries=1
        - --spider
        - http://localhost/ping
      interval: 10s
      timeout: 5s
      retries: 3
  php:
    volumes:
      - .:/var/www/html:cached
      - php_logs:/var/log/php-fpm
    environment:
      PHP_DISPLAY_ERRORS: ${PHP_DISPLAY_ERRORS}
      PHP_ERROR_REPORTING: ${PHP_ERROR_REPORTING}
      PHP_MEMORY_LIMIT: ${PHP_MEMORY_LIMIT}
      PHP_MAX_EXECUTION_TIME: ${PHP_MAX_EXECUTION_TIME}
      PHP_POST_MAX_SIZE: ${PHP_POST_MAX_SIZE}
      PHP_UPLOAD_MAX_FILESIZE: ${PHP_UPLOAD_MAX_FILESIZE}
    networks:
      - app_network
    healthcheck:
      test:
        - CMD
        - php-fpm
        - -t
      interval: 10s
      timeout: 5s
      retries: 3
volumes:
  mariadb_data:
    driver: local
    name: ${PROJECT_NAME}_mariadb_data
  php_logs:
    driver: local
    name: ${PROJECT_NAME}_php_logs
networks:
  app_network:
    driver: bridge
    name: ${PROJECT_NAME}_network

```

# src/chimera/templates/php/nginx/mariadb/docker-compose.yml

```yml
services:
  mariadb:
    image: mariadb:10.6
    container_name: ${PROJECT_NAME}-mariadb
    environment:
      MYSQL_DATABASE: ${DB_DATABASE}
      MYSQL_USER: ${DB_USERNAME}
      MYSQL_PASSWORD: ${DB_PASSWORD}
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
    ports:
      - "${MARIADB_PORT}:3306"
    volumes:
      - mariadb_data:/var/lib/mysql
      - ./docker/mariadb/my.cnf:/etc/mysql/conf.d/custom.cnf:cached
    networks:
      - app_network

  phpmyadmin:
    image: phpmyadmin/phpmyadmin
    container_name: ${PROJECT_NAME}-phpmyadmin
    environment:
      PMA_HOST: mariadb
      PMA_USER: ${DB_USERNAME}
      PMA_PASSWORD: ${DB_PASSWORD}
    ports:
      - "${PHPMYADMIN_PORT}:80"
    networks:
      - app_network

  php:
    build:
      context: .
      dockerfile: docker/php/Dockerfile
    container_name: ${PROJECT_NAME}-php
    volumes:
      - .:/var/www/html:cached
      - php_logs:/var/log/php-fpm
    networks:
      - app_network

  nginx:
    image: nginx:alpine
    container_name: ${PROJECT_NAME}-nginx
    ports:
      - "${NGINX_PORT}:80"
    volumes:
      - .:/var/www/html:cached
      - ./docker/nginx/conf.d:/etc/nginx/conf.d:cached
    depends_on:
      - php
    networks:
      - app_network

networks:
  app_network:
    name: ${PROJECT_NAME}_network

volumes:
  mariadb_data:
    name: ${PROJECT_NAME}_mariadb_data
  php_logs:
    name: ${PROJECT_NAME}_php_logs
```

# src/chimera/templates/php/nginx/mariadb/docker/mariadb/my.cnf

```cnf
[mysqld]
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

max_connections = 100
thread_cache_size = 8
thread_stack = 256K

innodb_buffer_pool_size = 256M
innodb_buffer_pool_instances = 4
innodb_log_file_size = 64M

sql_mode = STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION

[mysql]
default-character-set = utf8mb4

[client]
default-character-set = utf8mb4

```

# src/chimera/templates/php/nginx/mariadb/docker/nginx/conf.d/default.conf

```conf
server {
    listen 80;
    server_name localhost;
    root /var/www/html/public;
    index index.php index.html;

    location = /health {
        access_log off;
        add_header Content-Type text/plain;
        return 200 'healthy';
    }

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        fastcgi_split_path_info ^(.+\.php)(/.+)$;
        fastcgi_pass php:9000;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param PATH_INFO $fastcgi_path_info;
        fastcgi_buffer_size 32k;
        fastcgi_buffers 16 16k;
        fastcgi_read_timeout 300;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires max;
        access_log off;
        add_header Cache-Control "public";
    }
}

```

# src/chimera/templates/php/nginx/mariadb/docker/php/Dockerfile

```
FROM php:8.2-fpm

RUN apt-get update && apt-get install -y \
    git zip unzip libpng-dev libonig-dev libzip-dev \
    && rm -rf /var/lib/apt/lists/*

RUN docker-php-ext-install \
    pdo \
    pdo_mysql \
    mbstring \
    zip \
    exif \
    gd

COPY docker/php/php.ini /usr/local/etc/php/conf.d/custom.ini
COPY docker/php/www.conf /usr/local/etc/php-fpm.d/www.conf

RUN mkdir -p /var/log/php-fpm \
    && chown -R www-data:www-data /var/log/php-fpm

WORKDIR /var/www/html

USER www-data

```

# src/chimera/templates/php/nginx/mariadb/docker/php/php.ini

```ini
[PHP]
display_errors = ${PHP_DISPLAY_ERRORS}
display_startup_errors = ${PHP_DISPLAY_ERRORS}
error_reporting = ${PHP_ERROR_REPORTING}
log_errors = On
error_log = /var/log/php-fpm/php_errors.log
log_errors_max_len = 1024
ignore_repeated_errors = Off
ignore_repeated_source = Off
report_memleaks = On

memory_limit = ${PHP_MEMORY_LIMIT}
max_execution_time = ${PHP_MAX_EXECUTION_TIME}
post_max_size = ${PHP_POST_MAX_SIZE}
upload_max_filesize = ${PHP_UPLOAD_MAX_FILESIZE}
max_file_uploads = 20

[Date]
date.timezone = UTC

[Session]
session.save_handler = files
session.save_path = /tmp
session.gc_maxlifetime = 1800
session.gc_probability = 1
session.gc_divisor = 100

[opcache]
opcache.enable = 1
opcache.memory_consumption = 128
opcache.interned_strings_buffer = 8
opcache.max_accelerated_files = 4000
opcache.validate_timestamps = 1
opcache.revalidate_freq = 0
opcache.fast_shutdown = 1

[mysqlnd]
mysqlnd.collect_statistics = On
mysqlnd.collect_memory_statistics = On

```

# src/chimera/templates/php/nginx/mariadb/docker/php/www.conf

```conf
[global]
error_log = /var/log/php-fpm/error.log
log_level = notice

[www]
user = www-data
group = www-data

listen = 9000
listen.owner = www-data
listen.group = www-data
listen.mode = 0660

pm = dynamic
pm.max_children = 10
pm.start_servers = 2
pm.min_spare_servers = 1
pm.max_spare_servers = 3
pm.max_requests = 500

catch_workers_output = yes
decorate_workers_output = yes

php_admin_value[error_log] = /var/log/php-fpm/www-error.log
php_admin_flag[log_errors] = on

security.limit_extensions = .php

```

# src/chimera/templates/php/nginx/mariadb/public/index.php

```php
<?php
declare(strict_types=1);

require_once __DIR__ . '/../src/bootstrap.php';

$uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

switch ($uri) {
    case '/':
        require __DIR__ . '/../src/pages/home.php';
        break;
    case '/info':
        phpinfo();
        break;
    case '/health':
        header('Content-Type: text/plain');
        echo 'healthy';
        break;
    default:
        http_response_code(404);
        echo "404 Not Found";
        break;
}

```

# src/chimera/templates/php/nginx/mariadb/src/bootstrap.php

```php
<?php
declare(strict_types=1);

error_reporting(E_ALL);
ini_set('display_errors', '1');

if (file_exists(__DIR__ . '/../.env')) {
    $env = parse_ini_file(__DIR__ . '/../.env');
    foreach ($env as $key => $value) {
        $_ENV[$key] = $value;
        putenv("$key=$value");
    }
}

spl_autoload_register(function ($class) {
    $file = __DIR__ . DIRECTORY_SEPARATOR . 
            str_replace(['\\', '/'], DIRECTORY_SEPARATOR, $class) . '.php';
    
    if (file_exists($file)) {
        require_once $file;
        return true;
    }
    return false;
});

$composerAutoloader = __DIR__ . '/../vendor/autoload.php';
if (file_exists($composerAutoloader)) {
    require_once $composerAutoloader;
}

```

# src/chimera/templates/php/nginx/mariadb/src/pages/home.php

```php
<?php

declare(strict_types=1);
$title = 'ChimeraStack PHP Development Environment';
$webPort = $_ENV['NGINX_PORT'] ?? '8093';
$dbPort = $_ENV['MARIADB_PORT'] ?? '3307';
$pmaPort = $_ENV['PHPMYADMIN_PORT'] ?? '8092';
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= htmlspecialchars($title) ?></title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            line-height: 1.6;
        }

        .status {
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 4px;
        }

        .success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }

        .card {
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 1rem;
            margin: 1rem 0;
        }

        .info {
            background-color: #e2e3e5;
            border-color: #d6d8db;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }

        th,
        td {
            text-align: left;
            padding: 0.5rem;
            border-bottom: 1px solid #ddd;
        }
    </style>
</head>

<body>
    <h1><?= htmlspecialchars($title) ?></h1>

    <div class="card">
        <h2>Stack Overview</h2>
        <table>
            <tr>
                <th>Component</th>
                <th>Details</th>
                <th>Access</th>
            </tr>
            <tr>
                <td>Web Server</td>
                <td>Nginx + PHP-FPM</td>
                <td><a href="http://localhost:<?= $webPort ?>" target="_blank">localhost:<?= $webPort ?></a></td>
            </tr>
            <tr>
                <td>Database</td>
                <td>MariaDB <?= $_ENV['DB_DATABASE'] ?></td>
                <td>localhost:<?= $dbPort ?></td>
            </tr>
            <tr>
                <td>Database GUI</td>
                <td>phpMyAdmin</td>
                <td><a href="http://localhost:<?= $pmaPort ?>" target="_blank">localhost:<?= $pmaPort ?></a></td>
            </tr>
        </table>
    </div>

    <div class="card info">
        <h2>Quick Links</h2>
        <ul>
            <li><a href="/info">PHP Info</a></li>
            <li><a href="http://localhost:<?= $pmaPort ?>" target="_blank">phpMyAdmin</a></li>
        </ul>
    </div>

    <div class="card">
        <h2>Database Connection Status</h2>
        <?php
        try {
            $dsn = "mysql:host={$_ENV['DB_HOST']};dbname={$_ENV['DB_DATABASE']}";
            $pdo = new PDO($dsn, $_ENV['DB_USERNAME'], $_ENV['DB_PASSWORD']);
            $version = $pdo->query('SELECT VERSION()')->fetchColumn();
            echo '<div class="status success">
                ✓ Connected to MariaDB Server ' . htmlspecialchars($version) . '<br>
                Database: ' . htmlspecialchars($_ENV['DB_DATABASE']) . '<br>
                User: ' . htmlspecialchars($_ENV['DB_USERNAME']) . '
            </div>';
        } catch (PDOException $e) {
            echo '<div class="status error">✗ Database connection failed: ' . htmlspecialchars($e->getMessage()) . '</div>';
        }
        ?>
    </div>
</body>

</html>
```

# src/chimera/templates/php/nginx/mariadb/template.yaml

```yaml
name: "PHP/Nginx/MariaDB Stack"
type: "PHP Development"
description: "PHP development environment with Nginx web server and MariaDB database"
version: "1.0"
author: "ChimeraStack"

services:
  nginx:
    port_type: backend
    service_variant: php-nginx
    default_port: 8093
  phpmyadmin:
    port_type: admin
    service_variant: phpmyadmin
    default_port: 8092
  mariadb:
    port_type: database
    service_variant: mariadb
    default_port: 3307

env_template: ".env.example"
env_variables:
  PROJECT_NAME:
    description: "Project name"
    default: "${PROJECT_NAME}"
  DB_DATABASE:
    description: "Database name"
    default: "${PROJECT_NAME}"
  DB_USERNAME:
    description: "Database user"
    default: "${PROJECT_NAME}"
  DB_PASSWORD:
    description: "Database password"
    default: "secret"
  DB_ROOT_PASSWORD:
    description: "Database root password"
    default: "rootsecret"

network:
  name: "${PROJECT_NAME}_network"
  driver: bridge

```

# src/chimera/templates/php/nginx/mysql/config/development.yaml

```yaml
project:
  name: ${PROJECT_NAME}
  language: php
  framework: none
  environment: development

services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: ${DB_DATABASE}
      MYSQL_USER: ${DB_USERNAME}
      MYSQL_PASSWORD: ${DB_PASSWORD}
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
    ports:
      - ${MYSQL_PORT}:3306
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - app_network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - ${NGINX_PORT}:80
    volumes:
      - .:/var/www/html:cached
      - ./docker/nginx/conf.d:/etc/nginx/conf.d:ro
    depends_on:
      - php
    networks:
      - app_network
    healthcheck:
      test:
        [
          "CMD",
          "wget",
          "--quiet",
          "--tries=1",
          "--spider",
          "http://localhost/ping",
        ]
      interval: 10s
      timeout: 5s
      retries: 3

  php:
    volumes:
      - .:/var/www/html:cached
      - php_logs:/var/log/php-fpm
    environment:
      PHP_DISPLAY_ERRORS: ${PHP_DISPLAY_ERRORS}
      PHP_ERROR_REPORTING: ${PHP_ERROR_REPORTING}
      PHP_MEMORY_LIMIT: ${PHP_MEMORY_LIMIT}
      PHP_MAX_EXECUTION_TIME: ${PHP_MAX_EXECUTION_TIME}
      PHP_POST_MAX_SIZE: ${PHP_POST_MAX_SIZE}
      PHP_UPLOAD_MAX_FILESIZE: ${PHP_UPLOAD_MAX_FILESIZE}
    networks:
      - app_network
    healthcheck:
      test: ["CMD", "php-fpm", "-t"]
      interval: 10s
      timeout: 5s
      retries: 3

volumes:
  mysql_data:
    driver: local
    name: ${PROJECT_NAME}_mysql_data
  php_logs:
    driver: local
    name: ${PROJECT_NAME}_php_logs

networks:
  app_network:
    driver: bridge
    name: ${PROJECT_NAME}_network

```

# src/chimera/templates/php/nginx/mysql/docker-compose.yml

```yml
services:
  mysql:
    image: mysql:8.0
    container_name: ${PROJECT_NAME}-mysql
    environment:
      MYSQL_DATABASE: ${DB_DATABASE}
      MYSQL_USER: ${DB_USERNAME}
      MYSQL_PASSWORD: ${DB_PASSWORD}
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
    ports:
      - "${MYSQL_PORT}:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./docker/mysql/my.cnf:/etc/mysql/conf.d/custom.cnf:cached
    networks:
      - app_network

  phpmyadmin:
    image: phpmyadmin/phpmyadmin
    container_name: ${PROJECT_NAME}-phpmyadmin
    environment:
      PMA_HOST: mysql
      PMA_USER: ${DB_USERNAME}
      PMA_PASSWORD: ${DB_PASSWORD}
    ports:
      - "${PHPMYADMIN_PORT}:80"
    networks:
      - app_network

  php:
    build:
      context: .
      dockerfile: docker/php/Dockerfile
    container_name: ${PROJECT_NAME}-php
    volumes:
      - .:/var/www/html:cached
      - php_logs:/var/log/php-fpm
    networks:
      - app_network

  nginx:
    image: nginx:alpine
    container_name: ${PROJECT_NAME}-nginx
    ports:
      - "${NGINX_PORT}:80"
    volumes:
      - .:/var/www/html:cached
      - ./docker/nginx/conf.d:/etc/nginx/conf.d:cached
    depends_on:
      - php
    networks:
      - app_network

networks:
  app_network:
    name: ${PROJECT_NAME}_network

volumes:
  mysql_data:
    name: ${PROJECT_NAME}_mysql_data
  php_logs:
    name: ${PROJECT_NAME}_php_logs

```

# src/chimera/templates/php/nginx/mysql/docker/mysql/my.cnf

```cnf
[mysqld]
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci
default_authentication_plugin = mysql_native_password

max_connections = 100
thread_cache_size = 8
thread_stack = 256K

innodb_buffer_pool_size = 256M
innodb_buffer_pool_instances = 4
innodb_log_file_size = 64M
innodb_flush_method = O_DIRECT
innodb_flush_log_at_trx_commit = 2
innodb_file_per_table = 1
innodb_strict_mode = 1

tmp_table_size = 32M
max_heap_table_size = 32M

max_allowed_packet = 64M
sql_mode = STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION

[mysql]
default-character-set = utf8mb4

[client]
default-character-set = utf8mb4

```

# src/chimera/templates/php/nginx/mysql/docker/nginx/conf.d/default.conf

```conf
server {
    listen 80;
    server_name localhost;
    root /var/www/html/public;
    index index.php index.html;

    location = /health {
        access_log off;
        add_header Content-Type text/plain;
        return 200 'healthy';
    }

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        fastcgi_split_path_info ^(.+\.php)(/.+)$;
        fastcgi_pass php:9000;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param PATH_INFO $fastcgi_path_info;
        fastcgi_buffer_size 32k;
        fastcgi_buffers 16 16k;
        fastcgi_read_timeout 300;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires max;
        access_log off;
        add_header Cache-Control "public";
    }
}

```

# src/chimera/templates/php/nginx/mysql/docker/php/Dockerfile

```
FROM php:8.2-fpm

RUN apt-get update && apt-get install -y \
    git \
    zip \
    unzip \
    libpng-dev \
    libonig-dev \
    libzip-dev \
    && rm -rf /var/lib/apt/lists/*

RUN docker-php-ext-install \
    pdo \
    pdo_mysql \
    mbstring \
    zip \
    exif \
    gd

COPY docker/php/php.ini /usr/local/etc/php/conf.d/custom.ini
COPY docker/php/www.conf /usr/local/etc/php-fpm.d/www.conf

RUN mkdir -p /var/log/php-fpm \
    && chown -R www-data:www-data /var/log/php-fpm

WORKDIR /var/www/html

USER www-data

```

# src/chimera/templates/php/nginx/mysql/docker/php/php.ini

```ini
[PHP]
display_errors = ${PHP_DISPLAY_ERRORS}
display_startup_errors = ${PHP_DISPLAY_ERRORS}
error_reporting = ${PHP_ERROR_REPORTING}
log_errors = On
error_log = /var/log/php-fpm/php_errors.log
log_errors_max_len = 1024
ignore_repeated_errors = Off
ignore_repeated_source = Off
report_memleaks = On

memory_limit = ${PHP_MEMORY_LIMIT}
max_execution_time = ${PHP_MAX_EXECUTION_TIME}
post_max_size = ${PHP_POST_MAX_SIZE}
upload_max_filesize = ${PHP_UPLOAD_MAX_FILESIZE}
max_file_uploads = 20

[Date]
date.timezone = UTC

[Session]
session.save_handler = files
session.save_path = /tmp
session.gc_maxlifetime = 1800
session.gc_probability = 1
session.gc_divisor = 100

[opcache]
opcache.enable = 1
opcache.memory_consumption = 128
opcache.interned_strings_buffer = 8
opcache.max_accelerated_files = 4000
opcache.validate_timestamps = 1
opcache.revalidate_freq = 0
opcache.fast_shutdown = 1

[mysqlnd]
mysqlnd.collect_statistics = On
mysqlnd.collect_memory_statistics = On

```

# src/chimera/templates/php/nginx/mysql/docker/php/www.conf

```conf
[global]
error_log = /var/log/php-fpm/error.log
log_level = notice

[www]
user = www-data
group = www-data

listen = 9000
listen.owner = www-data
listen.group = www-data
listen.mode = 0660

pm = dynamic
pm.max_children = 10
pm.start_servers = 2
pm.min_spare_servers = 1
pm.max_spare_servers = 3
pm.max_requests = 500

catch_workers_output = yes
decorate_workers_output = yes

php_admin_value[error_log] = /var/log/php-fpm/www-error.log
php_admin_flag[log_errors] = on

security.limit_extensions = .php

```

# src/chimera/templates/php/nginx/mysql/public/index.php

```php
<?php
declare(strict_types=1);

require_once __DIR__ . '/../src/bootstrap.php';

$uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

switch ($uri) {
    case '/':
        require __DIR__ . '/../src/pages/home.php';
        break;
    case '/info':
        phpinfo();
        break;
    case '/health':
        header('Content-Type: text/plain');
        echo 'healthy';
        break;
    default:
        http_response_code(404);
        echo "404 Not Found";
        break;
}

```

# src/chimera/templates/php/nginx/mysql/src/bootstrap.php

```php
<?php
declare(strict_types=1);

error_reporting(E_ALL);
ini_set('display_errors', '1');

if (file_exists(__DIR__ . '/../.env')) {
    $env = parse_ini_file(__DIR__ . '/../.env');
    foreach ($env as $key => $value) {
        $_ENV[$key] = $value;
        putenv("$key=$value");
    }
}

spl_autoload_register(function ($class) {
    $file = __DIR__ . DIRECTORY_SEPARATOR . 
            str_replace(['\\', '/'], DIRECTORY_SEPARATOR, $class) . '.php';
    
    if (file_exists($file)) {
        require_once $file;
        return true;
    }
    return false;
});

$composerAutoloader = __DIR__ . '/../vendor/autoload.php';
if (file_exists($composerAutoloader)) {
    require_once $composerAutoloader;
}

```

# src/chimera/templates/php/nginx/mysql/src/pages/home.php

```php
<?php

declare(strict_types=1);
$title = 'ChimeraStack PHP Development Environment';
$webPort = $_ENV['NGINX_PORT'] ?? '8080';
$dbPort = $_ENV['MYSQL_PORT'] ?? '3306';
$pmaPort = $_ENV['PHPMYADMIN_PORT'] ?? '8081';
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= htmlspecialchars($title) ?></title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            line-height: 1.6;
        }

        .status {
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 4px;
        }

        .success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }

        .card {
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 1rem;
            margin: 1rem 0;
        }

        .info {
            background-color: #e2e3e5;
            border-color: #d6d8db;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }

        th,
        td {
            text-align: left;
            padding: 0.5rem;
            border-bottom: 1px solid #ddd;
        }
    </style>
</head>

<body>
    <h1><?= htmlspecialchars($title) ?></h1>

    <div class="card">
        <h2>Stack Overview</h2>
        <table>
            <tr>
                <th>Component</th>
                <th>Details</th>
                <th>Access</th>
            </tr>
            <tr>
                <td>Web Server</td>
                <td>Nginx + PHP-FPM</td>
                <td><a href="http://localhost:<?= $webPort ?>" target="_blank">localhost:<?= $webPort ?></a></td>
            </tr>
            <tr>
                <td>Database</td>
                <td>MySQL <?= $_ENV['DB_DATABASE'] ?></td>
                <td>localhost:<?= $dbPort ?></td>
            </tr>
            <tr>
                <td>Database GUI</td>
                <td>phpMyAdmin</td>
                <td><a href="http://localhost:<?= $pmaPort ?>" target="_blank">localhost:<?= $pmaPort ?></a></td>
            </tr>
        </table>
    </div>

    <div class="card info">
        <h2>Quick Links</h2>
        <ul>
            <li><a href="/info">PHP Info</a></li>
            <li><a href="http://localhost:<?= $pmaPort ?>" target="_blank">phpMyAdmin</a></li>
        </ul>
    </div>

    <div class="card">
        <h2>Database Connection Status</h2>
        <?php
        try {
            $dsn = "mysql:host={$_ENV['DB_HOST']};dbname={$_ENV['DB_DATABASE']}";
            $pdo = new PDO($dsn, $_ENV['DB_USERNAME'], $_ENV['DB_PASSWORD']);
            $version = $pdo->query('SELECT VERSION()')->fetchColumn();
            echo '<div class="status success">
                ✓ Connected to MySQL Server ' . htmlspecialchars($version) . '<br>
                Database: ' . htmlspecialchars($_ENV['DB_DATABASE']) . '<br>
                User: ' . htmlspecialchars($_ENV['DB_USERNAME']) . '
            </div>';
        } catch (PDOException $e) {
            echo '<div class="status error">✗ Database connection failed: ' . htmlspecialchars($e->getMessage()) . '</div>';
        }
        ?>
    </div>
</body>

</html>
```

# src/chimera/templates/php/nginx/mysql/template.yaml

```yaml
name: "PHP/Nginx/MySQL Stack"
type: "PHP Development"
description: "PHP development environment with Nginx web server and MySQL database"
version: "1.0"
author: "ChimeraStack"

services:
  nginx:
    port_type: backend
    service_variant: php-nginx
    default_port: 8080
  phpmyadmin:
    port_type: admin
    service_variant: phpmyadmin
    default_port: 8081
  mysql:
    port_type: database
    service_variant: mysql
    default_port: 3306

env_template: ".env.example"
env_variables:
  PROJECT_NAME:
    description: "Project name"
    default: "${PROJECT_NAME}"
  DB_DATABASE:
    description: "Database name"
    default: "${PROJECT_NAME}"
  DB_USERNAME:
    description: "Database user"
    default: "${PROJECT_NAME}"
  DB_PASSWORD:
    description: "Database password"
    default: "secret"
  DB_ROOT_PASSWORD:
    description: "Database root password"
    default: "rootsecret"

network:
  name: "${PROJECT_NAME}_network"
  driver: bridge

```

# src/chimera/templates/php/nginx/postgresql/config/development.yaml

```yaml
project:
  name: ${PROJECT_NAME}
  language: php
  framework: none
  environment: development

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ${DB_DATABASE}
      POSTGRES_USER: ${DB_USERNAME}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    ports:
      - ${POSTGRES_PORT}:5432
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app_network
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "${DB_USERNAME}"]
      interval: 10s
      timeout: 5s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - ${NGINX_PORT}:80
    volumes:
      - .:/var/www/html:cached
      - ./docker/nginx/conf.d:/etc/nginx/conf.d:ro
    depends_on:
      - php
    networks:
      - app_network
    healthcheck:
      test:
        [
          "CMD",
          "wget",
          "--quiet",
          "--tries=1",
          "--spider",
          "http://localhost/ping",
        ]
      interval: 10s
      timeout: 5s
      retries: 3

  php:
    volumes:
      - .:/var/www/html:cached
      - php_logs:/var/log/php-fpm
    environment:
      PHP_DISPLAY_ERRORS: ${PHP_DISPLAY_ERRORS}
      PHP_ERROR_REPORTING: ${PHP_ERROR_REPORTING}
      PHP_MEMORY_LIMIT: ${PHP_MEMORY_LIMIT}
      PHP_MAX_EXECUTION_TIME: ${PHP_MAX_EXECUTION_TIME}
      PHP_POST_MAX_SIZE: ${PHP_POST_MAX_SIZE}
      PHP_UPLOAD_MAX_FILESIZE: ${PHP_UPLOAD_MAX_FILESIZE}
    networks:
      - app_network
    healthcheck:
      test: ["CMD", "php-fpm", "-t"]
      interval: 10s
      timeout: 5s
      retries: 3

volumes:
  postgres_data:
    driver: local
    name: ${PROJECT_NAME}_postgres_data
  php_logs:
    driver: local
    name: ${PROJECT_NAME}_php_logs

networks:
  app_network:
    driver: bridge
    name: ${PROJECT_NAME}_network

```

# src/chimera/templates/php/nginx/postgresql/docker-compose.yml

```yml
services:
 postgres:
   image: postgres:15-alpine
   container_name: ${PROJECT_NAME}-postgres
   environment:
     POSTGRES_DB: ${DB_DATABASE}
     POSTGRES_USER: ${DB_USERNAME}
     POSTGRES_PASSWORD: ${DB_PASSWORD}
   ports:
     - "${POSTGRES_PORT}:5432"
   volumes:
     - postgres_data:/var/lib/postgresql/data
     - ./docker/postgres/init.sql:/docker-entrypoint-initdb.d/init.sql:cached
   networks:
     - app_network

 pgadmin:
   image: dpage/pgadmin4
   container_name: ${PROJECT_NAME}-pgadmin
   environment:
     PGADMIN_DEFAULT_EMAIL: admin@admin.com
     PGADMIN_DEFAULT_PASSWORD: admin
   ports:
     - "${PGADMIN_PORT}:80"
   networks:
     - app_network

 php:
   build:
     context: .
     dockerfile: docker/php/Dockerfile
   container_name: ${PROJECT_NAME}-php
   volumes:
     - .:/var/www/html:cached
     - php_logs:/var/log/php-fpm
   networks:
     - app_network

 nginx:
   image: nginx:alpine
   container_name: ${PROJECT_NAME}-nginx
   ports:
     - "${NGINX_PORT}:80"
   volumes:
     - .:/var/www/html:cached
     - ./docker/nginx/conf.d:/etc/nginx/conf.d:cached
   depends_on:
     - php
   networks:
     - app_network

networks:
 app_network:
   name: ${PROJECT_NAME}_network

volumes:
 postgres_data:
   name: ${PROJECT_NAME}_postgres_data
 php_logs:
   name: ${PROJECT_NAME}_php_logs
```

# src/chimera/templates/php/nginx/postgresql/docker/nginx/conf.d/default.conf

```conf
server {
    listen 80;
    server_name localhost;
    root /var/www/html/public;
    index index.php index.html;

    location = /health {
        access_log off;
        add_header Content-Type text/plain;
        return 200 'healthy';
    }

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        fastcgi_split_path_info ^(.+\.php)(/.+)$;
        fastcgi_pass php:9000;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param PATH_INFO $fastcgi_path_info;
        fastcgi_buffer_size 32k;
        fastcgi_buffers 16 16k;
        fastcgi_read_timeout 300;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires max;
        access_log off;
        add_header Cache-Control "public";
    }
}

```

# src/chimera/templates/php/nginx/postgresql/docker/php/Dockerfile

```
FROM php:8.2-fpm

RUN apt-get update && apt-get install -y \
    git zip unzip libpng-dev libonig-dev libzip-dev libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN docker-php-ext-install \
    pdo \
    pdo_pgsql \
    mbstring \
    zip \
    exif \
    gd

COPY docker/php/php.ini /usr/local/etc/php/conf.d/custom.ini
COPY docker/php/www.conf /usr/local/etc/php-fpm.d/www.conf

RUN mkdir -p /var/log/php-fpm \
    && chown -R www-data:www-data /var/log/php-fpm

WORKDIR /var/www/html

USER www-data

```

# src/chimera/templates/php/nginx/postgresql/docker/php/php.ini

```ini
[PHP]
display_errors = ${PHP_DISPLAY_ERRORS}
display_startup_errors = ${PHP_DISPLAY_ERRORS}
error_reporting = ${PHP_ERROR_REPORTING}
log_errors = On
error_log = /var/log/php-fpm/php_errors.log
log_errors_max_len = 1024
ignore_repeated_errors = Off
ignore_repeated_source = Off
report_memleaks = On

memory_limit = ${PHP_MEMORY_LIMIT}
max_execution_time = ${PHP_MAX_EXECUTION_TIME}
post_max_size = ${PHP_POST_MAX_SIZE}
upload_max_filesize = ${PHP_UPLOAD_MAX_FILESIZE}
max_file_uploads = 20

[Date]
date.timezone = UTC

[Session]
session.save_handler = files
session.save_path = /tmp
session.gc_maxlifetime = 1800
session.gc_probability = 1
session.gc_divisor = 100

[opcache]
opcache.enable = 1
opcache.memory_consumption = 128
opcache.interned_strings_buffer = 8
opcache.max_accelerated_files = 4000
opcache.validate_timestamps = 1
opcache.revalidate_freq = 0
opcache.fast_shutdown = 1

[mysqlnd]
mysqlnd.collect_statistics = On
mysqlnd.collect_memory_statistics = On

```

# src/chimera/templates/php/nginx/postgresql/docker/php/www.conf

```conf
[global]
error_log = /var/log/php-fpm/error.log
log_level = notice

[www]
user = www-data
group = www-data

listen = 9000
listen.owner = www-data
listen.group = www-data
listen.mode = 0660

pm = dynamic
pm.max_children = 10
pm.start_servers = 2
pm.min_spare_servers = 1
pm.max_spare_servers = 3
pm.max_requests = 500

catch_workers_output = yes
decorate_workers_output = yes

php_admin_value[error_log] = /var/log/php-fpm/www-error.log
php_admin_flag[log_errors] = on

security.limit_extensions = .php

```

# src/chimera/templates/php/nginx/postgresql/docker/postgres/init.sql

```sql
CREATE DATABASE ${DB_DATABASE} WITH OWNER ${DB_USERNAME} 
  ENCODING 'UTF8' LC_COLLATE 'en_US.utf8' LC_CTYPE 'en_US.utf8';

```

# src/chimera/templates/php/nginx/postgresql/public/index.php

```php
<?php
declare(strict_types=1);

require_once __DIR__ . '/../src/bootstrap.php';

$uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

switch ($uri) {
    case '/':
        require __DIR__ . '/../src/pages/home.php';
        break;
    case '/info':
        phpinfo();
        break;
    case '/health':
        header('Content-Type: text/plain');
        echo 'healthy';
        break;
    default:
        http_response_code(404);
        echo "404 Not Found";
        break;
}

```

# src/chimera/templates/php/nginx/postgresql/src/bootstrap.php

```php
<?php
declare(strict_types=1);

error_reporting(E_ALL);
ini_set('display_errors', '1');

if (file_exists(__DIR__ . '/../.env')) {
    $env = parse_ini_file(__DIR__ . '/../.env');
    foreach ($env as $key => $value) {
        $_ENV[$key] = $value;
        putenv("$key=$value");
    }
}

spl_autoload_register(function ($class) {
    $file = __DIR__ . DIRECTORY_SEPARATOR . 
            str_replace(['\\', '/'], DIRECTORY_SEPARATOR, $class) . '.php';
    
    if (file_exists($file)) {
        require_once $file;
        return true;
    }
    return false;
});

$composerAutoloader = __DIR__ . '/../vendor/autoload.php';
if (file_exists($composerAutoloader)) {
    require_once $composerAutoloader;
}

```

# src/chimera/templates/php/nginx/postgresql/src/pages/home.php

```php
<?php

declare(strict_types=1);
$title = 'ChimeraStack PHP Development Environment';
$webPort = $_ENV['NGINX_PORT'] ?? '8090';
$dbPort = $_ENV['POSTGRES_PORT'] ?? '5432';
$pgaPort = $_ENV['PGADMIN_PORT'] ?? '8091';
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= htmlspecialchars($title) ?></title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            line-height: 1.6;
        }

        .status {
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 4px;
        }

        .success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }

        .card {
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 1rem;
            margin: 1rem 0;
        }

        .info {
            background-color: #e2e3e5;
            border-color: #d6d8db;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }

        th,
        td {
            text-align: left;
            padding: 0.5rem;
            border-bottom: 1px solid #ddd;
        }
    </style>
</head>

<body>
    <h1><?= htmlspecialchars($title) ?></h1>

    <div class="card">
        <h2>Stack Overview</h2>
        <table>
            <tr>
                <th>Component</th>
                <th>Details</th>
                <th>Access</th>
            </tr>
            <tr>
                <td>Web Server</td>
                <td>Nginx + PHP-FPM</td>
                <td><a href="http://localhost:<?= $webPort ?>" target="_blank">localhost:<?= $webPort ?></a></td>
            </tr>
            <tr>
                <td>Database</td>
                <td>PostgreSQL <?= $_ENV['DB_DATABASE'] ?></td>
                <td>localhost:<?= $dbPort ?></td>
            </tr>
            <tr>
                <td>Database GUI</td>
                <td>pgAdmin</td>
                <td><a href="http://localhost:<?= $pgaPort ?>" target="_blank">localhost:<?= $pgaPort ?></a></td>
            </tr>
        </table>
    </div>

    <div class="card info">
        <h2>Quick Links</h2>
        <ul>
            <li><a href="/info">PHP Info</a></li>
            <li><a href="http://localhost:<?= $pgAdminPort ?>" target="_blank">pgAdmin</a></li>
        </ul>
    </div>

    <div class="card">
        <h2>Database Connection Status</h2>
        <?php
        try {
            $dsn = "pgsql:host={$_ENV['DB_HOST']};dbname={$_ENV['DB_DATABASE']}";
            $pdo = new PDO($dsn, $_ENV['DB_USERNAME'], $_ENV['DB_PASSWORD']);
            $version = $pdo->query('SELECT VERSION()')->fetchColumn();
            echo '<div class="status success">
                ✓ Connected to PostgreSQL Server ' . htmlspecialchars($version) . '<br>
                Database: ' . htmlspecialchars($_ENV['DB_DATABASE']) . '<br>
                User: ' . htmlspecialchars($_ENV['DB_USERNAME']) . '
            </div>';
        } catch (PDOException $e) {
            echo '<div class="status error">✗ Database connection failed: ' . htmlspecialchars($e->getMessage()) . '</div>';
        }
        ?>
    </div>
</body>

</html>
```

# src/chimera/templates/php/nginx/postgresql/template.yaml

```yaml
name: "PHP/Nginx/PostgreSQL Stack"
type: "PHP Development"
description: "PHP development environment with Nginx web server and PostgreSQL database"
version: "1.0"
author: "ChimeraStack"

services:
  nginx:
    port_type: backend
    service_variant: php-nginx
    default_port: 8090
  pgadmin:
    port_type: admin
    service_variant: pgadmin
    default_port: 8091
  postgres:
    port_type: database
    service_variant: postgres
    default_port: 5432

env_template: ".env.example"
env_variables:
  PROJECT_NAME:
    description: "Project name"
    default: "${PROJECT_NAME}"
  DB_DATABASE:
    description: "Database name"
    default: "${PROJECT_NAME}"
  DB_USERNAME:
    description: "Database user"
    default: "${PROJECT_NAME}"
  DB_PASSWORD:
    description: "Database password"
    default: "secret"

network:
  name: "${PROJECT_NAME}_network"
  driver: bridge

```


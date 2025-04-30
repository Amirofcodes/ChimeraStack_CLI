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
    VALID_CATEGORIES = ['frontend', 'backend', 'fullstack']

    def __init__(self, templates_dir: Path | str = None, verbose: bool = False):
        if templates_dir is None:
            templates_dir = Path(__file__).parent.parent / 'templates'
        self.templates_dir = Path(templates_dir)
        self.port_allocator = PortAllocator()
        self.port_scanner = PortScanner()
        self.verbose = verbose  # Control output verbosity

    # Helper method to print only when verbose is enabled
    def _verbose_print(self, message: str) -> None:
        """Print message only when verbose mode is enabled."""
        if self.verbose:
            console.print(message)

    def get_available_templates(self) -> List[Dict[str, str]]:
        """Get list of available templates with metadata."""
        templates = []

        # Only look for complete stacks in the stacks directory
        stacks_dir = self.templates_dir / 'stacks'
        if stacks_dir.exists():
            for stack_path in stacks_dir.glob('**/*'):
                if stack_path.is_dir() and self._is_valid_template(stack_path):
                    template_info = self._get_template_info(stack_path)
                    if template_info:
                        templates.append(template_info)

        return templates

    def get_templates_by_category(self) -> Dict[str, List[Dict[str, str]]]:
        """Get templates grouped by category."""
        templates = self.get_available_templates()
        grouped = {category: [] for category in self.VALID_CATEGORIES}
        grouped['other'] = []  # For any templates not in a standard category

        for template in templates:
            # Get category from the stack path (e.g., stacks/backend/php-web -> backend)
            relative_path = Path(template['id'])
            category = relative_path.parts[1] if len(
                relative_path.parts) > 1 else 'other'

            if category in self.VALID_CATEGORIES:
                grouped[category].append(template)
            else:
                grouped['other'].append(template)

        # Remove empty categories
        return {k: v for k, v in grouped.items() if v}

    def search_templates(self, query: str) -> List[Dict[str, str]]:
        """Search templates by name, category, description, or tags."""
        templates = self.get_available_templates()
        query = query.lower()

        return [
            template for template in templates
            if query in template.get('id', '').lower()
            or query in template.get('category', '').lower()
            or query in template.get('description', '').lower()
            or any(query in tag.lower() for tag in template.get('tags', []))
        ]

    def _is_valid_template(self, path: Path) -> bool:
        """Check if directory contains a valid template."""
        template_yaml = path / 'template.yaml'
        if not template_yaml.exists():
            return False

        try:
            with open(template_yaml) as f:
                config = yaml.safe_load(f)

            # For stack templates, we need at least one compose file
            if config.get('type') == 'stack':
                compose_files = list(path.glob('docker-compose*.yml'))
                return len(compose_files) > 0

            # For base components, we need the component type and required files
            elif config.get('type') in ['component', 'core']:
                required_files = config.get('files', [])
                return all((path / file['path']).exists() for file in required_files)

            return False
        except Exception:
            return False

    def _get_template_info(self, path: Path) -> Dict[str, str] | None:
        """Get template metadata from template.yaml."""
        try:
            config_path = path / 'template.yaml'
            if not config_path.exists():
                return None

            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)

            # Get the template ID (path relative to templates directory)
            relative_path = path.relative_to(self.templates_dir)
            template_id = str(relative_path)

            # Extract template type and components
            template_type = config.get('type', '')
            components = config.get('components', {})

            # Determine variants based on template
            variants = []

            # Check for database components - these templates have database variants
            has_database = 'database' in components

            # For templates with database component, include all database types as variants
            if has_database:
                # Hard-code the standard database variants for now
                variants = ['mysql', 'postgresql', 'mariadb']

                # When database is fixed in template, use only that variant
                if isinstance(components.get('database'), dict):
                    db_source = components['database'].get('source', '')
                    if db_source and not db_source.endswith('*') and '/' in db_source:
                        db_type = db_source.split('/')[-1]
                        if db_type in ['mysql', 'postgresql', 'mariadb']:
                            variants = [db_type]  # Fixed database type

            # If no variants were found, default to "default"
            if not variants:
                variants = ["default"]

            return {
                'id': template_id,
                'name': config.get('name', ''),
                'description': config.get('description', ''),
                'version': config.get('version', '1.0.0'),
                'type': template_type,
                'tags': config.get('tags', []),
                'variants': variants,
                'path': str(path)
            }
        except Exception as e:
            console.print(
                f"[red]Error reading template config from {path}: {str(e)}")
            return None

    def create_project(self, template_id: str, project_name: str, target_dir: Path | str = None, variant: str = None) -> bool:
        try:
            template_path = self.templates_dir / template_id
            if not self._is_valid_template(template_path):
                console.print(
                    f"[red]Error:[/] Template {template_id} not found or invalid")
                return False

            if target_dir is None:
                target_dir = Path.cwd() / project_name
            else:
                target_dir = Path(target_dir) / project_name

            if target_dir.exists():
                console.print(
                    f"[red]Error:[/] Directory {target_dir} already exists")
                return False

            # Load template configuration
            with open(template_path / 'template.yaml') as f:
                template_config = yaml.safe_load(f)

            # Apply variant if provided
            if variant and variant != 'default' and 'components' in template_config:
                # Check if this template has a database component
                if 'database' in template_config['components']:
                    # List of supported database types
                    db_types = ['mysql', 'postgresql', 'mariadb']

                    # If variant is a database type
                    if variant in db_types:
                        # Get database component config
                        db_component = template_config['components']['database']

                        # Update the database source to use the selected variant
                        if isinstance(db_component, dict):
                            db_component['source'] = f"base/database/{variant}"
                            console.print(
                                f"[green]Using database variant:[/] {variant}")
                        elif isinstance(db_component, str):
                            template_config['components']['database'] = {
                                'source': f"base/database/{variant}",
                                'required': True
                            }
                            console.print(
                                f"[green]Using database variant:[/] {variant}")

            # Allocate ports for services
            port_mappings = self._allocate_service_ports(template_config)
            if not port_mappings:
                console.print(
                    "[red]Error:[/] Failed to allocate required ports")
                return False

            # Copy template files
            shutil.copytree(template_path, target_dir,
                            ignore=shutil.ignore_patterns('template.yaml'))

            # Copy component files
            if 'components' in template_config:
                self._copy_component_files(
                    template_config['components'], target_dir)

            # Create comprehensive port mapping variables
            port_variables = {}

            # Standard service mappings
            if 'web' in port_mappings:
                port_variables['WEB_PORT'] = str(port_mappings['web'])
                port_variables['NGINX_PORT'] = str(port_mappings['web'])

            if 'db' in port_mappings:
                port_variables['DB_PORT'] = str(port_mappings['db'])

                # Add database-specific port names
                if variant == 'postgresql':
                    port_variables['POSTGRES_PORT'] = str(port_mappings['db'])
                    port_variables['POSTGRESQL_PORT'] = str(
                        port_mappings['db'])
                elif variant == 'mariadb':
                    port_variables['MARIADB_PORT'] = str(port_mappings['db'])
                    port_variables['MYSQL_PORT'] = str(
                        port_mappings['db'])  # For compatibility
                else:  # Default to MySQL
                    port_variables['MYSQL_PORT'] = str(port_mappings['db'])

            if 'admin' in port_mappings:
                port_variables['ADMIN_PORT'] = str(port_mappings['admin'])

                # Add admin tool-specific port names
                if variant == 'postgresql':
                    port_variables['PGADMIN_PORT'] = str(
                        port_mappings['admin'])
                else:
                    port_variables['PHPMYADMIN_PORT'] = str(
                        port_mappings['admin'])

            if 'frontend' in port_mappings:
                port_variables['FRONTEND_PORT'] = str(
                    port_mappings['frontend'])

            # Include all original port mappings with standard naming
            for service_name, port in port_mappings.items():
                port_variables[f"{service_name.upper()}_PORT"] = str(port)

            # Define variables for substitution
            variables = {
                'PROJECT_NAME': project_name,
                'DB_DATABASE': project_name,
                'DB_USERNAME': project_name,
                'DB_PASSWORD': 'secret',
                'DB_ROOT_PASSWORD': 'rootsecret',
                **port_variables
            }

            # Add variant to variables if provided
            if variant and variant != 'default':
                variables['VARIANT'] = variant
                variables['DB_ENGINE'] = variant

                # Also add database-specific environment variables
                if variant in ['mysql', 'postgresql', 'mariadb']:
                    variables['DB_TYPE'] = variant

                    # Set default port based on database type
                    if variant == 'postgresql':
                        variables['DB_DEFAULT_PORT'] = '5432'
                    else:
                        variables['DB_DEFAULT_PORT'] = '3306'

            # Process files
            self._process_project_files(target_dir, variables)

            # Display allocated ports
            self._print_port_mappings(port_mappings)

            # Show next steps guidance
            self._print_next_steps(
                target_dir, template_id, variant, port_mappings)

            return True

        except Exception as e:
            console.print(f"[red]Error creating project:[/] {str(e)}")
            if 'target_dir' in locals() and target_dir.exists():
                shutil.rmtree(target_dir)
            return False

    def _copy_component_files(self, components: dict, target_dir: Path) -> None:
        """Copy files from component templates."""
        for component_name, component_config in components.items():
            if not isinstance(component_config, dict):
                continue

            # Get component source path
            source = component_config.get('source')
            if not source:
                continue

            # Variables for string substitution in paths
            source_path_vars = {
                'DB_ENGINE': component_config.get('variant', 'mysql')}
            source = self._replace_path_variables(source, source_path_vars)

            # Resolve the actual component path
            component_path = self.templates_dir / source
            if not component_path.exists():
                console.print(
                    f"[yellow]Warning:[/] Component path not found: {source}")
                continue

            console.print(
                f"[green]Processing component:[/] {component_name} from {source}")

            # Check if component has its own template.yaml
            component_template = component_path / 'template.yaml'
            if component_template.exists():
                with open(component_template) as f:
                    comp_config = yaml.safe_load(f)

                # Copy Docker directory if it exists
                docker_dir = component_path / 'docker'
                if docker_dir.exists():
                    target_docker_dir = target_dir / 'docker'
                    target_docker_dir.mkdir(parents=True, exist_ok=True)

                    # Copy docker subdirectories
                    for item in docker_dir.glob('*'):
                        if item.is_dir():
                            target_subdirectory = target_docker_dir / item.name
                            target_subdirectory.mkdir(
                                parents=True, exist_ok=True)

                            # Special handling for nginx conf.d directory
                            if item.name == 'nginx' and (item / 'conf.d').exists():
                                nginx_conf_dir = target_docker_dir / 'nginx' / 'conf.d'
                                nginx_conf_dir.mkdir(
                                    parents=True, exist_ok=True)

                                # Copy and possibly modify nginx config files
                                for conf_file in (item / 'conf.d').glob('*.conf'):
                                    target_conf = nginx_conf_dir / conf_file.name

                                    # First read the content
                                    with open(conf_file, 'r') as f:
                                        conf_content = f.read()

                                    # If there's a public directory, adjust the root
                                    # If not, modify to use src/pages
                                    src_pages_exist = (
                                        component_path / 'src' / 'pages').exists()
                                    if src_pages_exist and 'root /var/www/html/public;' in conf_content:
                                        # Set up nginx to work with our file structure
                                        conf_content = conf_content.replace(
                                            'root /var/www/html/public;',
                                            'root /var/www/html;'
                                        )

                                    # Write the modified config
                                    with open(target_conf, 'w') as f:
                                        f.write(conf_content)

                                    self._verbose_print(
                                        f"[green]✓[/] Configured Nginx: {conf_file.name}")
                            else:
                                # Copy all files in subdirectory normally
                                for file in item.glob('**/*'):
                                    if file.is_file():
                                        rel_path = file.relative_to(item)
                                        dest_file = target_subdirectory / rel_path
                                        dest_file.parent.mkdir(
                                            parents=True, exist_ok=True)
                                        shutil.copy2(file, dest_file)

                    self._verbose_print(
                        f"[green]✓[/] Copied docker configuration from {component_name} component")

                # Copy src directory if it exists
                src_dir = component_path / 'src'
                if src_dir.exists() and src_dir.is_dir():
                    # Create target src dir if it doesn't exist
                    target_src_dir = target_dir / 'src'
                    target_src_dir.mkdir(parents=True, exist_ok=True)

                    # Copy all files in src directory
                    for file in src_dir.glob('**/*'):
                        if file.is_file():
                            rel_path = file.relative_to(src_dir)
                            dest_file = target_src_dir / rel_path
                            dest_file.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(file, dest_file)
                            self._verbose_print(
                                f"[green]✓[/] Copied src file: {rel_path}")

                # Copy www directory if it exists
                www_dir = component_path / 'www'
                if www_dir.exists() and www_dir.is_dir():
                    # Create target www dir if it doesn't exist
                    target_www_dir = target_dir / 'www'
                    target_www_dir.mkdir(parents=True, exist_ok=True)

                    # Copy all files in www directory
                    for file in www_dir.glob('**/*'):
                        if file.is_file():
                            rel_path = file.relative_to(www_dir)
                            dest_file = target_www_dir / rel_path
                            dest_file.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(file, dest_file)

                    self._verbose_print(
                        f"[green]✓[/] Copied www files from {component_name} component")

    def _replace_path_variables(self, path: str, variables: dict) -> str:
        """Replace variables in path string with their values."""
        result = path
        for key, value in variables.items():
            result = result.replace(f"${{{key}}}", value)
            result = result.replace(f"${key}", value)
        return result

    def _process_project_files(self, project_dir: Path, variables: dict) -> None:
        # First, try to process existing .env files
        env_file = project_dir / '.env.example'
        if env_file.exists():
            self._process_env_file(env_file, project_dir / '.env', variables)

        # Process all .env.*.example files
        env_files = list(project_dir.glob('.env.*.example'))
        if env_files:
            for env_file in env_files:
                self._process_env_file(
                    env_file, project_dir / '.env', variables)
        else:
            # If no .env files exist, create one with our variables
            self._create_default_env_file(project_dir, variables)

        # Process all docker-compose*.yml files
        compose_files = list(project_dir.glob('docker-compose*.yml'))
        for compose_file in compose_files:
            self._process_yaml_file(compose_file, variables, is_compose=True)

        # Process any PHP template files
        php_templates = list(project_dir.glob('**/*.template'))
        for template_file in php_templates:
            target_file = template_file.parent / \
                template_file.name.replace('.template', '')
            self._process_template_file(template_file, target_file, variables)

        # Ensure docker-compose.yml exists (copy from base if needed)
        if not project_dir.joinpath('docker-compose.yml').exists():
            if project_dir.joinpath('docker-compose.base.yml').exists():
                shutil.copy2(
                    project_dir.joinpath('docker-compose.base.yml'),
                    project_dir.joinpath('docker-compose.yml')
                )
                # Process the copied file
                self._process_yaml_file(project_dir.joinpath(
                    'docker-compose.yml'), variables, is_compose=True)
                self._verbose_print(
                    "[green]✓[/] Created docker-compose.yml from base template")

            # Look for variant-specific compose file
            elif 'DB_ENGINE' in variables:
                variant = variables['DB_ENGINE']
                variant_file = project_dir / f"docker-compose.{variant}.yml"
                if variant_file.exists():
                    shutil.copy2(variant_file, project_dir /
                                 'docker-compose.yml')
                    # Process the copied file
                    self._process_yaml_file(project_dir.joinpath(
                        'docker-compose.yml'), variables, is_compose=True)
                    self._verbose_print(
                        f"[green]✓[/] Created docker-compose.yml from {variant} template")

        # Create public directory with proper router
        public_dir = project_dir / 'public'
        public_dir.mkdir(parents=True, exist_ok=True)

        # Check if www/index.php exists with routing logic
        www_index = project_dir / 'www' / 'index.php'
        if www_index.exists():
            # Copy the original routing logic to public/index.php
            shutil.copy2(www_index, public_dir / 'index.php')
            self._verbose_print(
                "[green]✓[/] Copied routing logic to public/index.php")
        else:
            # Create an index.php file with proper routing
            index_content = """<?php
declare(strict_types=1);

// Bootstrap the application
require_once __DIR__ . '/../src/bootstrap.php';

// Parse the URI
$uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

// Simple router
switch ($uri) {
    case '/':
        // Include the home page
        if (file_exists(__DIR__ . '/../src/pages/home.php')) {
            require_once __DIR__ . '/../src/pages/home.php';
        } else {
            echo "<h1>Welcome to ChimeraStack</h1>";
            echo "<p>Your development environment is ready!</p>";
        }
        break;
    case '/info':
        // Show PHP info
        phpinfo();
        break;
    case '/health':
        // Health check endpoint
        header('Content-Type: text/plain');
        echo 'healthy';
        break;
    default:
        // 404 Not Found
        http_response_code(404);
        echo "<h1>404 Not Found</h1>";
        echo "<p>The requested resource could not be found.</p>";
        break;
}
"""
            with open(public_dir / 'index.php', 'w') as f:
                f.write(index_content)

            self._verbose_print(
                "[green]✓[/] Created public/index.php with routing logic")

        # Fix Nginx configuration to ensure proper document root
        nginx_conf = project_dir / 'docker/nginx/conf.d/default.conf'
        if nginx_conf.exists():
            try:
                with open(nginx_conf, 'r') as f:
                    conf_content = f.read()

                # Make sure root is set correctly - should always point to public
                if not 'root /var/www/html/public;' in conf_content:
                    # Update Nginx config to point to the public directory
                    conf_content = conf_content.replace(
                        'root /var/www/html;',
                        'root /var/www/html/public;'
                    )

                    with open(nginx_conf, 'w') as f:
                        f.write(conf_content)

                    self._verbose_print(
                        "[green]✓[/] Updated Nginx configuration")
            except Exception as e:
                console.print(
                    f"[yellow]Warning: Could not update Nginx configuration: {str(e)}[/]")

        # Clean up redundant files and directories
        self._cleanup_project_structure(project_dir)

    def _cleanup_project_structure(self, project_dir: Path) -> None:
        """Remove redundant files and directories to create a cleaner project structure."""
        try:
            # Get the DB_ENGINE from the .env file if it exists
            db_engine = None
            env_path = project_dir / '.env'
            if env_path.exists():
                try:
                    with open(env_path, 'r') as f:
                        for line in f:
                            if line.startswith('DB_ENGINE='):
                                db_engine = line.strip().split('=', 1)[1]
                                break
                except Exception:
                    pass

            # Remove redundant files
            redundant_files = [
                'docker-compose.base.yml',  # Keep only the main docker-compose.yml
            ]

            # Also remove any variant-specific docker-compose files that aren't our current variant
            if db_engine:
                # Always remove all variant docker-compose files - we only need docker-compose.yml
                variant_files = [
                    'docker-compose.mysql.yml',
                    'docker-compose.mariadb.yml',
                    'docker-compose.postgresql.yml',
                    'docker-compose.pgsql.yml'
                ]
                redundant_files.extend(variant_files)

            # Handle the case where we have a docker-compose.yml that wasn't properly updated
            # This can happen when the variant-specific docker-compose wasn't properly copied
            if db_engine and db_engine != 'mysql':
                # Handle both naming conventions for PostgreSQL
                if db_engine == 'postgresql':
                    variant_files = [project_dir / 'docker-compose.postgresql.yml',
                                     project_dir / 'docker-compose.pgsql.yml']
                    variant_compose = next(
                        (f for f in variant_files if f.exists()), None)
                else:
                    variant_compose = project_dir / \
                        f"docker-compose.{db_engine}.yml"

                main_compose = project_dir / "docker-compose.yml"

                if variant_compose and variant_compose.exists() and main_compose.exists():
                    # Check if we're using the wrong database in docker-compose.yml
                    with open(main_compose, 'r') as f:
                        compose_content = f.read()

                    # Check for incorrect database configurations
                    wrong_db_config = False
                    if db_engine == 'postgresql':
                        if "image: mysql:" in compose_content or "image: mariadb:" in compose_content:
                            wrong_db_config = True
                    elif db_engine == 'mariadb':
                        if "image: mysql:" in compose_content or "image: postgres:" in compose_content:
                            wrong_db_config = True
                    elif db_engine == 'mysql':
                        if "image: mariadb:" in compose_content or "image: postgres:" in compose_content:
                            wrong_db_config = True

                    if wrong_db_config:
                        console.print(
                            f"[yellow]Warning:[/] docker-compose.yml using incorrect database. Replacing with {db_engine} version.")

                        # Replace with the correct variant file
                        shutil.copy2(variant_compose, main_compose)

                        # Process the new file to ensure variables are properly substituted
                        from pathlib import Path
                        env_vars = {}
                        if env_path.exists():
                            with open(env_path, 'r') as f:
                                for line in f:
                                    if '=' in line and not line.startswith('#'):
                                        key, value = line.strip().split('=', 1)
                                        env_vars[key] = value

                        self._process_yaml_file(
                            main_compose, env_vars, is_compose=True)
                        console.print(
                            f"[green]✓[/] Updated docker-compose.yml to use {db_engine}")

            for file in redundant_files:
                file_path = project_dir / file
                if file_path.exists():
                    file_path.unlink()
                    self._verbose_print(
                        f"[green]✓[/] Removed redundant file: {file}")

            # Remove redundant directories if they're empty
            redundant_dirs = [
                'config',  # Empty config directory not needed with .env file
                'www',     # Consolidated to public directory
            ]

            # Remove database-related directories that don't match the current engine
            if db_engine == 'mariadb' or db_engine == 'postgresql':
                if (project_dir / 'docker/mysql').exists():
                    redundant_dirs.append('docker/mysql')

            if db_engine == 'mysql' or db_engine == 'postgresql':
                if (project_dir / 'docker/mariadb').exists():
                    redundant_dirs.append('docker/mariadb')

            if db_engine == 'mysql' or db_engine == 'mariadb':
                if (project_dir / 'docker/postgres' or project_dir / 'docker/postgresql').exists():
                    redundant_dirs.append('docker/postgres')
                    redundant_dirs.append('docker/postgresql')

            for directory in redundant_dirs:
                dir_path = project_dir / directory
                if dir_path.exists() and not any(dir_path.iterdir()):
                    dir_path.rmdir()
                    self._verbose_print(
                        f"[green]✓[/] Removed empty directory: {directory}")
                elif dir_path.exists() and directory == 'www':
                    # If www exists and has content, we've already copied what we need
                    # to public/, so it's safe to remove
                    shutil.rmtree(dir_path)
                    self._verbose_print(
                        f"[green]✓[/] Removed redundant directory: {directory}")
                elif dir_path.exists() and directory.startswith('docker/'):
                    # Remove conflicting database directories
                    shutil.rmtree(dir_path)
                    self._verbose_print(
                        f"[green]✓[/] Removed conflicting directory: {directory}")

            # Create an informative README.md if it doesn't exist
            readme_path = project_dir / 'README.md'
            self._create_readme(project_dir, readme_path)

        except Exception as e:
            console.print(
                f"[yellow]Warning: Could not clean up project structure: {str(e)}[/]")

    def _create_readme(self, project_dir: Path, readme_path: Path) -> None:
        """Create a README.md file with template-specific instructions."""

        # Try to load port settings from .env file
        env_path = project_dir / '.env'
        env_vars = {}
        if env_path.exists():
            try:
                with open(env_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            env_vars[key.strip()] = value.strip()
            except Exception:
                pass

        # Default port values if not found in .env
        web_port = env_vars.get('WEB_PORT', env_vars.get('NGINX_PORT', '8000'))
        db_port = env_vars.get('DB_PORT', '3306')
        admin_port = env_vars.get('ADMIN_PORT', env_vars.get(
            'PHPMYADMIN_PORT', env_vars.get('PGADMIN_PORT', '8080')))

        # Check for DB_ENGINE in env vars first
        db_engine = env_vars.get('DB_ENGINE', '').lower()

        # If no DB_ENGINE in env, determine based on directory structure
        if not db_engine:
            has_mysql = (project_dir / 'docker/mysql').exists()
            has_postgres = (project_dir / 'docker/postgres').exists() or (
                project_dir / 'docker/postgresql').exists()
            has_mariadb = (project_dir / 'docker/mariadb').exists()

            if has_mariadb:
                db_engine = 'mariadb'
            elif has_postgres:
                db_engine = 'postgresql'
            elif has_mysql:
                db_engine = 'mysql'
            else:
                db_engine = 'mysql'  # Default

        # Define database type based on engine
        db_type_mapping = {
            'mysql': 'MySQL',
            'mariadb': 'MariaDB',
            'postgresql': 'PostgreSQL'
        }
        db_type = db_type_mapping.get(db_engine, 'MySQL')

        # Define admin tool based on engine
        admin_tool_mapping = {
            'mysql': 'phpMyAdmin',
            'mariadb': 'phpMyAdmin',
            'postgresql': 'pgAdmin'
        }
        admin_tool = admin_tool_mapping.get(db_engine, 'phpMyAdmin')

        # Define host name based on engine
        host_mapping = {
            'mysql': 'mysql',
            'mariadb': 'mariadb',
            'postgresql': 'postgresql'
        }
        db_host = host_mapping.get(db_engine, db_engine)

        # Get project name
        project_name = project_dir.name

        # For specific DB engines, include special badge or logo
        db_badge = ""
        if db_engine == 'mariadb':
            db_badge = "\n[![MariaDB](https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white)](https://mariadb.org/)"
        elif db_engine == 'postgresql':
            db_badge = "\n[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)"
        elif db_engine == 'mysql':
            db_badge = "\n[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)"

        # Build template-specific README content
        content = f"""# {project_name}{db_badge}

A PHP development environment with {db_type} database created with ChimeraStack CLI.

## 🚀 Quick Start

1. **Start the environment**:
   ```bash
   docker-compose up -d
   ```

2. **Stop the environment**:
   ```bash
   docker-compose down
   ```

## 📋 Stack Components

| Component | Description | Access |
|-----------|-------------|--------|
| Nginx | Web server | http://localhost:{web_port} |
| PHP-FPM | PHP FastCGI Process Manager | N/A (Internal) |
| {db_type} | Database server | localhost:{db_port} |
| {admin_tool} | Database administration | http://localhost:{admin_port} |

## 🔧 Project Structure

- `docker/` - Docker configuration files
  - `nginx/` - Nginx web server configuration
  - `php/` - PHP-FPM configuration and Dockerfile
  {f"  - `postgresql/` - {db_type} database configuration" if db_engine == 'postgresql' else f"  - `{db_engine}/` - {db_type} database configuration"}
- `public/` - Web server document root (place your public files here)
- `src/` - Application source code (PHP classes and logic)
  - `pages/` - PHP page templates
  - `bootstrap.php` - Application initialization

## 💻 Development Workflow

1. **PHP Files**: Place all your PHP application files in the `src/` directory
2. **Public Assets**: Place publicly accessible files (index.php, images, CSS, JS) in the `public/` directory

## 📦 Database Access

- **Host**: {db_host.lower()}
- **Database**: {project_name}
- **Username**: {project_name}
- **Password**: secret
{'' if db_engine == 'postgresql' else '- **Root Password**: rootsecret'}

You can connect to the database using {admin_tool} at http://localhost:{admin_port} or use any database client.

## ⚙️ Configuration

Environment variables are stored in the `.env` file. Edit this file to change:
- Port mappings
- Database credentials
- PHP configuration

## 🐞 Troubleshooting

- **Container Issues**: Check container status with `docker-compose ps`
- **Logs**: View container logs with `docker-compose logs [service]`
- **PHP Configuration**: Modify PHP settings in `docker/php/php.ini`
- **Web Server Issues**: Check Nginx configuration in `docker/nginx/conf.d/default.conf`
"""

        # Write the README file
        with open(readme_path, 'w') as f:
            f.write(content)

        self._verbose_print(
            f"[green]✓[/] Created detailed README.md with helpful information")

    def _create_default_env_file(self, project_dir: Path, variables: dict) -> None:
        """Create a default .env file with essential variables when none exists in the template."""
        env_path = project_dir / '.env'
        db_engine = variables.get('DB_ENGINE', 'mysql')

        # Build comprehensive environment variables content
        env_content = f"""# Project Settings
PROJECT_NAME={variables.get('PROJECT_NAME', 'chimera-project')}

# Web Server
NGINX_PORT={variables.get('NGINX_PORT', variables.get('WEB_PORT', '8000'))}
WEB_PORT={variables.get('WEB_PORT', variables.get('NGINX_PORT', '8000'))}

# PHP Configuration
PHP_VERSION=8.1
PHP_DISPLAY_ERRORS=On
PHP_ERROR_REPORTING=E_ALL

# Database Configuration
DB_HOST={db_engine if db_engine != 'mariadb' else 'mariadb'}
# External port mapping - inside Docker, the internal port remains standard (3306 for MySQL/MariaDB, 5432 for PostgreSQL)
DB_PORT={variables.get('DB_PORT', '3306' if db_engine in ['mysql', 'mariadb'] else '5432')}
DB_ENGINE={db_engine}
DB_DATABASE={variables.get('DB_DATABASE', variables.get('PROJECT_NAME', 'chimera-project'))}
DB_USERNAME={variables.get('DB_USERNAME', variables.get('PROJECT_NAME', 'chimera-project'))}
DB_PASSWORD={variables.get('DB_PASSWORD', 'secret')}
DB_ROOT_PASSWORD={variables.get('DB_ROOT_PASSWORD', 'rootsecret')}
"""

        # Add database-specific variables
        if db_engine == 'mysql' or db_engine == 'mariadb':
            env_content += f"MYSQL_PORT={variables.get('DB_PORT', '3306')}\n"
        elif db_engine == 'postgresql':
            env_content += f"POSTGRES_PORT={variables.get('DB_PORT', '5432')}\n"

        # Add admin tool variables
        if db_engine in ['mysql', 'mariadb'] and any(k for k in variables if 'PHPMYADMIN' in k or 'ADMIN_PORT' in k):
            env_content += f"""
# phpMyAdmin Configuration
PHPMYADMIN_PORT={variables.get('PHPMYADMIN_PORT', variables.get('ADMIN_PORT', '8080'))}
PMA_HOST={db_engine}
"""
        elif db_engine == 'postgresql' and any(k for k in variables if 'PGADMIN' in k or 'ADMIN_PORT' in k or True):
            env_content += f"""
# pgAdmin Configuration
PGADMIN_PORT={variables.get('PGADMIN_PORT', variables.get('ADMIN_PORT', '8080'))}
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD={variables.get('DB_PASSWORD', 'secret')}
"""

        # Add development settings
        env_content += """
# Development Settings
APP_ENV=local
APP_DEBUG=true
"""

        # Write the file
        with open(env_path, 'w') as f:
            f.write(env_content)

        self._verbose_print(
            f"[green]✓[/] Created .env file with {db_engine} configuration")

    def _process_yaml_file(self, file_path: Path, variables: dict, is_compose: bool = False) -> None:
        try:
            with open(file_path) as f:
                content = yaml.safe_load(f)

            if is_compose:
                project_name = variables['PROJECT_NAME']

                # Handle DB_HOST specifically for MariaDB
                if 'DB_ENGINE' in variables and variables['DB_ENGINE'] == 'mariadb':
                    # Find services using DB_HOST env var
                    for service_name, service in content.get('services', {}).items():
                        if 'environment' in service and isinstance(service['environment'], dict):
                            # If a service has DB_HOST env var, set it to 'mariadb'
                            if 'DB_HOST' in service['environment']:
                                service['environment']['DB_HOST'] = 'mariadb'
                        elif 'environment' in service and isinstance(service['environment'], list):
                            # For array-style environment variables
                            for i, env_var in enumerate(service['environment']):
                                if isinstance(env_var, str) and env_var.startswith('DB_HOST='):
                                    service['environment'][i] = 'DB_HOST=mariadb'

                # Ensure PHP service has DB environment variables
                if 'services' in content and 'php' in content['services']:
                    php_service = content['services']['php']
                    # Create environment section if it doesn't exist
                    if 'environment' not in php_service:
                        php_service['environment'] = {}

                    # If environment is a list, convert to dict for easier manipulation
                    if isinstance(php_service['environment'], list):
                        env_dict = {}
                        for env_var in php_service['environment']:
                            if isinstance(env_var, str) and '=' in env_var:
                                key, value = env_var.split('=', 1)
                                env_dict[key] = value
                        php_service['environment'] = env_dict

                    # Add database environment variables
                    db_vars = {
                        'DB_HOST': variables.get('DB_ENGINE', 'mysql') if variables.get('DB_ENGINE', 'mysql') not in ['mariadb', 'postgresql'] else variables.get('DB_ENGINE', 'mysql'),
                        # Use internal container port
                        'DB_PORT': '3306' if variables.get('DB_ENGINE', 'mysql') in ['mysql', 'mariadb'] else '5432',
                        'DB_DATABASE': variables.get('DB_DATABASE', project_name),
                        'DB_USERNAME': variables.get('DB_USERNAME', project_name),
                        'DB_PASSWORD': variables.get('DB_PASSWORD', 'secret'),
                        'DB_ENGINE': variables.get('DB_ENGINE', 'mysql')
                    }

                    # Add or update environment variables
                    for key, value in db_vars.items():
                        php_service['environment'][key] = value

                # Update services
                for service_name, service in content.get('services', {}).items():
                    service['container_name'] = f"{project_name}-{service_name}"

                    # Update ports if defined
                    if 'ports' in service and isinstance(service['ports'], list):
                        for i, port_mapping in enumerate(service['ports']):
                            if ':' in str(port_mapping):
                                host_port, container_port = str(
                                    port_mapping).split(':')

                                # Replace variable references
                                if host_port.startswith('${') and host_port.endswith('}'):
                                    var_name = host_port[2:-1]
                                    if var_name in variables:
                                        service['ports'][i] = f"{variables[var_name]}:{container_port}"

                # Update networks
                if 'networks' in content:
                    for network_name, network in content['networks'].items():
                        if isinstance(network, dict) and 'name' in network:
                            # Ensure we don't have duplicated project name
                            if network['name'].startswith(f"${{{project_name}}}") or network['name'].startswith(f"${project_name}"):
                                network['name'] = f"{project_name}_network"
                            else:
                                network[
                                    'name'] = f"{project_name}_{network['name'].replace('${PROJECT_NAME}_', '')}"

                # Update volumes
                if 'volumes' in content:
                    for volume_name, volume in content['volumes'].items():
                        if isinstance(volume, dict) and 'name' in volume:
                            # Fix volume naming - prevent double project prefixing
                            volume_base_name = volume['name']
                            # Replace any variable reference first
                            if "${PROJECT_NAME}" in volume_base_name:
                                volume_base_name = volume_base_name.replace(
                                    "${PROJECT_NAME}", project_name)
                                volume_base_name = volume_base_name.replace(
                                    "${PROJECT_NAME}_", "")

                            # Check if the volume name already starts with the project name
                            if volume_base_name.startswith(f"{project_name}_"):
                                volume['name'] = volume_base_name
                            else:
                                volume['name'] = f"{project_name}_{volume_base_name}"

            # Replace variables
            content_str = yaml.dump(content)
            for key, value in variables.items():
                content_str = content_str.replace(f"${{{key}}}", str(value))
                content_str = content_str.replace(f"${key}", str(value))

            with open(file_path, 'w') as f:
                f.write(content_str)

            self._verbose_print(f"[green]✓[/] Processed: {file_path}")
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

            self._verbose_print(
                f"[green]✓[/] Environment file processed: {dest_path}")
        except Exception as e:
            console.print(
                f"[red]Error processing environment file:[/] {str(e)}")
            raise

    def _print_port_mappings(self, port_mappings: Dict[str, int]) -> None:
        console.print("\n[bold]Port Allocations:[/]")
        for service, port in port_mappings.items():
            console.print(f"  {service}: [cyan]localhost:{port}[/]")

    def _allocate_service_ports(self, template_config: dict) -> Dict[str, int]:
        port_mappings = {}

        # Get Docker port scanner to check for used ports
        used_ports = self.port_scanner.scan()['ports']

        # Check for service definitions
        services = template_config.get('services', {})
        components = template_config.get('components', {})
        stack_config = template_config.get('stack', {})
        welcome_config = template_config.get('welcome_page', {})

        # Process standard services (old format)
        for service_name, service_config in services.items():
            port_type = service_config.get('type')
            if not port_type:
                continue

            env_prefix = service_config.get('env_prefix', '').lower()
            port_range = service_config.get('port_range')

            if not port_range:
                continue

            port = self._find_available_port(port_range, used_ports)
            if port is None:
                console.print(
                    f"[red]Could not allocate port for {service_name} in range {port_range}[/]")
                return {}

            port_mappings[env_prefix or service_name] = port
            used_ports.add(port)  # Mark port as used

        # Process components (new format)
        for component_name, component_config in components.items():
            # Skip if not a dictionary with config
            if not isinstance(component_config, dict) or 'config' not in component_config:
                continue

            config = component_config.get('config', {})
            port_range = config.get('port_range')
            env_prefix = config.get('env_prefix', '').lower()

            if not port_range:
                continue

            port = self._find_available_port(port_range, used_ports)
            if port is None:
                console.print(
                    f"[red]Could not allocate port for {component_name} in range {port_range}[/]")
                return {}

            port_mappings[env_prefix or component_name] = port
            used_ports.add(port)  # Mark port as used

        # Ensure standard service ports are defined
        default_ports = {
            'frontend': '3000-3999',
            'web': '8000-8999',
            'db': '3306-3399',
            'admin': '8080-8099'
        }

        # Check compose files for expected service names
        # This is temporary until all templates are migrated to new format
        template_services = []
        for compose_file in self.templates_dir.glob('**/docker-compose*.yml'):
            try:
                with open(compose_file) as f:
                    compose_data = yaml.safe_load(f)
                    if compose_data and 'services' in compose_data:
                        template_services.extend(
                            compose_data['services'].keys())
            except:
                pass

        # Add required service ports based on template services
        if 'nginx' in template_services and 'web' not in port_mappings:
            port = self._find_available_port('8000-8999', used_ports)
            if port is None:
                console.print(f"[red]Could not allocate port for nginx/web[/]")
                return {}
            port_mappings['web'] = port
            used_ports.add(port)

        # Check welcome page for expected services
        welcome_sections = welcome_config.get('sections', [])
        for section in welcome_sections:
            service = section.get('service', '').lower()
            port_key = section.get('port_env', '').lower(
            ) or section.get('env_prefix', '').lower()

            # If service is defined but no port mapping exists
            if service and port_key and port_key not in port_mappings:
                port_range = default_ports.get(
                    service) or default_ports.get(port_key)
                if port_range:
                    port = self._find_available_port(port_range, used_ports)
                    if port is None:
                        console.print(
                            f"[red]Could not allocate port for {service}[/]")
                        return {}
                    port_mappings[port_key] = port
                    used_ports.add(port)

        # Add default ports for common services if not already allocated
        core_services = ['db', 'admin']
        for key in core_services:
            if key not in port_mappings:
                port_range = default_ports[key]
                port = self._find_available_port(port_range, used_ports)
                if port is None:
                    console.print(f"[red]Could not allocate port for {key}[/]")
                    return {}
                port_mappings[key] = port
                used_ports.add(port)

        # Always allocate web port for PHP templates
        if 'web' not in port_mappings:
            port = self._find_available_port('8000-8999', used_ports)
            if port is None:
                console.print(
                    f"[red]Could not allocate port for web server[/]")
                return {}
            port_mappings['web'] = port

        return port_mappings

    def _find_available_port(self, port_range: str, used_ports: set) -> int:
        """Find an available port in the given range."""
        try:
            start, end = map(int, port_range.split('-'))
            for port in range(start, end + 1):
                if port not in used_ports:
                    return port
            return None
        except Exception:
            return None

    def _print_next_steps(self, project_dir: Path, template_id: str, variant: str, port_mappings: Dict[str, int]) -> None:
        """Display helpful next steps after project creation."""
        relative_path = project_dir.relative_to(
            Path.cwd()) if project_dir.is_relative_to(Path.cwd()) else project_dir

        console.print("\n[bold green]✓ Project created successfully![/]")
        console.print("\n[bold]Next steps:[/]")
        console.print(f"  1. [yellow]cd[/] [cyan]{relative_path}[/]")
        console.print(
            f"  2. [yellow]docker-compose up -d[/] [dim](Start the development environment)[/]")

        # Template-specific instructions based on template_id
        if 'php' in template_id:
            web_port = port_mappings.get('web', 8000)
            admin_port = port_mappings.get('admin', 8080)

            console.print("\n[bold]Access your development environment:[/]")
            console.print(f"  • [cyan]Website:[/] http://localhost:{web_port}")

            if 'mysql' in variant or 'mariadb' in variant:
                console.print(
                    f"  • [cyan]phpMyAdmin:[/] http://localhost:{admin_port}")
            elif 'postgresql' in variant:
                console.print(
                    f"  • [cyan]pgAdmin:[/] http://localhost:{admin_port}")

            console.print("\n[bold]Development:[/]")
            console.print(
                "  • Place your PHP files in the [cyan]src/[/] directory")
            console.print(
                "  • Web server is configured to serve from [cyan]public/[/] directory")
            console.print("  • View the README.md file for more details")

    def _process_template_file(self, template_file: Path, target_file: Path, variables: dict) -> None:
        """Process PHP template files and replace variables."""
        try:
            with open(template_file) as f:
                template_content = f.read()

            # Replace variables in the template content
            for key, value in variables.items():
                template_content = template_content.replace(
                    f"${{{key}}}", str(value))
                template_content = template_content.replace(
                    f"${key}", str(value))

            # Special handling for PHP index.html templates with database information
            if template_file.name == 'index.html.template':
                # Specifically fix PostgreSQL port references
                if variables.get('DB_ENGINE') == 'postgresql':
                    # Ensure PGADMIN_PORT is used correctly
                    if 'PGADMIN_PORT' in variables and 'localhost:8081' in template_content:
                        template_content = template_content.replace(
                            'localhost:8081', f'localhost:{variables["PGADMIN_PORT"]}')

            # Write the processed content to the target file
            with open(target_file, 'w') as f:
                f.write(template_content)

            self._verbose_print(
                f"[green]✓[/] Processed template: {template_file} -> {target_file}")
        except Exception as e:
            console.print(f"[red]Error processing PHP template: {str(e)}")
            raise

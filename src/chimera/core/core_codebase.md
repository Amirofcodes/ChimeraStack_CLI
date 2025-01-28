# **init**.py

```py
# src/chimera/core/__init__.py

from .template_manager import TemplateManager
from .port_scanner import PortScanner
from .port_allocator import PortAllocator

__all__ = ['TemplateManager', 'PortScanner', 'PortAllocator']
```

# port_allocator.py

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
               'postgres': PortRange(5432, 5532)
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

       # Find available port
       for port in range(port_range.start, port_range.end + 1):
           if port not in used_ports and port not in port_range.allocated:
               port_range.allocated.add(port)
               return port

       return None

   def release_port(self, port: int) -> None:
       for ranges in self.ranges.values():
           for port_range in ranges.values():
               if port in port_range.allocated:
                   port_range.allocated.remove(port)
                   return
```

# port_scanner.py

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

        # Get both running and stopped containers
        containers = self.docker_client.containers.list(all=True)

        for container in containers:
            # Get port mappings from container config
            ports = container.attrs['NetworkSettings']['Ports'] or {}
            host_config = container.attrs['HostConfig']['PortBindings'] or {}

            # Check both current and configured port bindings
            for port_map in ports.values():
                if port_map:
                    self.used_ports.add(int(port_map[0]['HostPort']))

            for port_map in host_config.values():
                if port_map:
                    self.used_ports.add(int(port_map[0]['HostPort']))

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

# template_manager.py

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

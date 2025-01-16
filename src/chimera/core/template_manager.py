"""
Template management system for ChimeraStack CLI.
"""
from pathlib import Path
from typing import Dict, List
import shutil
import yaml
from rich.console import Console

console = Console()

class TemplateManager:
    """Manages discovery, validation, and loading of project templates."""
    
    def __init__(self, templates_dir: Path | str = None):
        """Initialize the template manager."""
        if templates_dir is None:
            # Default to the templates directory in the package
            templates_dir = Path(__file__).parent.parent / 'templates'
        self.templates_dir = Path(templates_dir)
    
    def get_available_templates(self) -> List[Dict[str, str]]:
        """Get list of available templates with metadata."""
        templates = []
        # Walk through template directories
        for template_path in self.templates_dir.glob('**/*'):
            if template_path.is_dir() and self._is_valid_template(template_path):
                template_info = self._get_template_info(template_path)
                if template_info:
                    templates.append(template_info)
        return templates

    def _is_valid_template(self, path: Path) -> bool:
        """Check if directory contains a valid template."""
        # A valid template must have:
        # 1. docker-compose.yml
        # 2. Template configuration (template.yaml)
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
                'path': str(path)
            }
        except Exception as e:
            console.print(f"[red]Error reading template config from {path}: {str(e)}")
            return None

    def get_template(self, template_id: str) -> Dict[str, str] | None:
        """Get specific template by ID."""
        template_path = self.templates_dir / template_id
        if self._is_valid_template(template_path):
            return self._get_template_info(template_path)
        return None

    def create_project(self, template_id: str, project_name: str, target_dir: Path | str = None) -> bool:
        """Create a new project from a template."""
        try:
            # Get template path
            template_path = self.templates_dir / template_id
            if not self._is_valid_template(template_path):
                console.print(f"[red]Error:[/] Template {template_id} not found or invalid")
                return False
                
            # Determine target directory
            if target_dir is None:
                target_dir = Path.cwd() / project_name
            else:
                target_dir = Path(target_dir) / project_name
                
            # Check if directory already exists
            if target_dir.exists():
                console.print(f"[red]Error:[/] Directory {target_dir} already exists")
                return False
                
            # Copy template files
            shutil.copytree(template_path, target_dir, ignore=shutil.ignore_patterns('template.yaml'))
            
            # Define variables for substitution
            variables = {
                'PROJECT_NAME': project_name,
                'DB_DATABASE': project_name,
                'DB_USERNAME': project_name,
                'DB_PASSWORD': 'secret',
                'DB_ROOT_PASSWORD': 'rootsecret'
            }
            
            # Process environment files
            if (target_dir / '.env.example').exists():
                self._process_env_file(target_dir / '.env.example', target_dir / '.env', variables)
                
            # Process docker-compose.yml
            self._process_yaml_file(target_dir / 'docker-compose.yml', variables)
                
            # Process development.yaml
            self._process_yaml_file(target_dir / 'config/development.yaml', variables)
            
            console.print(f"[green]✓[/] Project created successfully at {target_dir}")
            return True
            
        except Exception as e:
            console.print(f"[red]Error creating project:[/] {str(e)}")
            # If something went wrong, try to clean up
            if 'target_dir' in locals() and target_dir.exists():
                shutil.rmtree(target_dir)
            return False

    def _process_yaml_file(self, file_path: Path, variables: dict) -> None:
        """Process YAML files, replacing variables."""
        try:
            with open(file_path) as f:
                content = f.read()
            
            # Replace variables
            for key, value in variables.items():
                content = content.replace(f"${{{key}}}", str(value))
                content = content.replace(f"${key}", str(value))
            
            with open(file_path, 'w') as f:
                f.write(content)
                
            console.print(f"[green]✓[/] Processed: {file_path}")
        except Exception as e:
            console.print(f"[red]Error processing {file_path}:[/] {str(e)}")
            raise

    def _process_env_file(self, src_path: Path, dest_path: Path, variables: dict) -> None:
        """Process environment file, replacing variables."""
        try:
            with open(src_path) as f:
                content = f.read()
            
            # Replace variables
            for key, value in variables.items():
                content = content.replace(f"${{{key}}}", str(value))
                content = content.replace(f"${key}", str(value))
            
            with open(dest_path, 'w') as f:
                f.write(content)
                
            console.print(f"[green]✓[/] Environment file processed: {dest_path}")
        except Exception as e:
            console.print(f"[red]Error processing environment file:[/] {str(e)}")
            raise

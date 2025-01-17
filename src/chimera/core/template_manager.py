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
            templates_dir = Path(__file__).parent.parent / 'templates'
        self.templates_dir = Path(templates_dir)
    
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

# __init__.py

```py
"""
Command implementations for the ChimeraStack CLI.
"""

from .create import create_command
from .list import list_command

__all__ = ['create_command', 'list_command']

```

# create.py

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

# list.py

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


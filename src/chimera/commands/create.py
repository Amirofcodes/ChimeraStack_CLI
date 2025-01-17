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

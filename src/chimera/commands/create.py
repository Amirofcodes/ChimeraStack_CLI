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
        templates = template_manager.get_available_templates()
        
        if not template:
            # If no template is specified, show interactive selection
            choices = [
                {
                    'name': f"{t['id']} - {t['description']}",
                    'value': t['id']
                }
                for t in templates
            ]
            
            template = questionary.select(
                "Choose a template:",
                choices=choices,
                use_indicator=True
            ).ask()
            
            if not template:
                console.print("[red]Template selection cancelled[/]")
                return
        
        console.print(f"Creating project [bold blue]{name}[/] using template [bold green]{template}[/]")
        template_manager.create_project(template, name)
        
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")
        raise

"""
Implementation of the list command.
"""
from rich.console import Console
from rich.table import Table
from chimera.core import TemplateManager

console = Console()

def list_command() -> None:
    """List all available templates."""
    try:
        template_manager = TemplateManager()
        templates = template_manager.get_available_templates()
        
        table = Table(title="Available Templates")
        table.add_column("Template", style="cyan")
        table.add_column("Type", style="green")
        table.add_column("Description", style="white")
        
        for template in templates:
            table.add_row(
                template['id'],
                template.get('type', ''),
                template.get('description', '')
            )
        
        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")
        raise

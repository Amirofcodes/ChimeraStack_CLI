"""
Implementation of the list command.
"""
import click
from rich.console import Console
from rich.table import Table

console = Console()

def list_command() -> None:
    """List all available templates."""
    try:
        table = Table(title="Available Templates")
        table.add_column("Template", style="cyan")
        table.add_column("Type", style="green")
        table.add_column("Description", style="white")
        
        # TODO: Implement template discovery and listing
        table.add_row("php/nginx/mysql", "PHP", "Basic PHP environment with MySQL")
        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")
        raise

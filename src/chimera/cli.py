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

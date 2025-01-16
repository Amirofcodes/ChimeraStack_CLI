"""
ChimeraStack CLI entry point.
"""
import click
from rich.console import Console
from rich.traceback import install

from chimera import __version__
from chimera.commands import create_command, list_command

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
@click.option('--template', '-t', help='Template to use for the project')
def create(name: str, template: str | None = None):
    """Create a new project from a template."""
    create_command(name, template)

@cli.command()
def list():
    """List available templates."""
    list_command()

def main():
    try:
        cli()
    except Exception as e:
        console.print_exception()
        exit(1)

if __name__ == '__main__':
    main()

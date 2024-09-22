import click

@click.group()
def cli():
    """Tick Manager CLI"""
    pass

@cli.command()
def greet():
    """Greet the user."""
    click.echo("Hello, Tick Manager!")


import click
from click import ClickException

from tick_manager.operations.core import add, divide, multiply, subtract


@click.group()
def cli() -> None:
    """Tick Manager CLI"""
    pass


@cli.command()
def greet() -> None:
    """Greet the user."""
    click.echo("Hello, Tick Manager!")


@cli.command()
@click.argument("a", type=float)
@click.argument("b", type=float)
def add_cmd(a: float, b: float) -> None:
    """Add two numbers."""
    result = add(a, b)
    click.echo(f"Result: {result}")


@cli.command()
@click.argument("a", type=float)
@click.argument("b", type=float)
def subtract_cmd(a: float, b: float) -> None:
    """Subtract two numbers."""
    result = subtract(a, b)
    click.echo(f"Result: {result}")


@cli.command()
@click.argument("a", type=float)
@click.argument("b", type=float)
def multiply_cmd(a: float, b: float) -> None:
    """Multiply two numbers."""
    result = multiply(a, b)
    click.echo(f"Result: {result}")


@cli.command()
@click.argument("a", type=float)
@click.argument("b", type=float)
def divide_cmd(a: float, b: float) -> None:
    """Divide two numbers."""
    try:
        result = divide(a, b)
        click.echo(f"Result: {result}")
    except ValueError as e:
        raise ClickException(str(e)) from None  # This will print the error message and exit with status code 1


if __name__ == "__main__":
    cli()

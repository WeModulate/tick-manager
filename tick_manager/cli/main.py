import click
from click import ClickException

from tick_manager.operations.core import add, divide, multiply, subtract


@click.group()
def cli() -> None:
    """
    Tick Manager CLI group.

    This is the main entry point for the Tick Manager CLI.
    """
    pass


@cli.command()
def greet() -> None:
    """
    Greet the user.

    This command prints a greeting message to the user.
    """
    click.echo("Hello, Tick Manager!")


@cli.command()
@click.argument("a", type=float)
@click.argument("b", type=float)
def add_cmd(a: float, b: float) -> None:
    """
    Add two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    This command adds two numbers and prints the result.
    """
    result = add(a, b)
    click.echo(f"Result: {result}")


@cli.command()
@click.argument("a", type=float)
@click.argument("b", type=float)
def subtract_cmd(a: float, b: float) -> None:
    """
    Subtract two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    This command subtracts the second number from the first and prints the result.
    """
    result = subtract(a, b)
    click.echo(f"Result: {result}")


@cli.command()
@click.argument("a", type=float)
@click.argument("b", type=float)
def multiply_cmd(a: float, b: float) -> None:
    """
    Multiply two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    This command multiplies two numbers and prints the result.
    """
    result = multiply(a, b)
    click.echo(f"Result: {result}")


@cli.command()
@click.argument("a", type=float)
@click.argument("b", type=float)
def divide_cmd(a: float, b: float) -> None:
    """
    Divide two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    This command divides the first number by the second and prints the result.

    Raises:
        ClickException: If division by zero occurs.
    """
    try:
        result = divide(a, b)
        click.echo(f"Result: {result}")
    except ValueError as e:
        raise ClickException(str(e)) from None  # This will print the error message and exit with status code 1


if __name__ == "__main__":
    cli()

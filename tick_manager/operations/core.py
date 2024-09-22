from .exceptions import DivisionByZeroError


def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Subtract two numbers."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


def divide(a: float, b: float) -> float:
    """Divide two numbers, raising an error if division by zero."""
    if b == 0:
        raise DivisionByZeroError()
    return a / b

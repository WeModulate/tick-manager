class DivisionByZeroError(ValueError):
    def __init__(self) -> None:
        super().__init__("division by zero")

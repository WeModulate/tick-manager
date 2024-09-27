class DivisionByZeroError(ValueError):
    """
    Custom exception for division by zero errors.

    This exception is raised when an attempt is made to divide by zero.
    """

    def __init__(self) -> None:
        """
        Initialize the DivisionByZeroError with a default error message.
        """
        super().__init__("division by zero")

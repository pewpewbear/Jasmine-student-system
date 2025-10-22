"""
I/O utilities for safe input handling and consistent output formatting
"""


def safe_input(prompt: str) -> str:
    """Get input from user with error handling"""
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        return ""


def print_error(message: str) -> None:
    """Print error message with consistent formatting"""
    print(f"Error: {message}")


def print_success(message: str) -> None:
    """Print success message with consistent formatting"""
    print(message)


def print_info(message: str) -> None:
    """Print informational message"""
    print(message)

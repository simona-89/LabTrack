import os
from typing import Dict, List
from colorama import Fore, Style, init


init(autoreset=True)


def print_green(text: str) -> None:
    """
    Apply green color on text use colorama.

    Args:
        text (str): Received text.
    """
    print(Fore.GREEN + text)


def print_red(text: str) -> None:
    """
    Apply red color on text use colorama.

    Args:
        text (str): Received text.
    """
    print(Fore.RED + text)


def print_categories(result: Dict[str, List[str]]) -> None:
    """
    Prints categories and corresponding files.

    Args:
        result (Dict[str, List[str]]): Key - category, value - list of files.
    """
    for category, files in result.items():
        # Only print the category if it has file
        if files:
            if category == "Message":
                print_red(f"{", ".join(files)}")
            else:
                if category == "Valid PDFs":
                    print_green(f"{category}:")
                else:
                    print_red(f"{category}:")
                for file in files:
                    if category == "Valid PDFs":
                        print_green(f" - {file}")
                    else:
                        print_red(f" - {file}")


def print_valid_path(is_valid: bool, message: str) -> None:
    """
    Prints message in green if path valid, otherwise - in red.

    Args:
        is_valid (bool): True if the path is valid, False otherwise.
        message (str): The message to be printed.
    """
    if is_valid:
        print_green(message)
    else:
        print_red(message)


def in_bold(text: str) -> str:
    """
    Returns given text in bold use colorama.

    Args:
        text (str): The text to be bolded.

    Returns:
        str: The bolded text.
    """
    return f"{Style.BRIGHT}{text}{Style.RESET_ALL}"


def clear_screen() -> None:
    """
    Clears the temrinal.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

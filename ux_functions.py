import os
from colorama import Fore, Style, init

init(autoreset=True)


def print_green(text):
    print(Fore.GREEN + text)


def print_red(text):
    print(Fore.RED + text)


def print_categories(result):
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


def print_valid_path(is_valid, message):
    if is_valid:
        print_green(message)
    else:
        print_red(message)


def in_bold(text):
    return f"{Style.BRIGHT}{text}{Style.RESET_ALL}"


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

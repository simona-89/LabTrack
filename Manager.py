import os
from PyPDF2 import PdfReader
from colorama import Fore, Style, init


init(autoreset=True)


class FileManager:

    @staticmethod
    def is_valid_path(path):
        is_valid = os.path.isdir(path)
        if is_valid:
            message = (f"\nFolder is found:\n{path}\n")
        else:
            message = (f"\nFolder is not found:\n{path}\n"
                       "Check and try again.")
        UXManager.print_valid_path(is_valid, message)
        # return is_valid
        return is_valid, path if is_valid else None

    @staticmethod
    def is_valid_pdf(path):
        result = {"Valid": [],
                  "Invalid": []}

        for filename in os.listdir(path):
            if filename.endswith(".pdf"):
                try:
                    with open(os.path.join(path, filename), "rb") as file:
                        pdf = PdfReader(file)
                        info = pdf.metadata
                        if info.title == "E. sveikatos portalas":
                            result["Valid"].append(filename)
                        else:
                            result["Invalid"].append(filename)
                except Exception:
                    result["Invalid"].append(filename)
        if not any(result.values()):
            result["Message"] = ["Couldn\'t find any PDF file inside."]
        elif not result["Valid"]:
            result["Message"] = ["\nProvided PDFs don\'t meet requirements.\n"
                                 "Pls check README file. "
                                 "Otherwise, try again."]

        UXManager.print_categories(result)
        return result


class UXManager:
    @staticmethod
    def print_green(text):
        print(Fore.GREEN + text)

    @staticmethod
    def print_red(text):
        print(Fore.RED + text)

    @staticmethod
    def print_categories(result):
        for category, files in result.items():
            if files:  # Only print the category if it has file
                if category == "Message":
                    UXManager.print_red(f'{", ".join(files)}')
                else:
                    if category == "Valid":
                        UXManager.print_green(f'{category}:')
                    else:
                        UXManager.print_red(f'{category}:')
                    for file in files:
                        if category == "Valid":
                            UXManager.print_green(f' - {file}')
                        else:
                            UXManager.print_red(f' - {file}')

    @staticmethod
    def print_valid_path(is_valid, message):
        if is_valid:
            UXManager.print_green(message)
        else:
            UXManager.print_red(message)

    @staticmethod
    def in_bold(text):
        return f"{Style.BRIGHT}{text}{Style.RESET_ALL}"

    @staticmethod
    def clear_cli():
        os.system('cls' if os.name == 'nt' else 'clear')

from FileManager import FileManager
from ux_functions import clear_screen, in_bold
from file_manager import is_valid_path_pdf, create_database, track_details
from helper_functions import welcome_message, menu, quit_program
from export_functions import export_to_csv


def main():
    myfilemanager = FileManager()
    clear_screen()
    welcome_message()

    while True:
        menu()
        try:
            user_say = input(in_bold("Type selection here: "))
            while user_say not in ["1", "2", "3", "4"]:
                user_say = input(in_bold(
                    "Invalid choice.\n"
                    "Type selection between 1 and 4: "))
        except (EOFError, KeyboardInterrupt):
            quit_program()
        if user_say == "1":
            is_valid_path_pdf(myfilemanager)
        elif user_say == "2":
            if myfilemanager.is_valid_path():
                create_database(myfilemanager.filepath)
                track_details()
            else:
                input("\nPls fix, before continue...")
                clear_screen()
                continue
        elif user_say == "3":
            if myfilemanager.is_valid_path():
                export_to_csv(myfilemanager.filepath)
            else:
                input("\nPls fix, before continue...")
                clear_screen()
                continue
        elif user_say == "4":
            quit_program()


if __name__ == "__main__":
    main()

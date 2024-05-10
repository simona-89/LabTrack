import sys
from ux_functions import in_bold, clear_screen


def welcome_message():
    print(in_bold("Welcome to LabTrack"))
    print("Your personal assistant to track your blood test results.\n")


def menu():
    print(in_bold("LabTrack is here to help you:"))

    menu_options = {
        "1": "Upload your lab. test files",
        "2": "Track specific details",
        "3": "Export & Save CSV",
        "4": "Exit"
    }

    for key, value in menu_options.items():
        print(f"{in_bold('[' + key + ']')} {value}")


def quit_program():
    clear_screen()
    sys.exit(in_bold("\nThank you for using LabTrack!\n"))

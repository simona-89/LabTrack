import json
import re
import os

from datetime import datetime
from typing import Dict, Optional, Union
import FileManager
from helper_functions import quit_program
from pdfminer.high_level import extract_text
from ux_functions import clear_screen, in_bold


def is_valid_path_pdf(myfilemanager: FileManager) -> None:
    """
    Validates the path and checks if PDF files are and are valid.\n
    Prints messages following results from validation,
    calling methods of the class is_valid_path, is_valid_pdf.\n
    Handle user input while asking for navigation.

    Args:
        myfilemanager (FileManager): An instance of the class to take care of validation.
    Raises:
        EOFError: If caused by user input, terminates without a notice.
        KeyboardInterrupt: If caused by user input, terminates without a notice.
    """
    while True:
        clear_screen()
        print(in_bold("[ Upload your lab. test files ]\n"))

        try:
            myfilemanager.filepath = input("Enter path: ")
            valid_path = myfilemanager.is_valid_path()

            if valid_path:
                # Check if there is any PDF inside
                valid_pdf = myfilemanager.is_valid_pdf()
                # Read PDF metadata, create dict of valid & invalid PDFs
                if valid_pdf:
                    print(
                     f"Result after uploading files: {myfilemanager.filepath}")
                    return

            # Ask for next step and handle user's input
            print("\n")
            print(in_bold("[1]"), "Enter path again")
            print(in_bold("[2]"), "Go back")

            user_say = input(in_bold("Type selection here: "))

            while user_say not in ["1", "2"]:
                user_say = input(in_bold(
                    "Invalid choice.\n"
                    "Type selection between 1 and 2: "))

            if user_say == "1":
                continue

            clear_screen()
            return

        except (EOFError, KeyboardInterrupt):
            quit_program()


def create_database(pdf_dir: str) -> None:
    """
    Creates database in JSON file from the PDFs.\n
    Extracted text from PDFs has to have "E. sveikatos portalas" to call extract_data.\n
    Extracted data is formatted following extract_data and saved into "database.json".

    Args:
        pdf_dir (str): Dir to collect PDFs from.
    """
    print("... Please wait details are beeing extracted now...")

    data_from_pdf = {}
    raw_data = {}

    # Loops over each file in the directory
    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            # Reads the text from the PDF
            text = extract_text(os.path.join(pdf_dir, filename))
            raw_data[filename] = text
            if "E. sveikatos portalas" in text:
                # Extracts the specific details, following created patterns
                details = extract_data(text)
                data_from_pdf[filename] = details
            else:
                data_from_pdf[filename] = None
    with open("database.json", "w") as file:
        json.dump(data_from_pdf, file, indent=4)
    # For debugging, creating patterns while extracting all text
    # with open('rawData.json', 'w') as file:
    #     json.dump(raw_data, file, indent=4)


def extract_data(text: str)-> Dict[str, Union[str, Dict[str, Optional[str]]]]:
    """
    Extracts specific details from the given text,
    following specific structure.\n
    If value is not found, leaves by default None.

    Args:
        text (str): Extracted text passed to other functions, which apply regex.

    Returns:
        Dict[str, Union[str, Dict[str, Optional[str]]]]: The extracted data.
    """

    # Initialize the dictionary with all keys and None values
    extracted_data = {
        "Report date & time": None,
        "Hemoglobin": {
            "result": None,
            "levels from lab.": None,
            "analysed on": None
        },
        "Ferritin": {
            "result": None,
            "levels from lab.": None,
            "analysed on": None
        }
    }

    # Extract the report date & time
    extracted_data["Report date & time"] = extract_report_date_time(text)

    # Extract the hemoglobin data
    extracted_data["Hemoglobin"] = extract_hemoglobin_data(text)

    # Extract the ferritin data
    extracted_data["Ferritin"] = extract_ferritin_data(text)

    return extracted_data


def extract_report_date_time(text):
    pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2})"
    match = re.search(pattern, text)
    return match.group() if match else None


def extract_hemoglobin_data(text):
    hemoglobin_data = {"result": None, "levels from lab.": None, "analysed on": None}

    # Extract the hemoglobin result
    pattern_result = r"(HGB|HB)[\s\S]*?(\d+)"
    match_result = re.search(pattern_result, text)
    if match_result:
        hemoglobin_data["result"] = float(match_result.group(2))

        # Extract the levels
        pattern_levels = r"(\d+[\.\d{0,2}]*)\s*(?:-|–|iki)\s*(\d+[\.\d{0,2}]*)"
        match_levels = re.search(pattern_levels, text[match_result.end():])
        if match_levels:
            min_value = float(match_levels.group(1))
            max_value = float(match_levels.group(2))
            hemoglobin_data["levels from lab."] = f"{min_value} - {max_value}"

        # Extract the date
        pattern_date = r"(\d{4}[-.]\d{2}[-.]\d{2})"
        match_date = re.findall(pattern_date, text[:match_result.start()])
        if match_date:
            hemoglobin_data["analysed on"] = match_date[-1]

    return hemoglobin_data


def extract_ferritin_data(text):
    ferritin_data = {"result": None, "levels from lab.": None, "analysed on": None}

    pattern_result = r"Feritino koncentracijos nustatymas[,\n\s\d\.:]*?(\d+\.?\d?),?\s*(ng/ml|mkg/L)"
    match_result = re.search(pattern_result, text)
    if match_result:
        ferritin_data["result"] = float(match_result.group(1))

        # Extract the levels
        pattern_levels = r"[(\[]\s*(\d+[\.\d{0,2}]*)\s*(?:-|–|iki)\s*(\d+[\.\d{0,2}]*)\s*(?=[)\]])"
        match_levels = re.search(pattern_levels, text[match_result.end():])
        if match_levels:
            min_value = float(match_levels.group(1))
            max_value = float(match_levels.group(2))
            ferritin_data["levels from lab."] = f"{min_value} - {max_value}"

        # Extract the date
        pattern_date = r"(\d{4}[-.]\d{2}[-.]\d{2})"
        match_date_after = re.search(pattern_date, text[match_result.end():])
        if match_date_after:
            ferritin_data["analysed on"] = match_date_after.group(1)
        else:
            match_date_before = re.findall(pattern_date, text[:match_result.start()])
            if match_date_before:
                ferritin_data["analysed on"] = match_date_before[-1]

    return ferritin_data


def choose_parameter():
    parameter = {
        "1": "Hemoglobin",
        "2": "Ferritin",
        "3": "Back",
    }

    for key, value in parameter.items():
        print(f"{in_bold('[' + key + ']')} {value}")


def track_details():
    while True:
        clear_screen()
        print(in_bold("[ Track specific details ]\n"))
        print("Parameters were extracted from PDF.")
        print(in_bold("You can check results by selecting parameter:\n"))
        choose_parameter()
        try:
            user_say = input(in_bold("Type selection here: "))
            while user_say not in ["1", "2", "3"]:
                user_say = input(in_bold(
                    "Invalid choice.\n"
                    "Type selection between 1 and 3: "))
        except (EOFError, KeyboardInterrupt):
            quit_program()

        if user_say == "1":
            selected = "Hemoglobin"
            sorted_details(selected)
        elif user_say == "2":
            selected = "Ferritin"
            sorted_details(selected)
        elif user_say == "3":
            clear_screen()
            break


def sorted_details(parameter):
    with open("database.json", "r") as file:
        data = json.load(file)

    reports = []

    for filename, details in data.items():
        if details is not None and parameter in details and details[parameter]["result"] is not None:
            # Convert the report date to a datetime object for sorting
            report_date = datetime.strptime(details["Report date & time"], "%Y-%m-%d %H:%M")
            report = {k: (v if v is not None else 'N/A') for k, v in details[parameter].items()}
            reports.append((report_date, filename, report))

    # Sort the reports by date
    reports.sort()

    # Format how to print on CLI sorted details in the report
    while True:
        try:
            clear_screen()
            print(in_bold(f"Here are your {parameter} details:"))
            print("Details sorted in ascending order by Report issued on date.\n")
            print(in_bold("{:<30} {:<15} {:<10} {:<20} {:<10}".format("Report", "Issued on", "Result", "Lab. limits", "Analysed on")))
            print("-"*90)

            for report_date, filename, report_data in reports:
                print("{:<30} {:<15} {:<10} {:<20} {:<10}".format(
                        filename,
                        report_date.strftime("%Y-%m-%d"),
                        report_data["result"],
                        report_data["levels from lab."],
                        report_data["analysed on"]
                    ))

            print("\n" + in_bold("[1]"), "Go back")
            user_say = input(in_bold("Type selection here: "))

            while user_say != "1":
                user_say = input(in_bold(
                    "Invalid choice.\n"
                    "Type 1: "))

            if user_say == "1":
                clear_screen()
                return
        except (EOFError, KeyboardInterrupt):
            quit_program()


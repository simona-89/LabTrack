import json
import os
import re
from datetime import datetime
from typing import Dict, Optional, Union

from pdfminer.high_level import extract_text

import FileManager
from helper_functions import quit_program
from ux_functions import clear_screen, in_bold


def is_valid_path_pdf(myfilemanager: FileManager) -> None:
    """
    Validates the path and checks if PDF files are and are valid.\n
    Prints messages following results from validation,
    calling methods of the class is_valid_path, is_valid_pdf.\n
    Handle user input while asking for navigation.

    Args:
        myfilemanager (FileManager): Instance of class, take care of path validation.
    Raises:
        EOFError: When caused by user, terminates without a notice.
        KeyboardInterrupt: When caused by user, terminates without a notice.
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
    Creates database in JSON file using data inside PDFs, from validated path.\n
    Extracted text from PDFs has to have "E. sveikatos portalas" to call extract_data.\n
    Extracted data is formatted following extract_data and saved into "database.json".

    Args:
        pdf_dir (str): Dir to collect PDFs from.
    """
    print("... Please wait details are beeing extracted now...")

    # Initialize dict to hold extracted details from PDF and all text as raw_data
    data_from_pdf = {}
    raw_data = {}

    # Loops over each file in the directory
    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            # Extracts text from PDF (by file in valid path)
            text = extract_text(os.path.join(pdf_dir, filename))
            raw_data[filename] = text
            if "E. sveikatos portalas" in text:
                # Store details after regex was applied on strings of text
                details = extract_data(text)
                data_from_pdf[filename] = details
            else:
                data_from_pdf[filename] = None
    with open("database.json", "w") as file:
        json.dump(data_from_pdf, file, indent=4)
    # For debugging, creating patterns while extracting all text
    with open('rawData.json', 'w') as file:
        json.dump(raw_data, file, indent=4)


def extract_data(text: str) -> Dict[str, Union[str, Dict[str, Optional[str]]]]:
    """
    Extracts specific details from the given text,
    following specific structure.\n
    If value is not found, leaves by default None.

    Args:
        text (str): Extracted text passed to other f-tion where regex is used.

    Returns:
        Dict[str, Union[str, Dict[str, Optional[str]]]]: The extracted data.
    """

    # Initialize the dictionary with all keys and by default values as None
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


def extract_report_date_time(text: str) -> Optional[str]:
    """
    Extracts date and time of the report from the given text using regex.\n
    In case value not found use None by default.

    Args:
        text (str): The text to extract data from.

    Returns:
        str or None: Date & time if found, else None.
    """
    pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2})"
    match = re.search(pattern, text)
    return match.group() if match else None


def extract_hemoglobin_data(text: str) -> Dict[str, Optional[Union[float, str]]]:
    """
    Extracts hemoglobin data from the given text using regex.\n
    First search for parameter and it's result.\n
    Then search for min-max levels.\n
    Then find all dates before and use last one as value\n
    In case value not found use None by default.

    Args:
        text (str): The text to extract data from.

    Returns:
        Dict[str, Optional[Union[float, str]]]: The result to return or None.
    """
    hemoglobin_data = {"result": None,
                       "levels from lab.": None,
                       "analysed on": None}

    # Extract the hemoglobin result
    pattern_result = r"(HGB|HB)[\s\S]*?(\d+)"
    # First find if parameter is in the text
    match_result = re.search(pattern_result, text)
    # Get the float result, it's the number after
    if match_result:
        hemoglobin_data["result"] = float(match_result.group(2))

        # Then, search and extract the levels
        pattern_levels = r"(\d+[\.\d{0,2}]*)\s*(?:-|–|iki)\s*(\d+[\.\d{0,2}]*)"
        match_levels = re.search(pattern_levels, text[match_result.end():])
        # Get the float results for min and max values
        if match_levels:
            min_value = float(match_levels.group(1))
            max_value = float(match_levels.group(2))
            hemoglobin_data["levels from lab."] = f"{min_value} - {max_value}"

        # Then, find the date when lab. test was done
        pattern_date = r"(\d{4}[-.]\d{2}[-.]\d{2})"
        match_date = re.findall(pattern_date, text[:match_result.start()])
        if match_date:
            hemoglobin_data["analysed on"] = match_date[-1]

    return hemoglobin_data


def extract_ferritin_data(text: str) -> Dict[str, Optional[str]]:
    """
    Extracts ferritin data from the given text using regex.\n
    First search for parameter and it's result.\n
    Then search for min-max levels.\n
    Then search for 1st date after result,
    otherwise find all dates before and use last one as value\n
    In case value not found use None by default.

    Args:
        text (str): The text to extract data from.

    Returns:
        Dict[str, Optional[str]]: The result to return or None.
    """
    ferritin_data = {"result": None,
                     "levels from lab.": None,
                     "analysed on": None}
    # Extract the ferritin result
    pattern_result = r"Feritino koncentracijos nustatymas[,\n\s\d\.:]*?(\d+\.?\d?),?\s*(ng/ml|mkg/L)"
    # First find if parameter is in the text
    match_result = re.search(pattern_result, text)
    # Get the float result, it's the number after
    if match_result:
        ferritin_data["result"] = float(match_result.group(1))

        # Then, search and extract the levels
        pattern_levels = r"[(\[]\s*(\d+[\.\d{0,2}]*)\s*(?:-|–|iki)\s*(\d+[\.\d{0,2}]*)\s*(?=[)\]])"
        match_levels = re.search(pattern_levels, text[match_result.end():])
        # Get the float results for min and max values
        if match_levels:
            min_value = float(match_levels.group(1))
            max_value = float(match_levels.group(2))
            ferritin_data["levels from lab."] = f"{min_value} - {max_value}"

        # Then, find the date when lab. test was done
        pattern_date = r"(\d{4}[-.]\d{2}[-.]\d{2})"
        #  First check if date is after result
        match_date_after = re.search(pattern_date, text[match_result.end():])
        if match_date_after:
            ferritin_data["analysed on"] = match_date_after.group(1)
        else:
            # Otherwise check for all dates before result
            match_date_before = re.findall(pattern_date, text[:match_result.start()])
            # Take the last date found
            if match_date_before:
                ferritin_data["analysed on"] = match_date_before[-1]

    return ferritin_data


def choose_parameter() -> None:
    """
    Prints options inside one of sub-menu.
    """
    parameter = {
        "1": "Hemoglobin",
        "2": "Ferritin",
        "3": "Back",
    }

    for key, value in parameter.items():
        print(f"{in_bold('[' + key + ']')} {value}")


def track_details() -> None:
    """
    Tracks the details of a specific parameter chosen by the user.\n
    Pass selected parameter to f-tion sorted_details, for printing all details.

    Raises:
        EOFError: When caused by user, terminates without a notice.
        KeyboardInterrupt: When caused by user, terminates without a notice.
    """
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


def sorted_details(parameter: str) -> None:
    """
    Sorts and display details of specific parameter from a JSON file.\n
    Use .sort() for sorting data by report date, then parameter.\n
    Display results in formatted table using .format().

    Args:
        parameter (str): Selected parameter.
     Raises:
        EOFError: When caused by user, terminates without a notice.
        KeyboardInterrupt: When caused by user, terminates without a notice.
    """
    with open("database.json", "r") as file:
        data = json.load(file)

    reports = []

    # Iterrate over each item, assign k as filename, v - value
    for filename, details in data.items():
        # Check for parameter and it's result to be not None
        if details is not None and parameter in details and details[parameter]["result"] is not None:
            # Convert the report date to a datetime object for sorting
            report_date = datetime.strptime(details["Report date & time"], "%Y-%m-%d %H:%M")
            # Create new dict using details[parameter], only replace None to N/A
            report = {k: (v if v is not None else 'N/A') for k, v in details[parameter].items()}
            # Return result to reports as tuple
            reports.append((report_date, filename, report))

    # Sort in ascending order first by report_date, second - filename, third - report
    reports.sort()

    # Format how to print on CLI sorted details in the report
    while True:
        try:
            clear_screen()
            print(in_bold(f"Here are your {parameter} details:"))
            print("Details sorted in ascending order by Report issued on date.\n")
            print(in_bold("{:<30} {:<15} {:<10} {:<20} {:<10}".format("Report", "Issued on", "Result", "Lab. limits", "Analysed on")))
            print("-"*90)

            # Print details of each report
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


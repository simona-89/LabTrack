import csv
import json
import os
from datetime import datetime
from helper_functions import quit_program
from ux_functions import clear_screen, in_bold


def export_to_csv(pdf_dir: str) -> None:
    """
    F-tion to print selections and allow export data to a CSV.\n
    Handle selections while asking for user input.\n
    Related to create_csv() f-tion which takes care of creation of CSV.

    Args:
        pdf_dir (str): Dir where CSV file be saved.
    Raises:
        EOFError: when caused by user, terminates without a notice.
        KeyboardInterrupt: When caused by user, terminates without a notice.
    """
    save_csv_in_dir = pdf_dir
    while True:
        clear_screen()
        print(in_bold("[ Export & Save CSV ]\n"))
        print("Here extracted details could be saved as 'results.csv'.\n")
        print(in_bold("[1]"), "Export & Save")
        print(in_bold("[2]"), "Go back")
        try:
            user_say = input(in_bold("Type selection here: "))
            while user_say not in ["1", "2"]:
                user_say = input(in_bold(
                    "Invalid choice.\n"
                    "Type selection between 1 and 2: "))
        except (EOFError, KeyboardInterrupt):
            quit_program()

        if user_say == "1":
            create_csv(save_csv_in_dir)
            break
        else:
            clear_screen()
            break


def create_csv(csv_dir: str) -> None:
    """
    F-tion to create a CSV file from the data in a JSON file.\n
    To read data in JSON and formats it into rows\n
    To sort by parameter and after report date & time.\n
    To check if CSV file created successfully in the path.\n
    Related to export_to_csv, as get the path details to create CSV inside.

    Args:
        csv_dir (str): Dir where CSV file be saved.
    """
    while True:
        clear_screen()
        print(in_bold("[ Export & Save ]\n"))

        with open("database.json", "r") as file:
            data = json.load(file)

        # Store data to write into CSV
        rows = []

        for filename, details in data.items():
            if details is not None:
                report_date = datetime.strptime(details["Report date & time"], "%Y-%m-%d %H:%M")
                # Iterrate over details dict
                for parameter, report in details.items():
                    if parameter != "Report date & time" and report["result"] is not None:
                        rows.append({
                            "filename": filename,
                            "report_date": report_date,
                            "parameter": parameter,
                            "result": report["result"],
                            "levels from lab.": report["levels from lab."],
                            "analysed on": report["analysed on"]
                        })

        # Sort the rows by parameter and then by date
        rows.sort(key=lambda row: (row["parameter"], row["report_date"]))

        # Set the path and file name
        csv_save_as = f"{csv_dir}/results.csv"

        with open(csv_save_as, "w", newline="") as file:
            writer = csv.writer(file)
            # Create header row
            writer.writerow(["Report", "Issued on", "Parameter",
                             "Result", "Lab. limits", "Analysed on"])
            for row in rows:
                writer.writerow([
                    row["filename"],
                    row["report_date"].strftime('%Y-%m-%d'),
                    row["parameter"],
                    row["result"],
                    row["levels from lab."],
                    row["analysed on"]
                ])

        # Check if the file was created successfully and print message to user
        if os.path.exists(csv_save_as):
            input(f"File 'results.csv' was created successfully at {csv_save_as}")
            clear_screen()
            return
        else:
            input("Failed to create 'results.csv'")
            clear_screen()
            return


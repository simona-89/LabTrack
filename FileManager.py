import os
from PyPDF2 import PdfReader
from ux_functions import print_categories, print_valid_path


class FileManager:
    def __init__(self):
        self.filepath = ''

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, filepathname):
        self._filepath = filepathname

    def is_valid_path(self):
        is_valid = os.path.isdir(self.filepath)
        if is_valid:
            message = (f"\nFolder is found:\n{self.filepath}\n")
        else:
            message = (f"\nFolder is not found:\n{self.filepath}\n"
                       "Check and try again.")
        print_valid_path(is_valid, message)
        return is_valid

    def is_valid_pdf(self):
        result = {"Valid PDFs": [],
                  "Invalid PDFs": []}

        for filename in os.listdir(self.filepath):
            if filename.endswith(".pdf"):
                try:
                    with open(os.path.join(self.filepath, filename), "rb") as file:
                        pdf = PdfReader(file)
                        info = pdf.metadata
                        if info.title == "E. sveikatos portalas":
                            result["Valid PDFs"].append(filename)
                        else:
                            result["Invalid PDFs"].append(filename)
                except Exception:
                    result["Invalid PDFs"].append(filename)
        if not any(result.values()):
            result["Message"] = ["Couldn\'t find any PDF file inside."]
        elif not result["Valid PDFs"]:
            result["Message"] = ["\nProvided PDFs don\'t meet requirements.\n"
                                 "Pls check README file. "
                                 "Otherwise, try again."]

        print_categories(result)

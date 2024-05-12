import os
from typing import Dict, List, Union
from PyPDF2 import PdfReader
from ux_functions import print_categories, print_valid_path


class FileManager:
    """
    Manages files in the directory.\n
    Checks if dir path is valid.\n
    Then checks if PDF inside is valid, reads metadata using PyPDF2.\n
    Property filepath get and set dir path that FileManager instance
    is working with.\n

    Attr:
        filepath (str): Dir path FileManager instance is working with.
    Methohds:
        is_valid_path(): Performs validity check on directory.
        is_valid_pdf(): Performs validity check on PDF.
    """
    def __init__(self):
        self.filepath = ''

    @property
    def filepath(self) -> str:
        """
        Gets the value of the _filepath attribute.

        Returns:
            str: Dir path that FileManager instance working with.
        """
        return self._filepath

    @filepath.setter
    def filepath(self, filepathname: str) -> None:
        """
        Sets the value of the _filepath attribute.

        Args:
            filepathname (str): Dir path the FileManager instance working with.
        """
        self._filepath = filepathname

    def is_valid_path(self) -> bool:
        """
        Checks if the filepath is a valid directory and prints a message based 
        on the result.

        Returns:
            bool: True if path is valid, False otherwise.
        """
        is_valid = os.path.isdir(self.filepath)
        if is_valid:
            message = (f"\nFolder is found:\n{self.filepath}\n")
        else:
            message = (f"\nFolder is not found:\n{self.filepath}\n"
                       "Check and try again.")
        print_valid_path(is_valid, message)
        return is_valid

    def is_valid_pdf(self) -> Dict[str, Union[List[str], str]]:
        """
        Checks if PDF in the path dir is valid and
        prints a categorized list of the PDFs.

        Returns:
            Dict[str, Union[List[str], str]]: The collected data.
        """
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


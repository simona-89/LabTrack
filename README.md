# LabTrack

https://github.com/simona-89/LabTrack.git

LabTrack is a basic tool which allow you to track Hemoglobin and Ferritin levels from your blood tests which are accessible from your personal account from e-sveikata.
User should have folder with PDF files created and downloaded from personal account https://www.esveikata.lt/.


## Features

**Upload your lab. test files**: Thos feature allows you upload pdf files from your PC.

**Track specific details**: This feature allows you to track 'Hemoglobin' or 'Ferritin' levels.

**Export & Save CSV**: This feature allows you to save extracted details in CSV file.


## How to Run

To run the LabTrack application, navigate to the directory containing the `main.py` file in your terminal and run the following command:

```bash
python main.py

```
This will start the application and display the menu.

## How to Use

### Preparation

Before starting the application, you need to do some preparation.

1. Sign to your https://www.esveikata.lt/
2. Find & select "Sveikatos duomenys" (on the top row of the page)
3. Find & select "Sveikatos Istrija" (selection from navbar "Sveikatos duomenys")
4. Find & select "Dokumentai" (navbar on the left top)
5. Find & select "Ambulatorinis apsilankymas"
6. Notice records uploaded from your visits at clinics & hospitals (on the right side on the page)
7. Each record has sections "Apsilankymo suvestinė" & "Dokumentai"
8. Select "Dokumentai" and look for uploaded forms as "E025 Ambulatorinio apsilankymo aprašymas"
9. Open forms "E025 Ambulatorinio apsilankymo aprašymas" and use mouse right-click to create PDF (print>save)

Please note that this version of LabTrack was desidned and tested mainly to read data from these forms and in case they are saved as PDF in this way.

### Running the LabTrack

If you are finished with preparation, you will see the menu with the following options:

LabTrack is here to help you:
[1] Upload your lab. test files
[2] Track specific details
[3] Export & Save CSV
[4] Exit
Type selection here: 

Enter the number of your choice to access the corresponding module or Exit. 
Please note that here and while choosing from other options, application will keep asking for valid option. In case of EOFError or KeyboardInterrupt application will terminate.

## Dependencies
LabTrack uses external libraries as below.

- pdfminer.high_level: This is a part of the pdfminer.six library, which is a Python package for extracting text, images, metadata, and more from PDF files. It can be installed with pip.
- PyPDF2: This is a Python library for reading and writing PDF files. It can be installed with pip.
- colorama: This is a Python library for producing colored terminal text and cursor positioning on multiple platforms. It can be installed with pip.

You can install the external libraries by running:

```bash
pip install pdfminer.six
pip install PyPDF2
pip install colorama
```

## Limitations and Future Improvements

LabTrack currently reads data from specific PDF files, also there is very high dependency on the patterns used to find and extract specific details, areas below could be improved:

1. **Flexibility**: Currently, the application supports only one type of documents, created in specific way as PDFs. In the next version, it could be made more flexible by having possibilities to read details from PDFs when data is in the tables or as graph bars. It might be worth thinking if there are files which allow to work with data easier than PDFs and could be generated from https://www.esveikata.lt/.

2. **Error Handling**: Not all errors are handled and could be improved:
- While working with .json and .csv files not currently handling the errors. 
- Pending problem not solved, as now program could run using valid path without valid pdf files as user could run options as [2] Track specific details, [3] Export & Save CSV, and do not get any results, this approach is not informative and sign of a bad desing. Planning to improve this.

3. **Features**: Currently, application allows to print only details in ascending order and this could be improved by adding more options how data could be presented. Extracted details, when printed on CLI does not support coloring of the results (to visually show if parameter is in acceptable levels or not) this could imporve UX. Also now the validated path in the begining is used as a path to save results.csv file, this could be improved by allowing uses to choose the path.

4. **Code Structure**: Current code could be imporved reducing code inside file_manager.py by separating functions and creating separate files for data extraction, meniu options, specific actions. Solutions to reuse code should be found, refactoring to use more OOP could be beneficial.

Please note that these improvements would require significant changes to the application's codebase and are intended for future versions of the application.

## Contact
For any issues or suggestions related to LabTrack, please contact the maintainers.

## Contributions
In case of the further ideas or willingnes to cooperate on this application, please contact the maintainers for more details.

# WLLR Rostering App

### Background

The WLLR is a steam railway in Wales (https://www.wllr.org.uk/). It is a charitable organisation run by (almost exclusively) volunteers, including the engine drivers and firemen.

In order to provide a fixed timetable with volunteer labour, volunteers provide their availability for driving and/or firing and this availability is matched to the requirements for the timetable. In the past this has been done manually; now it is done by this program.

### Using the program

The WLLR rostering app take inputs from .csv files or .xlsx files for:
1. the timetable by day, showing the 'colour' of the timetable for that day (see 'test/Test input data' => 'Timetable.xlsx')
2. the crew requirements for each 'colour' on the timetable (see 'test/Test input data' => 'Crew requirements.xlsx')
3. each individual's availability put into the relevant folders depending on their grade (see the folders '01 Driver availability', '02 Fireman availability' and '03 Trainee availability')

The app takes the user through a number of steps including:
1. Creating a blank availability form that can be sent to volunteers
2. Creating a blank roster based on the timetable and the crew requirements
3. Allocating volunteer availability to the roster based on the allocation algorithm
4. Creating individual rosters for each volunteer based on the finalised roster

The outputs are created as .xlsx files with the exception of the individual rosters for each volunteer, which are created as .pdf files.

The app can be run directly from the terminal or it can be packaged into a .exe and run independently (which is how it is currently being used by the roster clerk).

To run the app from the terminal, navigate to the directory you have saved the files and run: `python src/rostering_app.py`

To package the code into a .exe using pyinstaller (https://www.pyinstaller.org/) first run `pip install pyinstaller`, then run: `pyinstaller rostering_app.spec`.

NB: the code has only been used and tested on the Windows 10 operating system.

### Code used

This program is written in Python 3.8, with the user interface developed in tkinter.

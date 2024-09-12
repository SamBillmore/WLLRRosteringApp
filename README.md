# WLLR Rostering App

## Background

The WLLR is a steam railway in Wales (https://www.wllr.org.uk/). It is a charitable organisation run by (almost exclusively) volunteers, including the engine drivers and firemen.

In order to provide a fixed timetable with volunteer labour, volunteers provide their availability for driving and/or firing and this availability is matched to the requirements for the timetable. In the past this has been done manually; now it is done by this app.

## Using the app

The WLLR rostering app take inputs from .csv files or .xlsx files for:
1. the timetable by day, showing the 'colour' of the timetable for that day
2. the crew requirements for each 'colour' on the timetable
3. each individual's availability put into the relevant folders depending on their grade

Examples of each of these input files can be created by the app by the user.

The app takes the user through a number of steps including:
1. Creating a blank availability form that can be sent to volunteers
2. Creating a blank roster based on the timetable and the crew requirements
3. Allocating volunteer availability to the roster based on the allocation algorithm
4. Creating individual rosters for each volunteer based on the finalised roster

The outputs are created as .xlsx files with the exception of the individual rosters for each volunteer, which are created as .pdf files.

The app is intended to be packaged into a standalone .exe (which is how it is currently being used by the roster clerk).

## Development

### Code used

This program is written in Python 3.8, with the user interface developed in tkinter.

### Development environment

In your virtual environment, run `pip install -e ."[dev,test,build]"` to install the package in editable mode with all the dependencies that are required.

The app can be run directly from the terminal or it can be packaged into a .exe and run independently (which is how it is currently being used by the roster clerk).

To run the app from the terminal, navigate to the directory you have saved the files, ensure you have installed the package and the base dependencies, then run: `WLLRRosteringApp`.

To package the code into a .exe using pyinstaller (https://www.pyinstaller.org/) first ensure you have installed the build dependencies, then run: `pyinstaller rostering_app.spec`.

import pandas as pd

from import_export.import_export_classes import Data_Imports
from import_export.import_export_classes import Data_Exports


def create_blank_availability(timetable_path, save_location):
    timetable = Timetable()
    availability_form = Availability_Form()
    timetable.import_data(timetable_path)
    availability_form.get_timetable_dates(timetable)
    availability_form.create_availability_form(save_location)


class Timetable(Data_Imports):
    """Timetables as input by the user."""

    def __init__(self, timetable=None):
        """Initiates the class."""
        self.data_import = timetable
        self.expected_columns = {"Date": object, "Timetable": object}


class Availability_Form(Data_Exports):
    """Blank availability forms."""

    def __init__(self, dates=None):
        """Initiates the class."""
        self.dates = dates
        self.columns = ["Date", "Available"]
        self.entry_values = ["Y", "N"]
        self.data_export = None

    def get_timetable_dates(self, timetable):
        """Populates self.dates from the dates in a timetable."""
        self.dates = timetable.data_import["Date"]

    def create_availability_form(self, save_location):
        """Creates a .xlsx document with self.dates, self.columns and limits the entry
        values to self.entry_values."""
        sheet_name = "Availability"
        self.data_export = pd.DataFrame(self.dates, columns=self.columns)
        data_val_cells = ["B" + str(i + 2) for i in self.data_export.index]
        export_test = self.export_data(
            filepath=save_location, sheet_name=sheet_name, data_val_cells=data_val_cells
        )
        return export_test

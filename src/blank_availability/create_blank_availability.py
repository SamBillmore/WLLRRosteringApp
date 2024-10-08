import pandas as pd

from import_export.import_export_classes import DataImports
from import_export.import_export_classes import DataExports
from standard_labels.standard_labels import StandardLabels


def create_blank_availability(timetable_path, save_location, password=None):
    timetable = Timetable()
    availability_form = Availability_Form()
    timetable.import_data(file_path=timetable_path)
    availability_form.get_timetable_dates(timetable=timetable)
    availability_form.create_availability_form(
        save_location=save_location, password=password
    )


class Timetable(DataImports):
    """Timetables as input by the user."""

    def __init__(self, timetable=None):
        """Initiates the class."""
        self.data_import = timetable
        self.expected_columns = {
            StandardLabels.date: object,
            StandardLabels.timetable: object,
        }


class Availability_Form(DataExports):
    """Blank availability forms."""

    def __init__(self, dates=None):
        """Initiates the class."""
        self.dates = dates
        self.columns = [StandardLabels.date, StandardLabels.available]
        self.entry_values = [StandardLabels.y, StandardLabels.n]
        self.data_export = None

    def get_timetable_dates(self, timetable):
        """Populates self.dates from the dates in a timetable."""
        self.dates = timetable.data_import[StandardLabels.date]

    def create_availability_form(self, save_location, password=None):
        """Creates a .xlsx document with self.dates, self.columns and limits the entry
        values to self.entry_values."""
        sheet_name = "Availability"
        self.data_export = pd.DataFrame(self.dates, columns=self.columns)
        data_entry_cells = ["B" + str(i + 2) for i in self.data_export.index]
        self.export_data(
            filepath=save_location,
            sheet_name=sheet_name,
            data_val_cells=data_entry_cells,
            editable_cells=data_entry_cells,
            password=password,
        )

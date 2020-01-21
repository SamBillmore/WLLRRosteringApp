import pandas as pd

from import_export.import_export_classes import Data_Imports
from import_export.import_export_classes import Data_Exports

class Timetable(Data_Imports):
    """
    Timetables as input by the user
    """

    def __init__(self, timetable=None):
        """
        Initiates the class
        """
        self.data_import = timetable
        self.expected_columns = {'Date':object,'Timetable':object}

class Availability_Form(Data_Exports):
    """
    Blank availability forms
    """

    def __init__(self, dates=None):
        """
        Initiates the class
        """
        self.dates = dates
        self.columns = ['Date','Available']
        self.entry_values = ['Y','N']
        self.data_export = None

    def get_timetable_dates(self, timetable):
        """
        Populates self.dates from the dates in a timetable
        """
        self.dates = timetable.data_import['Date']

    def create_availability_form(self, save_location):
        """
        Creates a .xlsx document with self.dates, self.columns 
        and limits the entry values to self.entry_values
        """
        sheet_name='Availability'
        self.data_export = pd.DataFrame(self.dates, columns=self.columns)
        data_val_cells = ['B'+str(i+2) for i in self.data_export.index]
        self.export_data(filepath=save_location, sheet_name=sheet_name, data_val_cells=data_val_cells)
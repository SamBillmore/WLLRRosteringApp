import numpy as np
import pandas as pd

class Timetable():
    """
    Timetables as input by the user
    """

    def __init__(self, timetable=None):
        """
        Initiates the class
        """
        self.timetable = timetable
        self.expected_columns = ['Date','Timetable']

    def import_data(self, filepath):
        """
        Attempts to imports data from a csv as the timetable and
        checks whether columns are as expected
        Returns True if import completes and columns are correct
        Returns False otherwise
        """
        try:
            self.timetable = pd.read_csv(filepath)
            return np.array_equal(self.timetable.columns, self.expected_columns)
        except:
            return False
        
class Availability_Form():
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

    def get_timetable_dates(self, timetable):
        """
        Populates self.dates from the dates in a timetable
        """
        self.dates = timetable.timetable['Date']

    def create_availability_form(self, save_location):
        """
        Creates a .xlsx document with self.dates, self.columns 
        and limits the entry values to self.entry_values
        """
        writer = pd.ExcelWriter(save_location, engine='xlsxwriter')
        sheet_name = 'Availability'

        availability_form_df = pd.DataFrame(self.dates, columns=self.columns)
        availability_form_df.to_excel(writer, sheet_name=sheet_name,index=False)
        workbook  = writer.book
        worksheet = writer.sheets[sheet_name]
        workbook.add_format({'border':1})
        worksheet.set_column(0,0,11)
        data_val_cells = ['B'+str(i+2) for i,j in enumerate(availability_form_df['Available'])]
        for i in data_val_cells:
            worksheet.data_validation(i,{'validate':'list','source': self.entry_values})
        writer.save()








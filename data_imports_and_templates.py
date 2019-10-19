import numpy as np
import pandas as pd

class Data_Imports():
    """
    Parent Class for importing data
    """

    def __init__(self):
        """
        Initiates the class
        """
        self.data = None
        self.expected_columns = None

    def import_data(self, filepath):
        """
        Attempts to imports data from a csv as the timetable and
        checks whether columns are as expected
        Returns True if import completes and columns are correct
        Returns False otherwise
        """
        try:
            self.data = pd.read_csv(filepath)
            return np.array_equal(self.data.columns, self.expected_columns)
        except:
            return False

class Timetable(Data_Imports):
    """
    Timetables as input by the user
    """

    def __init__(self, timetable=None):
        """
        Initiates the class
        """
        self.data = timetable
        self.expected_columns = ['Date','Timetable']

class Crew_Requirements(Data_Imports):
    """
    Crew requirements as input by the user
    """

    def __init__(self, crew_reqs=None):
        """
        Initiates the class
        """
        self.crew_reqs = crew_reqs
        self.expected_columns = ['Timetable','Turn','Points']

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
        self.availability_form = None

    def get_timetable_dates(self, timetable):
        """
        Populates self.dates from the dates in a timetable
        """
        self.dates = timetable.data['Date']

    def create_availability_form(self, save_location):
        """
        Creates a .xlsx document with self.dates, self.columns 
        and limits the entry values to self.entry_values
        """
        writer = pd.ExcelWriter(save_location, engine='xlsxwriter')
        sheet_name = 'Availability'

        self.availability_form = pd.DataFrame(self.dates, columns=self.columns)
        self.availability_form.to_excel(writer, sheet_name=sheet_name,index=False)
        workbook  = writer.book
        worksheet = writer.sheets[sheet_name]
        workbook.add_format({'border':1})
        worksheet.set_column(0,0,11)
        data_val_cells = ['B'+str(i+2) for i,j in enumerate(self.availability_form['Available'])]
        for i in data_val_cells:
            worksheet.data_validation(i,{'validate':'list','source': self.entry_values})
        writer.save()

class Blank_Roster():
    """
    Blank roster
    """

    def __init__(self, timetable=None, crew_requirements=None):
        """
        Initiates the class
        """
        self.timetable = timetable
        self.crew_requirements = crew_requirements
        self.blank_roster = None
        self.blank_columns = ['Driver','Fireman','Trainee']

    def create_blank_roster(self, timetable, crew_requirements, save_location):
        """
        Creates the data for the blank roster
        """
        writer = pd.ExcelWriter(save_location, engine='xlsxwriter')
        sheet_name = 'Roster'
        
        self.timetable = timetable
        self.crew_requirements = crew_requirements
        self.blank_roster = self.timetable.merge(self.crew_requirements,how='left',on='Timetable')
        blank_roster_columns = self.blank_roster.columns.tolist() + self.blank_columns
        self.blank_roster = self.blank_roster.reindex(columns = blank_roster_columns)
        self.blank_roster.to_excel(writer, sheet_name=sheet_name,index=False)
        workbook  = writer.book
        worksheet = writer.sheets[sheet_name]
        workbook.add_format({'border':1})
        worksheet.set_column(0,0,11)
        writer.save()
        




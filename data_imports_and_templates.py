import numpy as np
import pandas as pd
import os

class Data_Imports():
    """
    Parent Class for importing data
    """

    def __init__(self):
        """
        Initiates the class
        """
        self.data_import = None
        self.expected_columns = None

    def import_data(self, file_path):
        """
        Attempts to imports data from a csv as the timetable and
        checks whether columns are as expected
        Returns True if import completes and columns are correct
        Returns False otherwise
        """
        try:
            self.data_import = pd.read_csv(file_path)
            return np.array_equal(self.data_import.columns, self.expected_columns)
        except:
            self.data_import = pd.read_excel(file_path)
            return np.array_equal(self.data_import.columns, self.expected_columns)

class Data_Exports():
    """
    Parent Class for exporting data
    """

    def __init__(self):
        """
        Initiates the class
        """
        self.data_export = None
        self.entry_values = ['Y','N']

    def export_data(self, filepath=None, sheet_name=None, data_val_cells=None):
        """
        Attempts to export data to a .xlsx
        Includes formatting of columns and header
        Adds data validation to cells specified in data_val_cells 
        """
        writer = pd.ExcelWriter(filepath, engine='xlsxwriter')
        self.data_export.to_excel(writer, sheet_name=sheet_name, index=False)
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]
        workbook.add_format({'border':1})
        worksheet.set_column(0,0,11)
        if data_val_cells:
            for i in data_val_cells:
                worksheet.data_validation(i, {'validate':'list', 'source':self.entry_values})
        writer.save()

class Timetable(Data_Imports):
    """
    Timetables as input by the user
    """

    def __init__(self, timetable=None):
        """
        Initiates the class
        """
        self.data_import = timetable
        self.expected_columns = ['Date','Timetable']

class Crew_Requirements(Data_Imports):
    """
    Crew requirements as input by the user
    """

    def __init__(self, crew_reqs=None):
        """
        Initiates the class
        """
        self.data_import = crew_reqs
        self.expected_columns = ['Timetable','Turn','Points']

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

class Blank_Roster(Data_Exports):
    """
    Blank roster
    """

    def __init__(self, timetable=None, crew_requirements=None):
        """
        Initiates the class
        """
        self.timetable = timetable
        self.crew_requirements = crew_requirements
        self.data_export = None
        self.blank_columns = ['Driver','Fireman','Trainee']

    def create_blank_roster(self, timetable, crew_requirements, save_location):
        """
        Creates the data for the blank roster
        """
        sheet_name = 'Roster'
        self.timetable = timetable
        self.crew_requirements = crew_requirements
        self.data_export = self.timetable.merge(self.crew_requirements, how='left', on='Timetable')
        blank_roster_columns = self.data_export.columns.tolist() + self.blank_columns
        self.data_export = self.data_export.reindex(columns = blank_roster_columns)
        self.export_data(filepath=save_location, sheet_name=sheet_name)
        
class Crew_Member(Data_Imports):
    """
    Availability as input by the user
    """

    def __init__(self, availability=None, name=None, grade=None):
        """
        Initiates the class
        """
        self.data_import = availability
        self.name = name
        self.grade = grade
        self.expected_columns = ['Date','Available']

class Crew_Members():
    """
    List of all crew members
    """

    def __init__(self):
        """
        Initiates the class
        """
        self.data = []

class Master_Availability(Data_Exports):
    """
    Master list of availability
    """

    def __init__(self, individual_availability=None):
        """
        Initiates the class
        """
        self.individual_availability = individual_availability
        self.data_export = pd.DataFrame()

    def create_master_availability(self, grade, availability_folder, crew_members):
        """
        Importing availability from completed availability forms
        Create master availability form
        Save to save location
        """
        for file_name in os.listdir(availability_folder):
            crew_member = Crew_Member()
            crew_member.name = file_name.split('.')[0]
            crew_member.grade = grade
            file_path = os.path.join(availability_folder + "/" + file_name)
            crew_member.import_data(file_path)
            self.append_availability(crew_member)
            crew_members.data.append(crew_member)

    def append_availability(self, crew_member):
        """
        Appends an individual's availability to the master list
        """
        availability = crew_member.data_import
        availability.insert(0,'Name',[crew_member.name for i in range(len(availability))])
        availability.insert(0,'Grade',[crew_member.grade for i in range(len(availability))])
        self.data_export = self.data_export.append(availability)
        self.data_export = self.data_export[self.data_export['Available'] == 'Y']
        
class Master_Roster(Data_Imports,Data_Exports):
    """
    Master roster
    """

    def __init__(self):
        """
        Initiates the class
        """
        self.data_import = None
        self.data_export = None

    
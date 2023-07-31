import numpy as np
import pandas as pd
import os
from win32com.client import Dispatch
import matplotlib.pyplot as plt

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
        Attempts to import data from a csv or xlsx and
        checks whether columns are as expected
        Returns True if import completes and column headers are correct
        Returns False otherwise
        """
        try:
            try:
                self.data_import = pd.read_csv(file_path,dtype=self.expected_columns)
            except:
                self.data_import = pd.read_excel(file_path,dtype=self.expected_columns)
            if 'Date' in self.data_import.columns:
                self.data_import['Date'] = pd.to_datetime(self.data_import['Date'],dayfirst=True,infer_datetime_format=True)
            return np.array_equal(self.data_import.columns, list(self.expected_columns.keys()))
        except:
            return False

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

    def export_data(self, filepath, sheet_name, data_val_cells=None):
        """
        Attempts to export data to a .xlsx
        Includes formatting of columns and header
        Adds data validation to cells specified in data_val_cells 
        """
        try:
            writer = pd.ExcelWriter(filepath, engine='xlsxwriter', date_format='ddd dd-mm-yyyy', datetime_format='ddd dd-mm-yyyy')
            self.data_export.to_excel(writer, sheet_name=sheet_name, index=False)
            workbook = writer.book
            worksheet = writer.sheets[sheet_name]
            workbook.add_format({'border':1})
            if data_val_cells:
                for i in data_val_cells:
                    worksheet.data_validation(i, {'validate':'list', 'source':self.entry_values})
            writer.close()
            self.autofit_columns(filepath,sheet_name)
            return True
        except:
            return False

    def autofit_columns(self,filepath,sheet_name):
        """
        Auto adjusts the width of columns in a specific worksheet of an Excel workbook
        """
        excel = Dispatch('Excel.Application')
        full_filepath = os.path.abspath(filepath)
        wb = excel.Workbooks.Open(full_filepath)
        excel.Worksheets(sheet_name).Activate()
        excel.ActiveSheet.Columns.AutoFit()
        wb.Save()
        wb.Close()

    def print_df_to_pdf(self,df,filepath):
        """
        Saves a pandas dataframe to a pdf using matplotlib
        """
        fig = plt.figure()
        ax=fig.add_subplot(111)
        cell_text = []
        for row in range(len(df)):
            cell_text.append(df.iloc[row])
        ax.table(cellText=cell_text, colLabels=df.columns, loc='center')
        ax.axis('off')
        try:
            fig.savefig(filepath)
            return True
        except:
            return False
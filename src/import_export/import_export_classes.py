import pandas as pd
import os
import platform
import xlwings as xw
import matplotlib.pyplot as plt
from copy import copy

from standard_labels.standard_labels import StandardLabels


class DataImports:
    """Parent Class for importing data."""

    extension_mapping = {
        ".csv": pd.read_csv,
        ".xls": pd.read_excel,
        ".xlsx": pd.read_excel,
        ".xlsm": pd.read_excel,
        ".xlsb": pd.read_excel,
        ".odf": pd.read_excel,
        ".ods": pd.read_excel,
        ".odt": pd.read_excel,
    }

    def __init__(self):
        """Initiates the class."""
        self.data_import = None
        self.expected_columns = None

    def import_data(self, file_path):
        """Attempts to import data from a csv or xlsx and checks whether columns are as
        expected."""
        _, file_extension = os.path.splitext(file_path)
        import_func = DataImports.extension_mapping.get(file_extension, None)
        if not import_func:
            raise ValueError(
                f"The file {file_path} is not of the correct type. \n"
                f"It should be one of {set(DataImports.extension_mapping.keys())}"
            )
        self.data_import = import_func(file_path)
        self.column_name_validation(file_path=file_path)
        self.datatype_conversion(file_path=file_path)
        self.contains_rows_validation(file_path=file_path)

    def column_name_validation(self, file_path):
        imported_columns = self.data_import.columns
        if not set(self.expected_columns.keys()).issubset(set(imported_columns)):
            raise ValueError(
                f"The file {file_path} does not contain the correct columns. \n"
                f"The correct columns are {list(self.expected_columns.keys())}"
            )

    def datatype_conversion(self, file_path):
        data_types = copy(self.expected_columns)
        date_included = data_types.pop(StandardLabels.date, None)
        try:
            self.data_import = self.data_import.astype(data_types)
            if date_included:
                self.date_type_conversion()
        except ValueError as err:
            raise ValueError(
                f"The data in {file_path} is not of the correct type. \n{str(err)}"
            )

    def date_type_conversion(self):
        self.data_import[StandardLabels.date] = pd.to_datetime(
            self.data_import[StandardLabels.date],
            dayfirst=True,
        )

    def contains_rows_validation(self, file_path):
        if self.data_import.empty:
            raise ValueError(f"The file {file_path} does not contain any rows of data.")


class DataExports:
    """Parent Class for exporting data."""

    def __init__(self):
        """Initiates the class."""
        self.data_export = None
        self.entry_values = [StandardLabels.y, StandardLabels.n]

    def export_data(
        self,
        filepath,
        sheet_name,
        data_val_cells=None,
        editable_cells=None,
        password=None,
    ):
        """Exports data to a .xlsx.

        Includes formatting of columns and header. Adds data validation to cells
        specified in data_val_cells. Protects all cells except those specified in
        editable_cells. If a password is provided, also password protects the worksheet.
        """
        writer = pd.ExcelWriter(
            filepath,
            engine="xlsxwriter",
            date_format="ddd dd-mm-yyyy",
            datetime_format="ddd dd-mm-yyyy",
        )
        self.data_export.to_excel(writer, sheet_name=sheet_name, index=False)
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]
        workbook.add_format({"border": 1})

        # Create locked and unlocked formats
        locked_format = workbook.add_format({"locked": True})
        unlocked_format = workbook.add_format({"locked": False})
        # Lock all cells
        worksheet.set_column(0, worksheet.dim_colmax, None, locked_format)
        # Unlock specified cells
        if editable_cells:
            for cell in editable_cells:
                worksheet.write(cell, None, unlocked_format)

        # Autofit column widths
        for col_num, value in enumerate(self.data_export.columns.values):
            max_len = (
                max(self.data_export[value].astype(str).map(len).max(), len(str(value)))
                + 6
            )  # Add a little extra space
            worksheet.set_column(col_num, col_num, max_len)

        # Add data validation if specified
        if data_val_cells:
            for i in data_val_cells:
                worksheet.data_validation(
                    i, {"validate": "list", "source": self.entry_values}
                )

        # Protect the worksheet (with or without password)
        if password:
            worksheet.protect(password)
        else:
            worksheet.protect()

        writer.close()

    def autofit_columns(self, filepath, sheet_name):
        """Auto adjusts the width of columns in a specific worksheet of an Excel
        workbook."""
        if platform.system() == "Windows":
            with xw.App(visible=False):
                wb = xw.Book(filepath)
                wb.sheets[sheet_name].autofit(axis="columns")
                wb.save()
                wb.close()

    def print_df_to_pdf(self, df, filepath):
        """Saves a pandas dataframe to a pdf using matplotlib."""
        fig = plt.figure()
        ax = fig.add_subplot(111)
        cell_text = []
        for row in range(len(df)):
            cell_text.append(df.iloc[row])
        ax.table(cellText=cell_text, colLabels=df.columns, loc="center")
        ax.axis("off")
        err = None
        try:
            fig.savefig(filepath)
        except Exception as e:
            err = e
        finally:
            plt.close()
            if err is not None:
                raise Exception(
                    f"An exception of type {type(err).__name__} occurred. \n"
                    f"Arguments:\n {err.args}"
                )

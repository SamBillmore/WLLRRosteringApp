import pandas as pd
import os
import platform
import xlwings as xw
import matplotlib.pyplot as plt


class Data_Imports:
    """Parent Class for importing data."""

    csv_extensions = [".csv"]
    excel_extensions = [
        ".xls",
        ".xlsx",
        ".xlsm",
        ".xlsb",
        ".odf",
        ".ods",
        ".odt",
    ]

    def __init__(self):
        """Initiates the class."""
        self.data_import = None
        self.expected_columns = None

    def import_data(self, file_path):
        """Attempts to import data from a csv or xlsx and checks whether columns are as
        expected."""
        _, file_extension = os.path.splitext(file_path)
        if file_extension in Data_Imports.csv_extensions:
            self.data_import = pd.read_csv(file_path, dtype=self.expected_columns)
        elif file_extension in Data_Imports.excel_extensions:
            self.data_import = pd.read_excel(file_path, dtype=self.expected_columns)
        else:
            raise ValueError(
                f"The file {file_path} is not of the correct type. \n"
                "It should be either .csv or .xlsx"
            )

        self.column_name_validation(file_path=file_path)
        # self.column_type_validation(file_path=file_path)

    def column_name_validation(self, file_path):
        imported_columns = self.data_import.columns
        if set(self.expected_columns.keys()).issubset(set(imported_columns)):
            return
        raise ValueError(
            f"The file {file_path} does not contain the correct columns. \n"
            f"The correct columns are {list(self.expected_columns.keys())}"
        )

    # def column_type_validation(self, file_path):
    #     data_import_types = self.data_import.dtypes.apply(lambda x: x.name).to_dict()
    #     if data_import_types != self.expected_columns:
    #         raise ValueError(
    #             f"The file {file_path} "
    #         )

    #     if "Date" in self.data_import.columns:
    #         self.data_import["Date"] = pd.to_datetime(
    #             self.data_import["Date"], dayfirst=True, infer_datetime_format=True
    #         )


class Data_Exports:
    """Parent Class for exporting data."""

    def __init__(self):
        """Initiates the class."""
        self.data_export = None
        self.entry_values = ["Y", "N"]

    def export_data(self, filepath, sheet_name, data_val_cells=None):
        """Exports data to a .xlsx.

        Includes formatting of columns and header. Adds data validation to cells
        specified in data_val_cells.
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
        if data_val_cells:
            for i in data_val_cells:
                worksheet.data_validation(
                    i, {"validate": "list", "source": self.entry_values}
                )
        writer.close()
        self.autofit_columns(filepath, sheet_name)

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

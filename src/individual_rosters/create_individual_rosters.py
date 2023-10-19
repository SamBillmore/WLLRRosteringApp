import os
import pandas as pd

from import_export.import_export_classes import DataImports
from import_export.import_export_classes import DataExports
from standard_labels.standard_labels import StandardLabels


def create_individual_rosters(final_roster_path, individual_roster_save_folder):
    """Create individual rosters from the final roster."""
    individual_rosters = Individual_Rosters()
    individual_rosters.import_data(final_roster_path)
    individual_rosters.create_individual_rosters(individual_roster_save_folder)


class Individual_Rosters(DataImports, DataExports):
    """Create individual rosters for each crew member."""

    def __init__(self):
        """Initiates the class."""
        self.data_import = None
        self.expected_columns = {
            StandardLabels.date: object,
            StandardLabels.timetable: object,
            StandardLabels.turn: int,
            StandardLabels.driver: object,
            StandardLabels.fireman: object,
            StandardLabels.trainee: object,
        }
        self.fill_na = ""

    def create_individual_rosters(self, save_location):
        """
        Controlling function to:
        - import the final roster
        - create individual rosters for each crew member
        - save them to a specified location as a pdf
        """
        self.data_import.fillna(self.fill_na, inplace=True)
        rostered_individuals = pd.concat(
            [
                self.data_import[StandardLabels.driver],
                self.data_import[StandardLabels.fireman],
                self.data_import[StandardLabels.trainee],
            ]
        ).drop_duplicates()
        for indiv in rostered_individuals:
            if indiv != self.fill_na:
                driver_filter = self.data_import[StandardLabels.driver] == indiv
                fireman_filter = self.data_import[StandardLabels.fireman] == indiv
                trainee_filter = self.data_import[StandardLabels.trainee] == indiv
                indiv_roster_df = self.data_import[
                    driver_filter | fireman_filter | trainee_filter
                ]
                indiv_roster_df = self.change_date_format(
                    indiv_roster_df, StandardLabels.date
                )
                indiv_save_path = os.path.join(
                    save_location, r"Individual roster_" + indiv + ".pdf"
                )
                self.print_df_to_pdf(indiv_roster_df, indiv_save_path)

    def change_date_format(self, df, date_column):
        """
        Amends the date format of a date column in a pandas dataframe to:
        Day of week, Day, Month, Year
        and stores as a string column
        """
        output_df = df.copy()
        output_df[date_column] = df[date_column].dt.strftime("%a %d %m %Y")
        return output_df

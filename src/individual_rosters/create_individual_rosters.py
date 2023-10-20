import os

from import_export.import_export_classes import DataImports
from import_export.import_export_classes import DataExports
from standard_labels.standard_labels import StandardLabels


def create_individual_rosters(final_roster_path, individual_roster_save_folder):
    """Create individual rosters from the final roster."""
    individual_rosters = IndividualRosters()
    individual_rosters.import_data(final_roster_path)
    individual_rosters.create_individual_rosters(individual_roster_save_folder)


class IndividualRosters(DataImports, DataExports):
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
        self.rostered_individuals = None

    def create_individual_rosters(self, save_location):
        """
        Controlling function to:
        - create individual rosters for each crew member
        - save them to a specified location as a pdf
        """
        self.list_rostered_individuals()
        for indiv in self.rostered_individuals:
            indiv_roster_df = self.create_individual_roster_df(indiv)
            indiv_save_path = os.path.join(
                save_location, r"Individual roster_" + indiv + ".pdf"
            )
            self.print_df_to_pdf(indiv_roster_df, indiv_save_path)

    def list_rostered_individuals(self):
        self.rostered_individuals = set(
            self.data_import[StandardLabels.driver].dropna().to_list()
            + self.data_import[StandardLabels.fireman].dropna().to_list()
            + self.data_import[StandardLabels.trainee].dropna().to_list()
        )

    def create_individual_roster_df(self, indiv):
        driver_filter = self.data_import[StandardLabels.driver] == indiv
        fireman_filter = self.data_import[StandardLabels.fireman] == indiv
        trainee_filter = self.data_import[StandardLabels.trainee] == indiv
        indiv_roster_df = self.data_import[
            driver_filter | fireman_filter | trainee_filter
        ]
        indiv_roster_df = self.change_date_format(indiv_roster_df, StandardLabels.date)
        return indiv_roster_df

    def change_date_format(self, df, date_column):
        """
        Amends the date format of a date column in a pandas dataframe to:
        Day of week, Day, Month, Year
        and stores as a string column
        """
        output_df = df.copy()
        output_df[date_column] = df[date_column].dt.strftime("%a %d %m %Y")
        return output_df

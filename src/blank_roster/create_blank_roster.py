from import_export.import_export_classes import Data_Imports
from import_export.import_export_classes import Data_Exports
from blank_availability.create_blank_availability import Timetable


def create_blank_roster(timetable_path, crew_reqs_path, save_location):
    """Creating blank roster."""
    timetable = Timetable()
    crew_reqs = Crew_Requirements()
    blank_roster = Blank_Roster()
    timetable.import_data(timetable_path)
    crew_reqs.import_data(crew_reqs_path)
    blank_roster.create_blank_roster(
        timetable.data_import, crew_reqs.data_import, save_location
    )


class Crew_Requirements(Data_Imports):
    """Crew requirements as input by the user."""

    def __init__(self, crew_reqs=None):
        """Initiates the class."""
        self.data_import = crew_reqs
        self.expected_columns = {"Timetable": object, "Turn": int, "Points": int}


class Blank_Roster(Data_Exports):
    """Blank roster."""

    def __init__(self, timetable=None, crew_requirements=None):
        """Initiates the class."""
        self.timetable = timetable
        self.crew_requirements = crew_requirements
        self.data_export = None
        self.blank_columns = ["Driver", "Fireman", "Trainee"]

    def create_blank_roster(self, timetable, crew_requirements, save_location):
        """Creates the data for the blank roster."""
        sheet_name = "Roster"
        self.timetable = timetable
        self.crew_requirements = crew_requirements
        self.data_export = self.timetable.merge(
            self.crew_requirements, how="left", on="Timetable"
        )
        blank_roster_columns = self.data_export.columns.tolist() + self.blank_columns
        self.data_export = self.data_export.reindex(columns=blank_roster_columns)
        self.export_data(filepath=save_location, sheet_name=sheet_name)

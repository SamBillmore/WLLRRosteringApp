from import_export.import_export_classes import DataImports
from import_export.import_export_classes import DataExports
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


class Crew_Requirements(DataImports):
    """Crew requirements as input by the user."""

    def __init__(self, crew_reqs=None):
        """Initiates the class."""
        self.data_import = crew_reqs
        self.expected_columns = {"Timetable": object, "Turn": int, "Points": int}


class Blank_Roster(DataExports):
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
            self.crew_requirements, how="outer", on="Timetable"
        ).sort_values(["Date", "Turn"], ascending=[True, True])
        blank_roster_columns = self.data_export.columns.tolist() + self.blank_columns
        self.data_export = self.data_export.reindex(columns=blank_roster_columns)
        self.validate_merge()
        self.export_data(filepath=save_location, sheet_name=sheet_name)

    def validate_merge(self):
        not_in_timetable = self.data_export[self.data_export["Date"].isna()]
        not_in_crew_reqs = self.data_export[self.data_export["Turn"].isna()]
        if len(not_in_timetable) > 0:
            raise ValueError(
                "There are entries in the crew requirements file that do not have "
                f"a corresponding entry in the timetable file: \n{not_in_timetable}"
            )
        if len(not_in_crew_reqs) > 0:
            raise ValueError(
                "There are entries in the timetable file "
                "that do not have a corresponding entry in the crew "
                f"requirements file: \n{not_in_crew_reqs}"
            )

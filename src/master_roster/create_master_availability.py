import pandas as pd
import os

from import_export.import_export_classes import Data_Imports
from import_export.import_export_classes import Data_Exports


class Crew_Member(Data_Imports):
    """Availability as input by the user."""

    def __init__(self, availability=None, name=None, grade=None):
        """Initiates the class."""
        self.data_import = availability
        self.name = name
        self.grade = grade
        self.expected_columns = {"Date": object, "Available": object}


class Crew_Members:
    """List of all crew members."""

    def __init__(self):
        """Initiates the class."""
        self.data = []
        self.points_tally = pd.DataFrame()

    def create_points_tally(self):
        """Creates the points tally attribute containing a list of crew and their points
        initially set to zero."""
        self.points_tally = pd.DataFrame(
            [[crew_member.name, 0] for crew_member in self.data],
            columns=["Name", "Points"],
        )


class Master_Availability(Data_Exports):
    """Master list of availability."""

    def __init__(self, individual_availability=None):
        """Initiates the class."""
        self.individual_availability = individual_availability
        self.data_export = pd.DataFrame()

    def create_master_availability(self, grade, availability_folder, crew_members):
        """Importing availability from completed availability forms.

        Creates individual crew member objects and adds to crew_members list. Creates
        master availability form.
        """
        for file_name in os.listdir(availability_folder):
            crew_member = Crew_Member()
            crew_member.name = file_name.split(".")[0]
            crew_member.grade = grade
            file_path = os.path.join(availability_folder + "/" + file_name)
            crew_member.import_data(file_path)
            self.append_availability(crew_member)
            crew_members.data.append(crew_member)

    def append_availability(self, crew_member):
        """Appends an individual's availability to the master list."""
        availability = crew_member.data_import
        availability.insert(
            1, "Name", [crew_member.name for i in range(len(availability))]
        )
        availability.insert(
            1, "Grade", [crew_member.grade for i in range(len(availability))]
        )
        self.data_export = pd.concat([self.data_export, availability])
        self.data_export = self.data_export[self.data_export["Available"] == "Y"]

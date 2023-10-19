import pandas as pd
import numpy as np
import os

from import_export.import_export_classes import DataImports
from import_export.import_export_classes import DataExports


def create_master_availability(
    driver_availability_folder, fireman_availability_folder, trainee_availability_folder
):
    availability_folders = {
        "Driver": driver_availability_folder,
        "Fireman": fireman_availability_folder,
        "Trainee": trainee_availability_folder,
    }
    master_availabilty = MasterAvailability()
    for key, value in availability_folders.items():
        master_availabilty.create_crew_member_objects(key, value)
    master_availabilty.data_export.sort_values(
        by=["Grade", "Date", "Name"], inplace=True
    )
    master_availabilty.data_export.reset_index(drop=True, inplace=True)
    return master_availabilty


class MasterAvailability(DataExports):
    """Master list of availability."""

    def __init__(self):
        """Initiates the class."""
        self.crew_members = []
        self.data_export = pd.DataFrame()

    def create_crew_member_objects(self, grade, availability_folder):
        """Importing availability from completed availability forms.

        Creates individual crew member objects and adds to crew_members list. Creates
        master availability form.
        """
        for file_name in os.listdir(availability_folder):
            crew_member = CrewMember()
            crew_member.name = file_name.split(".")[0]
            crew_member.grade = grade
            file_path = os.path.join(availability_folder, file_name)
            crew_member.import_data(file_path)
            crew_member.validate_data(file_path)
            self.append_availability(crew_member)
            self.crew_members.append(crew_member)

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


class CrewMember(DataImports):
    """Availability as input by the user."""

    valid_availability_values = {"Y", "N", None, np.nan}

    def __init__(self, availability=None, name=None, grade=None):
        """Initiates the class."""
        self.data_import = availability
        self.name = name
        self.grade = grade
        self.expected_columns = {"Date": object, "Available": object}

    def validate_data(self, file_path):
        self.validate_columns(file_path=file_path)
        self.validate_availability_column(file_path=file_path)

    def validate_columns(self, file_path):
        actual_columns = set(self.data_import.columns)
        expected_columns = set(self.expected_columns.keys())
        if not actual_columns.issubset(expected_columns):
            raise ValueError(
                f"The file {file_path} contains additional unexpected columns"
            )

    def validate_availability_column(self, file_path):
        available_column = set(self.data_import["Available"])
        bad_entries = available_column - CrewMember.valid_availability_values
        if bad_entries:
            raise ValueError(
                f"The file {file_path} contains invalid entries in the "
                f"'Available' column: {bad_entries}"
            )

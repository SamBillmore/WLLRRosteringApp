from pathlib import Path
import pandas as pd
import numpy as np
import os

from import_export.import_export_classes import DataImports
from import_export.import_export_classes import DataExports
from standard_labels.standard_labels import StandardLabels


def create_master_availability(
    driver_availability_folder, fireman_availability_folder, trainee_availability_folder
):
    availability_folders = {
        StandardLabels.driver: driver_availability_folder,
        StandardLabels.fireman: fireman_availability_folder,
        StandardLabels.trainee: trainee_availability_folder,
    }
    master_availabilty = MasterAvailability()
    for key, value in availability_folders.items():
        master_availabilty.create_crew_member_objects(key, value)
    master_availabilty.data_export.sort_values(
        by=[StandardLabels.grade, StandardLabels.date, StandardLabels.name],
        inplace=True,
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
        directories_in_availability_folder = []
        for path in os.listdir(availability_folder):
            path_is_directory = self.check_path_is_directory(
                grade, availability_folder, path
            )
            if path_is_directory:
                directories_in_availability_folder.append(path)
            if len(directories_in_availability_folder) == 0:
                self.create_crew_member_object(
                    grade=grade,
                    availability_folder=availability_folder,
                    path=path,
                )
        if len(directories_in_availability_folder) > 0:
            self.raise_directories_found_error(
                directories_in_availability_folder=directories_in_availability_folder,
                availability_folder=availability_folder,
                grade=grade,
            )

    def create_crew_member_object(self, grade, availability_folder, path):
        """Creates a single crew member object."""
        crew_member = CrewMember()
        crew_member.name = path.split(".")[0]
        crew_member.grade = grade
        file_path = os.path.join(availability_folder, path)
        crew_member.import_data(file_path)
        crew_member.validate_data(file_path)
        self.append_availability(crew_member)
        self.crew_members.append(crew_member)

    def check_path_is_directory(self, grade, availability_folder, path):
        """Validates directory only contains files."""
        path_to_validate = os.path.join(availability_folder, path)
        return os.path.isdir(path_to_validate)

    def append_availability(self, crew_member):
        """Appends an individual's availability to the master list."""
        availability = crew_member.data_import
        availability.insert(
            1, StandardLabels.name, [crew_member.name for i in range(len(availability))]
        )
        availability.insert(
            1,
            StandardLabels.grade,
            [crew_member.grade for i in range(len(availability))],
        )
        self.data_export = pd.concat([self.data_export, availability])
        self.data_export = self.data_export[
            self.data_export[StandardLabels.available] == StandardLabels.y
        ]

    def raise_directories_found_error(
        self, directories_in_availability_folder, availability_folder, grade
    ):
        """Raises error if directories found in availability directory."""
        directories_string = ""
        directories_in_availability_folder.sort()
        for directory in directories_in_availability_folder:
            directories_string = directories_string + f"- {directory}\n"
        msg = (
            f"Error getting the {grade} availability files from the directory: "
            f"{Path(availability_folder).name}\n\n"
            "Did you mean to select one of the following locations?\n"
            f"{directories_string}\n"
            "When selecting the location of the availability files, please "
            "DOUBLE CLICK on the directory name to select it.\n\n"
            "The directory should only contain the availability files and "
            "nothing else.\n\n"
            f"Full selected location: {availability_folder}"
        )
        raise ValueError(msg)


class CrewMember(DataImports):
    """Availability as input by the user."""

    valid_availability_values = {StandardLabels.y, StandardLabels.n, None, np.nan}

    def __init__(self, availability=None, name=None, grade=None):
        """Initiates the class."""
        self.data_import = availability
        self.name = name
        self.grade = grade
        self.expected_columns = {
            StandardLabels.date: object,
            StandardLabels.available: object,
        }

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
        available_column = set(self.data_import[StandardLabels.available])
        bad_entries = available_column - CrewMember.valid_availability_values
        if bad_entries:
            raise ValueError(
                f"The file {file_path} contains invalid entries in the "
                f"'{StandardLabels.available}' column: {bad_entries}"
            )

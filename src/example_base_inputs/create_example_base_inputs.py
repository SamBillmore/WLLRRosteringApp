import pandas as pd
import os
import numpy as np

from import_export.import_export_classes import DataExports
from standard_labels.standard_labels import StandardLabels


def create_example_base_inputs(save_location):
    example_base_inputs = ExampleBaseInputs()
    example_base_inputs.create_base_inputs_controller(save_location=save_location)


class ExampleBaseInputs(DataExports):
    """Example base inputs."""

    def __init__(self):
        """Initiates the class."""
        self.data_export = None

    def create_base_inputs_controller(self, save_location):
        self.create_example_timetable(save_location=save_location)
        self.create_example_crew_reqs(save_location=save_location)
        self.create_availability_folders(save_location=save_location)

    def create_example_timetable(self, save_location):
        sheet_name = "Timetable"
        self.data_export = pd.DataFrame(
            {
                StandardLabels.date: [
                    pd.to_datetime("21/01/2023", dayfirst=True),
                    pd.to_datetime("22/01/2023", dayfirst=True),
                    pd.to_datetime("23/01/2023", dayfirst=True),
                ],
                StandardLabels.timetable: ["Blue", "Yellow", "Blue"],
            }
        )
        filepath = os.path.join(save_location, "example_timetable_dates_colours.xlsx")
        self.export_data(filepath=filepath, sheet_name=sheet_name)

    def create_example_crew_reqs(self, save_location):
        sheet_name = "CrewReqs"
        self.data_export = pd.DataFrame(
            {
                "Timetable": ["Blue", "Blue", "Yellow", "Yellow", "Yellow"],
                "Turn": [
                    np.int64(0),
                    np.int64(1),
                    np.int64(1),
                    np.int64(2),
                    np.int64(3),
                ],
                "Points": [
                    np.int64(0),
                    np.int64(4),
                    np.int64(3),
                    np.int64(4),
                    np.int64(2),
                ],
            }
        )
        filepath = os.path.join(save_location, "example_crew_reqs_by_colour.xlsx")
        self.export_data(filepath=filepath, sheet_name=sheet_name)

    def create_availability_folders(self, save_location):
        folders_to_create = [
            StandardLabels.driver,
            StandardLabels.fireman,
            StandardLabels.trainee,
        ]
        for folder in folders_to_create:
            path_to_create = os.path.join(save_location, folder + " availability")
            os.mkdir(path_to_create)

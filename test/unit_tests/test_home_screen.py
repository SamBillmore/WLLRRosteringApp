from unittest import mock
import os
import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal
from tkinter import END


@mock.patch("user_interface.blank_roster_screen.filedialog.askdirectory")
def test_correct(askdirectory, app, tmp_path):
    # Given some input data and initial state
    output_dir = tmp_path / "output_data"
    output_dir.mkdir()

    home_screen = app.frames["HomeScreen"]

    # When we run the function
    askdirectory.return_value = output_dir
    home_screen.run_create_example_base_inputs()

    # Then the files are created as expected
    expected_timetable_path = os.path.join(
        output_dir, "example_timetable_dates_colours.xlsx"
    )
    assert os.path.exists(expected_timetable_path)
    expected_crew_reqs_path = os.path.join(
        output_dir, "example_crew_reqs_by_colour.xlsx"
    )
    assert os.path.exists(expected_crew_reqs_path)
    expected_timetable_data = pd.DataFrame(
        {
            "Date": [
                pd.to_datetime("21/01/2023", dayfirst=True),
                pd.to_datetime("22/01/2023", dayfirst=True),
                pd.to_datetime("23/01/2023", dayfirst=True),
            ],
            "Timetable": ["Blue", "Yellow", "Blue"],
        }
    )
    actual_timetable_data = pd.read_excel(
        expected_timetable_path, dtype={"Date": object, "Timetable": object}
    )
    assert_frame_equal(actual_timetable_data, expected_timetable_data)
    expected_crew_reqs_data = pd.DataFrame(
        {
            "Timetable": ["Blue", "Blue", "Yellow", "Yellow", "Yellow"],
            "Turn": [np.int64(0), np.int64(1), np.int64(1), np.int64(2), np.int64(3)],
            "Points": [np.int64(0), np.int64(4), np.int64(3), np.int64(4), np.int64(2)],
        }
    )
    actual_crew_reqs_data = pd.read_excel(
        expected_crew_reqs_path,
        dtype={"Timetable": object, "Turn": np.int64, "Points": np.int64},
    )
    assert_frame_equal(actual_crew_reqs_data, expected_crew_reqs_data)


@mock.patch("user_interface.blank_roster_screen.filedialog.askdirectory")
def test_errors_raised_correctly(askdirectory, app):
    # Given some initial state and input data that will raise an error
    home_screen = app.frames["HomeScreen"]

    # When we run the function
    askdirectory.return_value = "dummy_location.xlsx"
    home_screen.run_create_example_base_inputs()

    # Then the error is raised correctly
    assert app.visible_frame == "ErrorScreen"
    error_screen = app.frames["ErrorScreen"]
    assert (
        error_screen.error_message.get(1.0, END)
        == "Cannot save file into a non-existent directory: 'dummy_location.xlsx'\n"
    )

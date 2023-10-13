from unittest import mock
import os
import pandas as pd
from pandas.testing import assert_frame_equal


@mock.patch("user_interface.allocate_crews_screen.filedialog.asksaveasfilename")
def test_real_files(asksaveasfilename, app, tmp_path):
    # Given some input data and initial state
    input_working_file = "./test/unit_tests/input_data/Working Roster.xlsx"
    assert os.path.exists(input_working_file)
    input_driver_dir = "./test/unit_tests/input_data/01 Driver availability"
    input_fireman_dir = "./test/unit_tests/input_data/02 Fireman availability"
    input_trainee_dir = "./test/unit_tests/input_data/03 Trainee availability"
    assert os.path.exists(input_driver_dir)
    assert os.path.exists(input_fireman_dir)
    assert os.path.exists(input_trainee_dir)

    allocate_crews_screen = app.frames["AllocateCrewsScreen"]

    dir = tmp_path / "data"
    dir.mkdir()
    output_file = dir / "output_data.xlsx"

    # When we run the function
    asksaveasfilename.return_value = output_file
    allocate_crews_screen.run_create_master_roster(
        working_roster_path=input_working_file,
        driver_availability_folder=input_driver_dir,
        fireman_availability_folder=input_fireman_dir,
        trainee_availability_folder=input_trainee_dir,
    )

    # Then the file is created as expected
    assert os.path.exists(output_file)
    expected_data = pd.DataFrame(
        {
            "Date": [
                pd.to_datetime("10/02/2018", dayfirst=True),
                pd.to_datetime("11/02/2018", dayfirst=True),
                pd.to_datetime("11/02/2018", dayfirst=True),
                pd.to_datetime("11/02/2018", dayfirst=True),
                pd.to_datetime("14/02/2018", dayfirst=True),
                pd.to_datetime("15/02/2018", dayfirst=True),
                pd.to_datetime("17/02/2018", dayfirst=True),
                pd.to_datetime("18/02/2018", dayfirst=True),
                pd.to_datetime("18/02/2018", dayfirst=True),
                pd.to_datetime("18/02/2018", dayfirst=True),
                pd.to_datetime("21/02/2018", dayfirst=True),
                pd.to_datetime("22/02/2018", dayfirst=True),
                pd.to_datetime("24/02/2018", dayfirst=True),
                pd.to_datetime("25/02/2018", dayfirst=True),
            ],
            "Timetable": [
                "Purple",
                "Yellow",
                "Yellow",
                "Yellow",
                "Purple",
                "Purple",
                "Purple",
                "Yellow",
                "Yellow",
                "Yellow",
                "Purple",
                "Purple",
                "Purple",
                "Purple",
            ],
            "Turn": [1, 1, 2, 3, 1, 1, 1, 1, 2, 3, 1, 1, 1, 1],
            "Driver": [
                "John Travis",
                "James Newby",
                "John Travis",
                "John Bancroft",
                "John Bancroft",
                "John Bancroft",
                "James Newby",
                None,
                "John Bancroft",
                None,
                "John Bancroft",
                "John Bancroft",
                "John Travis",
                "James Newby",
            ],
            "Fireman": [
                "Megan Charman",
                "Joe Gunby",
                "Kate Billmore",
                "Megan Charman",
                "John Travis",
                "Kate Billmore",
                "Joe Gunby",
                None,
                "Rowan Joachim",
                None,
                "Rowan Joachim",
                "Kate Billmore",
                "Megan Charman",
                "Rowan Joachim",
            ],
            "Trainee": [
                "Sam Billmore",
                "Sam Billmore",
                "Stewart Charman",
                "Harry Billmore",
                "Harry Billmore",
                "Harry Billmore",
                "Sam Billmore",
                None,
                None,
                None,
                "Stewart Charman",
                None,
                None,
                None,
            ],
        }
    )
    actual_data = pd.read_excel(
        output_file, dtype={"Driver": object, "Fireman": object, "Trainee": object}
    )
    assert_frame_equal(actual_data, expected_data)


@mock.patch("user_interface.allocate_crews_screen.filedialog.asksaveasfilename")
def test_errors_raised_correctly(asksaveasfilename, app):
    # Given some initial state and input data that will raise an error
    allocate_crews_screen = app.frames["AllocateCrewsScreen"]
    file_name = "bad_path.csv"

    # When we run the function
    asksaveasfilename.return_value = "dummy_location.xlsx"
    allocate_crews_screen.run_create_master_roster(
        file_name, file_name, file_name, file_name
    )

    # Then the error is raised correctly
    assert app.visible_frame == "ErrorScreen"
    error_screen = app.frames["ErrorScreen"]
    assert (
        error_screen.error_message["text"]
        == "[Errno 2] No such file or directory: 'bad_path.csv'"
    )

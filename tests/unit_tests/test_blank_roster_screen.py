from unittest import mock
import os
import pandas as pd
from pandas.testing import assert_frame_equal
from tkinter import END


@mock.patch("user_interface.blank_roster_screen.filedialog.asksaveasfilename")
def test_correct(asksaveasfilename, app, tmp_path):
    # Given some input data and initial state
    dir = tmp_path / "data"
    dir.mkdir()
    input_timetable_file = dir / "timetable_data.xlsx"
    timetable_data = pd.DataFrame({"Date": ["21/01/2023"], "Timetable": ["Blue"]})
    timetable_data.to_excel(input_timetable_file, index=False)
    assert os.path.exists(input_timetable_file)
    input_crew_reqs = dir / "crew_reqs.xlsx"
    crew_reqs_data = pd.DataFrame(
        {"Timetable": ["Blue", "Blue"], "Turn": [1, 2], "Points": [4, 3]}
    )
    crew_reqs_data.to_excel(input_crew_reqs, index=False)
    assert os.path.exists(input_crew_reqs)

    blank_roster_screen = app.frames["BlankRosterScreen"]

    output_file = dir / "output_data.xlsx"

    # When we run the function
    asksaveasfilename.return_value = output_file
    blank_roster_screen.run_create_blank_roster(input_timetable_file, input_crew_reqs)

    # Then the file is created as expected
    assert os.path.exists(output_file)
    expected_data = pd.DataFrame(
        {
            "Date": [
                pd.to_datetime("21/01/2023", dayfirst=True),
                pd.to_datetime("21/01/2023", dayfirst=True),
            ],
            "Timetable": ["Blue", "Blue"],
            "Turn": [1, 2],
            "Points": [4, 3],
            "Driver": [None, None],
            "Fireman": [None, None],
            "Trainee": [None, None],
        }
    )
    actual_data = pd.read_excel(
        output_file, dtype={"Driver": object, "Fireman": object, "Trainee": object}
    )
    assert_frame_equal(actual_data, expected_data)


@mock.patch("user_interface.blank_roster_screen.filedialog.asksaveasfilename")
def test_real_files(asksaveasfilename, app, tmp_path):
    # Given some input data and initial state
    input_timetable_file = "./tests/input_data/Timetable.xlsx"
    assert os.path.exists(input_timetable_file)
    input_crew_reqs_file = "./tests/input_data/Crew requirements.csv"
    assert os.path.exists(input_crew_reqs_file)

    blank_roster_screen = app.frames["BlankRosterScreen"]

    dir = tmp_path / "data"
    dir.mkdir()
    output_file = dir / "output_data.xlsx"

    # When we run the function
    asksaveasfilename.return_value = output_file
    blank_roster_screen.run_create_blank_roster(
        timetable_path=input_timetable_file, crew_reqs_path=input_crew_reqs_file
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
            "Points": [6, 3, 4, 2, 6, 6, 6, 3, 4, 2, 6, 6, 6, 6],
            "Driver": [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            ],
            "Fireman": [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            ],
            "Trainee": [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
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


@mock.patch("user_interface.blank_roster_screen.filedialog.asksaveasfilename")
def test_errors_raised_correctly(asksaveasfilename, app):
    # Given some initial state and input data that will raise an error
    blank_roster_screen = app.frames["BlankRosterScreen"]
    file_name = "bad_path.csv"

    # When we run the function
    asksaveasfilename.return_value = "dummy_location.xlsx"
    blank_roster_screen.run_create_blank_roster(file_name, file_name)

    # Then the error is raised correctly
    assert app.visible_frame == "ErrorScreen"
    error_screen = app.frames["ErrorScreen"]
    assert (
        error_screen.error_message.get(1.0, END)
        == "[Errno 2] No such file or directory: 'bad_path.csv'\n"
    )


@mock.patch("user_interface.blank_roster_screen.filedialog.asksaveasfilename")
def test_cancel(asksaveasfilename, app, tmp_path):
    # Given some input data and initial state
    dir = tmp_path / "data"
    dir.mkdir()
    input_timetable_file = dir / "timetable_data.xlsx"
    timetable_data = pd.DataFrame({"Date": ["21/01/2023"], "Timetable": ["Blue"]})
    timetable_data.to_excel(input_timetable_file, index=False)
    assert os.path.exists(input_timetable_file)
    input_crew_reqs = dir / "crew_reqs.xlsx"
    crew_reqs_data = pd.DataFrame(
        {"Timetable": ["Blue", "Blue"], "Turn": [1, 2], "Points": [4, 3]}
    )
    crew_reqs_data.to_excel(input_crew_reqs, index=False)
    assert os.path.exists(input_crew_reqs)

    app.visible_frame = "BlankRosterScreen"
    blank_roster_screen = app.frames["BlankRosterScreen"]

    # When we run the function and click cancel
    asksaveasfilename.return_value = ()
    blank_roster_screen.run_create_blank_roster(input_timetable_file, input_crew_reqs)

    # Then the app remains on the correct screen
    assert app.visible_frame == "BlankRosterScreen"

    # And if we run the function and click cancel again
    asksaveasfilename.return_value = ""
    blank_roster_screen.run_create_blank_roster(input_timetable_file, input_crew_reqs)

    # Then the app remains on the correct screen
    assert app.visible_frame == "BlankRosterScreen"

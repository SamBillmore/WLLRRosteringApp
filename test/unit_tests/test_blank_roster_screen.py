from unittest import mock
import os
import pandas as pd
from pandas.testing import assert_frame_equal


if os.environ.get("DISPLAY", "") == "":
    print("no display found. Using :0.0")
    os.environ.__setitem__("DISPLAY", ":0.0")


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
def test_errors_raised_correctly(asksaveasfilename, app, tmp_path):
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
        error_screen.error_message["text"]
        == "[Errno 2] No such file or directory: 'bad_path.csv'"
    )

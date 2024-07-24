from unittest import mock
import os
import pandas as pd
from pandas.testing import assert_frame_equal
from tkinter import END


@mock.patch("user_interface.blank_availability_screen.filedialog.asksaveasfilename")
def test_correct(asksaveasfilename, app, tmp_path):
    # Given some input data and initial state
    dir = tmp_path / "data"
    dir.mkdir()
    input_file = dir / "valid_data.xlsx"
    input_data = pd.DataFrame({"Date": ["21/01/2023"], "Timetable": ["Blue"]})
    input_data.to_excel(input_file, index=False)
    assert os.path.exists(input_file)

    blank_availability_screen = app.frames["BlankAvailabilityScreen"]

    output_file = dir / "output_data.xlsx"

    # When we run the function
    asksaveasfilename.return_value = output_file
    blank_availability_screen.run_create_blank_availability(input_file)

    # Then the file is created as expected
    assert os.path.exists(output_file)
    expected_data = pd.DataFrame(
        {"Date": [pd.to_datetime("21/01/2023", dayfirst=True)], "Available": [None]}
    )
    actual_data = pd.read_excel(output_file, dtype={"Available": object})
    assert_frame_equal(actual_data, expected_data)


@mock.patch("user_interface.blank_availability_screen.filedialog.asksaveasfilename")
def test_real_file(asksaveasfilename, app, tmp_path):
    # Given some input data and initial state
    input_file = "./tests/input_data/Timetable.xlsx"
    assert os.path.exists(input_file)

    blank_availability_screen = app.frames["BlankAvailabilityScreen"]

    dir = tmp_path / "data"
    dir.mkdir()
    output_file = dir / "output_data.xlsx"

    # When we run the function
    asksaveasfilename.return_value = output_file
    blank_availability_screen.run_create_blank_availability(input_file)

    # Then the file is created as expected
    assert os.path.exists(output_file)
    expected_data = pd.DataFrame(
        {
            "Date": [
                pd.to_datetime("10/02/2018", dayfirst=True),
                pd.to_datetime("11/02/2018", dayfirst=True),
                pd.to_datetime("14/02/2018", dayfirst=True),
                pd.to_datetime("15/02/2018", dayfirst=True),
                pd.to_datetime("17/02/2018", dayfirst=True),
                pd.to_datetime("18/02/2018", dayfirst=True),
                pd.to_datetime("21/02/2018", dayfirst=True),
                pd.to_datetime("22/02/2018", dayfirst=True),
                pd.to_datetime("24/02/2018", dayfirst=True),
                pd.to_datetime("25/02/2018", dayfirst=True),
            ],
            "Available": [None, None, None, None, None, None, None, None, None, None],
        }
    )
    actual_data = pd.read_excel(output_file, dtype={"Available": object})
    assert_frame_equal(actual_data, expected_data)


@mock.patch("user_interface.blank_availability_screen.filedialog.asksaveasfilename")
def test_errors_raised_correctly(asksaveasfilename, app):
    # Given an initial state and inputs that will raise an error
    blank_availability_screen = app.frames["BlankAvailabilityScreen"]
    file_name = "bad_path.csv"

    # When we run the function
    asksaveasfilename.return_value = "dummy_location.xlsx"
    blank_availability_screen.run_create_blank_availability(file_name)

    # Then the error is raised correctly
    assert app.visible_frame == "ErrorScreen"
    error_screen = app.frames["ErrorScreen"]
    assert (
        error_screen.error_message.get(1.0, END)
        == "[Errno 2] No such file or directory: 'bad_path.csv'\n"
    )


@mock.patch("user_interface.blank_availability_screen.filedialog.asksaveasfilename")
def test_cancel(asksaveasfilename, app, tmp_path):
    # Given some input data and initial state
    dir = tmp_path / "data"
    dir.mkdir()
    input_file = dir / "valid_data.xlsx"
    input_data = pd.DataFrame({"Date": ["21/01/2023"], "Timetable": ["Blue"]})
    input_data.to_excel(input_file, index=False)
    assert os.path.exists(input_file)

    app.visible_frame = "BlankAvailabilityScreen"
    blank_availability_screen = app.frames["BlankAvailabilityScreen"]

    # When we run the function and click cancel
    asksaveasfilename.return_value = ()
    blank_availability_screen.run_create_blank_availability(input_file)

    # Then the app remains on the correct screen
    assert app.visible_frame == "BlankAvailabilityScreen"

    # And if we run the function and click cancel again
    asksaveasfilename.return_value = ""
    blank_availability_screen.run_create_blank_availability(input_file)

    # Then the app remains on the correct screen
    assert app.visible_frame == "BlankAvailabilityScreen"

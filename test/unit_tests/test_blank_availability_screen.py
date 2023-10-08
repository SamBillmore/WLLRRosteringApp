from unittest import mock
import pytest
import os
import pandas as pd
from pandas.testing import assert_frame_equal

from user_interface.app_container import App
from blank_availability.create_blank_availability import Timetable

SCOPE = "session"


@pytest.fixture(scope=SCOPE)
def app():
    app = App()
    yield app


@mock.patch("user_interface.blank_availability_screen.filedialog.asksaveasfilename")
def test_real_file(asksaveasfilename, app, tmp_path):
    # Given some input data and initial state
    input_file = "./test/unit_tests/input_data/Timetable.xlsx"
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
    expected_data.head()
    actual_data = pd.read_excel(output_file, dtype={"Available": object})
    assert_frame_equal(actual_data, expected_data)


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
        {"Date": [pd.to_datetime("21/01/2023")], "Available": [None]}
    )
    actual_data = pd.read_excel(output_file, dtype={"Available": object})
    assert_frame_equal(actual_data, expected_data)


@mock.patch("user_interface.blank_availability_screen.filedialog.asksaveasfilename")
def test_error_handling_no_file(asksaveasfilename, app):
    # Given an initial state
    blank_availability_screen = app.frames["BlankAvailabilityScreen"]

    # When we run the function
    asksaveasfilename.return_value = "dummy_location.xlsx"
    blank_availability_screen.run_create_blank_availability("bad_path.csv")

    # Then the error is raised correctly
    error_screen = app.frames["ErrorScreen"]
    assert (
        error_screen.error_message["text"]
        == "[Errno 2] No such file or directory: 'bad_path.csv'"
    )
    assert app.visible_frame == "ErrorScreen"


@mock.patch("user_interface.blank_availability_screen.filedialog.asksaveasfilename")
def test_error_handling_incorrect_filetype(asksaveasfilename, tmp_path, app):
    # Given an initial state
    blank_availability_screen = app.frames["BlankAvailabilityScreen"]
    dir = tmp_path / "input_data"
    dir.mkdir()
    file = dir / "bad_file_type.txt"
    file.write_text("content")
    assert os.path.exists(file)

    # When we run the function
    asksaveasfilename.return_value = "dummy_location.xlsx"
    blank_availability_screen.run_create_blank_availability(file)

    # Then the error is raised correctly
    error_screen = app.frames["ErrorScreen"]
    err_msg = (
        f"The file {file} is not of the correct type. \nIt should be "
        "either .csv or .xlsx"
    )
    assert error_screen.error_message["text"] == err_msg
    assert app.visible_frame == "ErrorScreen"


@mock.patch("user_interface.blank_availability_screen.filedialog.asksaveasfilename")
def test_error_handling_incorrect_columns_csv(asksaveasfilename, tmp_path, app):
    # Given an initial state
    blank_availability_screen = app.frames["BlankAvailabilityScreen"]
    dir = tmp_path / "input_data"
    dir.mkdir()
    file = dir / "incorrect_columns.csv"
    pd.DataFrame({"column_1": ["abc"], "column_2": ["def"]}).to_csv(file, index=False)
    assert os.path.exists(file)

    # When we run the function
    asksaveasfilename.return_value = "dummy_location.xlsx"
    blank_availability_screen.run_create_blank_availability(file)

    # Then the error is raised correctly
    error_screen = app.frames["ErrorScreen"]
    timetable = Timetable()
    err_msg = (
        f"The file {file} does not contain the correct columns. \nThe "
        f"correct columns are {list(timetable.expected_columns.keys())}"
    )
    assert error_screen.error_message["text"] == err_msg
    assert app.visible_frame == "ErrorScreen"


@mock.patch("user_interface.blank_availability_screen.filedialog.asksaveasfilename")
def test_error_handling_incorrect_columns_xlsx(asksaveasfilename, tmp_path, app):
    # Given an initial state
    blank_availability_screen = app.frames["BlankAvailabilityScreen"]
    dir = tmp_path / "input_data"
    dir.mkdir()
    file = dir / "incorrect_columns.xlsx"
    pd.DataFrame({"column_1": ["abc"], "column_2": ["def"]}).to_excel(file, index=False)
    assert os.path.exists(file)

    # When we run the function
    asksaveasfilename.return_value = "dummy_location.xlsx"
    blank_availability_screen.run_create_blank_availability(file)

    # Then the error is raised correctly
    error_screen = app.frames["ErrorScreen"]
    timetable = Timetable()
    err_msg = (
        f"The file {file} does not contain the correct columns. \nThe "
        f"correct columns are {list(timetable.expected_columns.keys())}"
    )
    assert error_screen.error_message["text"] == err_msg
    assert app.visible_frame == "ErrorScreen"

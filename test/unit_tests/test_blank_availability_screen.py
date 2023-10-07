from unittest import mock
import pytest
import os
import pandas as pd

from user_interface.app_container import App
from blank_availability.create_blank_availability import Timetable

SCOPE = "session"


@pytest.fixture(scope=SCOPE)
def app():
    app = App()
    yield app


@mock.patch("user_interface.blank_availability_screen.filedialog.asksaveasfilename")
def test_error_handling_no_file(asksaveasfilename, app):
    # Given an initial state
    blank_availability_screen = app.frames["BlankAvailabilityScreen"]

    # When we run the function
    asksaveasfilename.return_value = "dummy_location.csv"
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
    asksaveasfilename.return_value = "dummy_location.csv"
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
    asksaveasfilename.return_value = "dummy_location.csv"
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
    asksaveasfilename.return_value = "dummy_location.csv"
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


# @mock.patch('user_interface.blank_availability_screen.filedialog.asksaveasfilename')
# def test_error_handling_incorrect_columns_types_xlsx(asksaveasfilename, tmp_path, app)
#     # Given an initial state
#     blank_availability_screen = app.frames['BlankAvailabilityScreen']
#     dir = tmp_path / "input_data"
#     dir.mkdir()
#     file = dir / "incorrect_columns.xlsx"
#     pd.DataFrame({
#         "Date": [1],
#         "Timetable": [2]
#     }).to_excel(file, index=False)
#     assert os.path.exists(file)

#     # When we run the function
#     asksaveasfilename.return_value = 'dummy_location.csv'
#     blank_availability_screen.run_create_blank_availability(file)

#     # Then the error is raised correctly
#     error_screen = app.frames['ErrorScreen']
#     print(error_screen.full_traceback["text"])
#     timetable = Timetable()
#     err_msg = f"The file {file} does not contain the correct columns. \nThe " \
#         "correct columns are {timetable.expected_columns}"
#     assert error_screen.error_message["text"] == err_msg
#     assert app.visible_frame == "ErrorScreen"

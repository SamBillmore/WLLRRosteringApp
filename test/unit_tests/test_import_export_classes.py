import pytest
import pandas as pd
import re
from pandas.testing import assert_frame_equal
import os

from blank_roster.create_blank_roster import Crew_Requirements
from blank_availability.create_blank_availability import Timetable


def test_import_validation(tmp_path):
    # Given some valid input data and initial state
    dir = tmp_path / "input_data"
    dir.mkdir()
    file = dir / "valid_data.xlsx"
    input_data = pd.DataFrame({"Timetable": ["Blue"], "Turn": [1], "Points": [5]})
    input_data.to_excel(file, index=False)
    assert os.path.exists(file)

    crew_reqs = Crew_Requirements()
    crew_reqs.expected_columns = {"Timetable": object, "Turn": int, "Points": int}

    # When we import data
    crew_reqs.import_data(file)

    # Then the data imported is as expected
    assert_frame_equal(crew_reqs.data_import, input_data)


def test_import_validation_dates(tmp_path):
    # Given some valid input data (containing dates) and initial state
    dir = tmp_path / "input_data"
    dir.mkdir()
    file = dir / "valid_data_dates.xlsx"
    input_data = pd.DataFrame({"Date": ["21/01/2023"], "Timetable": ["Blue"]})
    input_data.to_excel(file, index=False)
    assert os.path.exists(file)

    timetable = Timetable()
    timetable.expected_columns = {"Date": object, "Timetable": object}

    # When we import data
    timetable.import_data(file)

    # Then the data imported is as expected
    expected_data = pd.DataFrame(
        {"Date": [pd.to_datetime("21/01/2023")], "Timetable": ["Blue"]}
    )
    assert_frame_equal(timetable.data_import, expected_data)


def test_import_validation_no_file():
    # Given an incorrect filename
    file = "bad_path.csv"

    crew_reqs = Crew_Requirements()

    # When we try to import the data then the correct exception is raised
    expected_error = re.escape("[Errno 2] No such file or directory: 'bad_path.csv'")
    with pytest.raises(FileNotFoundError, match=expected_error):
        crew_reqs.import_data(file)


def test_import_validation_incorrect_filetype(tmp_path):
    # Given an invalid file type
    dir = tmp_path / "input_data"
    dir.mkdir()
    file = dir / "bad_file_type.txt"
    file.write_text("content")
    assert os.path.exists(file)

    crew_reqs = Crew_Requirements()

    # When we try to import the data then the correct exception is raised
    expected_error = (
        f"The file {file} is not of the correct type. \nIt should be one of "
    )
    with pytest.raises(ValueError, match=expected_error):
        crew_reqs.import_data(file)


def test_import_validation_incorrect_dtype(tmp_path):
    # Given some invalid data (where the data type is incorrect)
    dir = tmp_path / "input_data"
    dir.mkdir()
    file = dir / "incorrect_dtypes.xlsx"
    input_data = pd.DataFrame(
        {
            "Timetable": ["Blue"],
            "Turn": ["Bad string"],
            "Points": ["Another bad string"],
        }
    )
    input_data.to_excel(file, index=False)
    assert os.path.exists(file)

    crew_reqs = Crew_Requirements()
    crew_reqs.expected_columns = {"Timetable": object, "Turn": int, "Points": int}

    # When we import data then the correct exception is raised
    expected_error = re.escape("Unable to convert column Turn to type int64 (sheet: 0)")
    with pytest.raises(ValueError, match=expected_error):
        crew_reqs.import_data(file)


def test_import_validation_incorrect_dtype_date(tmp_path):
    # Given some input data with invalid date type
    dir = tmp_path / "input_data"
    dir.mkdir()
    file = dir / "incorrect_dtypes_date.xlsx"
    input_data = pd.DataFrame({"Date": ["Not a date"], "Timetable": ["Blue"]})
    input_data.to_excel(file, index=False)
    assert os.path.exists(file)

    crew_reqs = Crew_Requirements()
    crew_reqs.expected_columns = {"Date": object, "Timetable": object}

    # When we import data then the correct exception is raised
    expected_error = re.escape(
        "Unknown datetime string format, unable to "
        "parse: Not a date, at position 0 (sheet: 0)"
    )
    with pytest.raises(ValueError, match=expected_error):
        crew_reqs.import_data(file)


def test_import_validation_incorrect_columns(tmp_path):
    # Given some input data with the incorrect columns
    dir = tmp_path / "input_data"
    dir.mkdir()
    file = dir / "incorrect_columns.xlsx"
    input_data = pd.DataFrame(
        {"Timetable": ["Blue"], "Bad column": ["Bad string"], "Points": [5]}
    )
    input_data.to_excel(file, index=False)
    assert os.path.exists(file)

    crew_reqs = Crew_Requirements()
    crew_reqs.expected_columns = {"Timetable": object, "Turn": int, "Points": int}

    # When we import data then the correct exception is raised
    expected_error = f"The file {file} does not contain the correct columns. \n"
    f"The correct columns are {list(crew_reqs.expected_columns.keys())}"
    with pytest.raises(ValueError, match=expected_error):
        crew_reqs.import_data(file)

import pytest
import os
import pandas as pd
from pandas.testing import assert_frame_equal

from master_roster.create_master_availability import create_master_availability


def test_create_master_availability_valid(tmp_path):
    # Given some input data
    driver_dir = tmp_path / "driver data"
    driver_dir.mkdir()
    driver_1_file = driver_dir / "driver 1.xlsx"
    driver_1_data = pd.DataFrame(
        {
            "Date": [
                pd.to_datetime("21/01/2023", dayfirst=True),
                pd.to_datetime("22/01/2023", dayfirst=True),
            ],
            "Available": ["Y", None],
        }
    )
    driver_1_data.to_excel(driver_1_file, index=False)
    assert os.path.exists(driver_1_file)
    driver_2_file = driver_dir / "driver 2.csv"
    driver_2_data = pd.DataFrame(
        {
            "Date": [
                pd.to_datetime("20/01/2023", dayfirst=True),
                pd.to_datetime("22/01/2023", dayfirst=True),
            ],
            "Available": ["Y", None],
        }
    )
    driver_2_data.to_csv(driver_2_file, index=False)
    assert os.path.exists(driver_2_file)

    fireman_dir = tmp_path / "fireman data"
    fireman_dir.mkdir()
    fireman_1_file = fireman_dir / "fireman 1.xlsx"
    fireman_1_data = pd.DataFrame(
        {
            "Date": [
                pd.to_datetime("21/01/2023", dayfirst=True),
                pd.to_datetime("22/01/2023", dayfirst=True),
            ],
            "Available": ["N", "Y"],
        }
    )
    fireman_1_data.to_excel(fireman_1_file, index=False)
    assert os.path.exists(fireman_1_file)

    trainee_dir = tmp_path / "trainee data"
    trainee_dir.mkdir()

    # When we run the function
    actual = create_master_availability(
        driver_availability_folder=driver_dir,
        fireman_availability_folder=fireman_dir,
        trainee_availability_folder=trainee_dir,
    )

    # The correct output is given
    expected = pd.DataFrame(
        {
            "Date": [
                pd.to_datetime("20/01/2023", dayfirst=True),
                pd.to_datetime("21/01/2023", dayfirst=True),
                pd.to_datetime("22/01/2023", dayfirst=True),
            ],
            "Grade": ["Driver", "Driver", "Fireman"],
            "Name": ["driver 2", "driver 1", "fireman 1"],
            "Available": ["Y", "Y", "Y"],
        }
    )
    assert_frame_equal(actual.data_export, expected)


def test_create_master_availability_bad_availability(tmp_path):
    # Given some input data
    driver_dir = tmp_path / "driver data"
    driver_dir.mkdir()
    driver_1_file = driver_dir / "driver 1.xlsx"
    driver_1_data = pd.DataFrame(
        {
            "Date": [
                pd.to_datetime("21/01/2023", dayfirst=True),
                pd.to_datetime("22/01/2023", dayfirst=True),
            ],
            "Available": ["y", None],
        }
    )
    driver_1_data.to_excel(driver_1_file, index=False)
    assert os.path.exists(driver_1_file)

    fireman_dir = tmp_path / "fireman data"
    fireman_dir.mkdir()

    trainee_dir = tmp_path / "trainee data"
    trainee_dir.mkdir()

    # When we run the function
    expected_error = (
        f"The file {driver_1_file} contains invalid "
        "entries in the 'Available' column: {'y'}"
    )
    with pytest.raises(ValueError, match=expected_error):
        create_master_availability(
            driver_availability_folder=driver_dir,
            fireman_availability_folder=fireman_dir,
            trainee_availability_folder=trainee_dir,
        )


def test_create_master_availability_bad_date(tmp_path):
    # Given some input data
    driver_dir = tmp_path / "driver data"
    driver_dir.mkdir()
    driver_1_file = driver_dir / "driver 1.xlsx"
    driver_1_data = pd.DataFrame(
        {
            "Date": [
                "Random string",
                pd.to_datetime("22/01/2023", dayfirst=True),
            ],
            "Available": ["y", None],
        }
    )
    driver_1_data.to_excel(driver_1_file, index=False)
    assert os.path.exists(driver_1_file)

    fireman_dir = tmp_path / "fireman data"
    fireman_dir.mkdir()

    trainee_dir = tmp_path / "trainee data"
    trainee_dir.mkdir()

    # When we run the function
    expected_error = f"The data in {driver_1_file} is not of the correct type. \n"
    "Unknown datetime string format, unable to parse: Date, at position 0"
    with pytest.raises(ValueError, match=expected_error):
        create_master_availability(
            driver_availability_folder=driver_dir,
            fireman_availability_folder=fireman_dir,
            trainee_availability_folder=trainee_dir,
        )


def test_create_master_availability_extra_column(tmp_path):
    # Given some input data
    driver_dir = tmp_path / "driver data"
    driver_dir.mkdir()
    driver_1_file = driver_dir / "driver 1.xlsx"
    driver_1_data = pd.DataFrame(
        {
            "Date": [
                pd.to_datetime("21/01/2023", dayfirst=True),
                pd.to_datetime("22/01/2023", dayfirst=True),
            ],
            "Available": ["Y", None],
            None: ["bad entry", None],
        }
    )
    driver_1_data.to_excel(driver_1_file, index=False)
    assert os.path.exists(driver_1_file)

    fireman_dir = tmp_path / "fireman data"
    fireman_dir.mkdir()

    trainee_dir = tmp_path / "trainee data"
    trainee_dir.mkdir()

    # When we run the function
    expected_error = f"The file {driver_1_file} contains additional unexpected columns"
    with pytest.raises(ValueError, match=expected_error):
        create_master_availability(
            driver_availability_folder=driver_dir,
            fireman_availability_folder=fireman_dir,
            trainee_availability_folder=trainee_dir,
        )


def test_create_master_availability_extra_column_not_captured(tmp_path):
    # Given some input data
    driver_dir = tmp_path / "driver data"
    driver_dir.mkdir()
    driver_1_file = driver_dir / "driver 1.xlsx"
    driver_1_data = pd.DataFrame(
        {
            "Date": [
                pd.to_datetime("21/01/2023", dayfirst=True),
                pd.to_datetime("22/01/2023", dayfirst=True),
            ],
            "Available": ["Y", None],
            None: ["", None],
            "": [None, None],
        }
    )
    driver_1_data.to_excel(driver_1_file, index=False)
    assert os.path.exists(driver_1_file)

    fireman_dir = tmp_path / "fireman data"
    fireman_dir.mkdir()

    trainee_dir = tmp_path / "trainee data"
    trainee_dir.mkdir()

    # When we run the function
    actual = create_master_availability(
        driver_availability_folder=driver_dir,
        fireman_availability_folder=fireman_dir,
        trainee_availability_folder=trainee_dir,
    )

    # The correct output is given
    expected = pd.DataFrame(
        {
            "Date": [pd.to_datetime("21/01/2023", dayfirst=True)],
            "Grade": ["Driver"],
            "Name": ["driver 1"],
            "Available": ["Y"],
        }
    )
    assert_frame_equal(actual.data_export, expected)

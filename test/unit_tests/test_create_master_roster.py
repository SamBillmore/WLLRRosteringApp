import os
import pandas as pd
from pandas.testing import assert_frame_equal

from master_roster.create_master_availability import create_master_availability
from master_roster.create_master_roster import create_master_roster


def test_create_master_roster_valid(tmp_path):
    # Given some input data
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    working_roster_file = data_dir / "working roster.xlsx"
    working_roster_data = pd.DataFrame(
        {
            "Date": [
                "10/02/2018",
                "11/02/2018",
                "11/02/2018",
            ],
            "Timetable": [
                "Purple",
                "Yellow",
                "Yellow",
            ],
            "Turn": [1, 1, 2],
            "Points": [4, 3, 2],
            "Driver": [None, None, None],
            "Fireman": [None, None, None],
            "Trainee": [None, None, None],
        }
    )
    working_roster_data.to_excel(working_roster_file, index=False)
    assert os.path.exists(working_roster_file)

    driver_dir = data_dir / "driver data"
    driver_dir.mkdir()
    driver_1_file = driver_dir / "driver 1.xlsx"
    driver_1_data = pd.DataFrame(
        {
            "Date": [
                "10/02/2018",
                "11/02/2018",
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
                "10/02/2018",
                "11/02/2018",
            ],
            "Available": ["Y", "Y"],
        }
    )
    driver_2_data.to_csv(driver_2_file, index=False)
    assert os.path.exists(driver_2_file)

    fireman_dir = tmp_path / "fireman data"
    fireman_dir.mkdir()

    trainee_dir = tmp_path / "trainee data"
    trainee_dir.mkdir()

    master_availability = create_master_availability(
        driver_availability_folder=driver_dir,
        fireman_availability_folder=fireman_dir,
        trainee_availability_folder=trainee_dir,
    )

    output_file = data_dir / "output_data.xlsx"

    # When we run the function
    create_master_roster(
        working_roster_path=working_roster_file,
        master_availability=master_availability,
        master_roster_save_location=output_file,
    )

    # The the output is as expected
    assert os.path.exists(output_file)
    expected_data = pd.DataFrame(
        {
            "Date": [
                pd.to_datetime("10/02/2018", dayfirst=True),
                pd.to_datetime("11/02/2018", dayfirst=True),
                pd.to_datetime("11/02/2018", dayfirst=True),
            ],
            "Timetable": [
                "Purple",
                "Yellow",
                "Yellow",
            ],
            "Turn": [1, 1, 2],
            "Driver": [
                "driver 1",
                "driver 2",
                None,
            ],
            "Fireman": [
                None,
                None,
                None,
            ],
            "Trainee": [
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


def test_create_master_roster_valid_driver_as_fireman(tmp_path):
    # Given some input data
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    working_roster_file = data_dir / "working roster.xlsx"
    working_roster_data = pd.DataFrame(
        {
            "Date": [
                "10/02/2018",
                "11/02/2018",
                "11/02/2018",
            ],
            "Timetable": [
                "Purple",
                "Yellow",
                "Yellow",
            ],
            "Turn": [1, 1, 2],
            "Points": [4, 3, 2],
            "Driver": [None, None, None],
            "Fireman": [None, "driver 2", None],
            "Trainee": [None, None, None],
        }
    )
    working_roster_data.to_excel(working_roster_file, index=False)
    assert os.path.exists(working_roster_file)

    driver_dir = data_dir / "driver data"
    driver_dir.mkdir()
    driver_1_file = driver_dir / "driver 1.xlsx"
    driver_1_data = pd.DataFrame(
        {
            "Date": [
                "10/02/2018",
                "11/02/2018",
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
                "10/02/2018",
                "11/02/2018",
            ],
            "Available": ["Y", "Y"],
        }
    )
    driver_2_data.to_csv(driver_2_file, index=False)
    assert os.path.exists(driver_2_file)

    fireman_dir = tmp_path / "fireman data"
    fireman_dir.mkdir()

    trainee_dir = tmp_path / "trainee data"
    trainee_dir.mkdir()

    master_availability = create_master_availability(
        driver_availability_folder=driver_dir,
        fireman_availability_folder=fireman_dir,
        trainee_availability_folder=trainee_dir,
    )

    output_file = data_dir / "output_data.xlsx"

    # When we run the function
    create_master_roster(
        working_roster_path=working_roster_file,
        master_availability=master_availability,
        master_roster_save_location=output_file,
    )

    # The the output is as expected
    assert os.path.exists(output_file)
    expected_data = pd.DataFrame(
        {
            "Date": [
                pd.to_datetime("10/02/2018", dayfirst=True),
                pd.to_datetime("11/02/2018", dayfirst=True),
                pd.to_datetime("11/02/2018", dayfirst=True),
            ],
            "Timetable": [
                "Purple",
                "Yellow",
                "Yellow",
            ],
            "Turn": [1, 1, 2],
            "Driver": [
                "driver 1",
                None,
                None,
            ],
            "Fireman": [
                None,
                "driver 2",
                None,
            ],
            "Trainee": [
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

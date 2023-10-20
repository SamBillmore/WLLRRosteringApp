from unittest import mock
import os
import pandas as pd
from pandas.testing import assert_frame_equal

from master_roster.create_master_availability import MasterAvailability


@mock.patch("user_interface.master_availability_screen.filedialog.asksaveasfilename")
def test_correct(asksaveasfilename, app, tmp_path):
    # Given some initial data and state
    master_availability_screen = app.frames["MasterAvailabilityScreen"]
    master_availability_data = pd.DataFrame(
        {
            "Date": [pd.to_datetime("2018-01-05")],
            "Grade": ["Driver"],
            "Name": ["James Newby"],
            "Available": ["Y"],
        }
    )
    master_availability = MasterAvailability()
    master_availability.data_export = master_availability_data
    master_availability_screen.master_availability = master_availability

    dir = tmp_path / "data"
    dir.mkdir()
    output_file = dir / "output_data.xlsx"

    # When we run the function
    asksaveasfilename.return_value = output_file
    master_availability_screen.save_master_availability()

    # Then the file is created as expected
    assert os.path.exists(output_file)
    actual_data = pd.read_excel(output_file)
    expected_data = pd.DataFrame(
        {
            "Date": [pd.to_datetime("05/01/2018", dayfirst=True)],
            "Grade": ["Driver"],
            "Name": ["James Newby"],
            "Available": ["Y"],
        }
    )
    assert_frame_equal(actual_data, expected_data)

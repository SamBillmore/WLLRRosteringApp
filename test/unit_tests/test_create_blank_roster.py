import pytest
import pandas as pd
import os

from blank_roster.create_blank_roster import create_blank_roster


@pytest.mark.parametrize(
    "timetable_data,crew_reqs_data,expected_error",
    [
        (
            pd.DataFrame({"Date": ["21/01/2023"], "Timetable": ["Green"]}),
            pd.DataFrame(
                {
                    "Timetable": ["Green", "Blue", "Blue"],
                    "Turn": [1, 1, 2],
                    "Points": [5, 4, 3],
                }
            ),
            "There are entries in the crew requirements file that do not "
            "have a corresponding entry in the timetable file:",
        ),
        (
            pd.DataFrame(
                {"Date": ["21/01/2023", "22/02/2023"], "Timetable": ["Green", "Blue"]}
            ),
            pd.DataFrame(
                {"Timetable": ["Blue", "Blue"], "Turn": [1, 2], "Points": [4, 3]}
            ),
            "There are entries in the timetable file that do not have "
            "a corresponding entry in the crew requirements file:",
        ),
        (
            pd.DataFrame({"Date": ["21/01/2023"], "Timetable": ["Green"]}),
            pd.DataFrame(
                {"Timetable": ["Blue", "Blue"], "Turn": [1, 2], "Points": [4, 3]}
            ),
            "There are entries in the crew requirements file that do not "
            "have a corresponding entry in the timetable file:",
        ),
    ],
)
def test_merge_not_valid_mismatch(
    timetable_data, crew_reqs_data, expected_error, tmp_path
):
    # Given some input data that is mismatched
    dir = tmp_path / "data"
    dir.mkdir()
    input_timetable_file = dir / "timetable_data.xlsx"
    timetable_data.to_excel(input_timetable_file, index=False)
    assert os.path.exists(input_timetable_file)
    input_crew_reqs = dir / "crew_reqs.xlsx"
    crew_reqs_data.to_excel(input_crew_reqs, index=False)
    assert os.path.exists(input_crew_reqs)

    output_file = dir / "output_data.xlsx"

    # When we run the function then the error is raised correctly
    with pytest.raises(ValueError, match=expected_error):
        create_blank_roster(input_timetable_file, input_crew_reqs, output_file)

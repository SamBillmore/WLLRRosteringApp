import pandas as pd
from pandas.testing import assert_frame_equal

from individual_rosters.create_individual_rosters import IndividualRosters


def test_list_rostered_individuals():
    # Given some input data
    individual_rosters = IndividualRosters()
    individual_rosters.data_import = pd.DataFrame(
        {
            "Date": [
                pd.to_datetime("2018-01-05"),
                pd.to_datetime("2018-01-06"),
                pd.to_datetime("2018-01-06"),
                pd.to_datetime("2018-01-06"),
            ],
            "Timetable": ["Blue", "Yellow", "Yellow", "Yellow"],
            "Turn": [1, 1, 2, 3],
            "Driver": ["John Travis", "John Travis", "James Newby", None],
            "Fireman": ["Joe Gunby", None, "Megan Charman", "Kate Billmore"],
            "Trainee": ["Harry Billmore", "Stewart Charman", "Harry Billmore", None],
        }
    )

    # When we run the method
    individual_rosters.list_rostered_individuals()

    # Then the result is as expected
    actual = individual_rosters.rostered_individuals
    expected = {
        "John Travis",
        "James Newby",
        "Joe Gunby",
        "Megan Charman",
        "Kate Billmore",
        "Harry Billmore",
        "Stewart Charman",
    }
    assert actual == expected


def test_create_individual_roster_df():
    # Given some input data
    individual_rosters = IndividualRosters()
    individual_rosters.data_import = pd.DataFrame(
        {
            "Date": [
                pd.to_datetime("2018-01-05"),
                pd.to_datetime("2018-01-06"),
                pd.to_datetime("2018-01-06"),
                pd.to_datetime("2018-01-06"),
            ],
            "Timetable": ["Blue", "Yellow", "Yellow", "Yellow"],
            "Turn": [1, 1, 2, 3],
            "Driver": ["John Travis", "John Bancroft", "James Newby", None],
            "Fireman": ["Joe Gunby", None, "John Travis", "Kate Billmore"],
            "Trainee": ["Harry Billmore", "Stewart Charman", "Harry Billmore", None],
        }
    )

    individual = "John Travis"

    # When we run the method
    actual = individual_rosters.create_individual_roster_df(indiv=individual)

    # Then the result is as expected
    expected = pd.DataFrame(
        {
            "Date": ["Fri 05 01 2018", "Sat 06 01 2018"],
            "Timetable": ["Blue", "Yellow"],
            "Turn": [1, 2],
            "Driver": ["John Travis", "James Newby"],
            "Fireman": ["Joe Gunby", "John Travis"],
            "Trainee": ["Harry Billmore", "Harry Billmore"],
        },
        index=[0, 2],
    )
    assert_frame_equal(actual, expected)

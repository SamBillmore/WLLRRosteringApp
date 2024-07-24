import os
from tkinter import END


def test_real_file(app, tmp_path):
    # Given some input data and initial state
    input_file = "./tests/input_data/Final Roster.xlsx"
    assert os.path.exists(input_file)

    individual_rosters_screen = app.frames["IndividualRostersScreen"]

    output_dir = tmp_path / "output_data"
    output_dir.mkdir()

    # When we run the function
    individual_rosters_screen.run_create_individual_rosters(
        final_roster_path=input_file, individual_roster_save_folder=output_dir
    )

    # Then the files are created as expected
    assert len(os.listdir(output_dir)) == 10
    for file in os.listdir(output_dir):
        assert file.endswith(".pdf")


def test_errors_raised_correctly(app):
    # Given an initial state and inputs that will raise an error
    input_file = "bad_path.csv"
    output_dir = "output_data"
    individual_rosters_screen = app.frames["IndividualRostersScreen"]

    # When we run the function
    individual_rosters_screen.run_create_individual_rosters(
        final_roster_path=input_file, individual_roster_save_folder=output_dir
    )

    # Then the error is raised correctly
    assert app.visible_frame == "ErrorScreen"
    error_screen = app.frames["ErrorScreen"]
    assert (
        error_screen.error_message.get(1.0, END)
        == "[Errno 2] No such file or directory: 'bad_path.csv'\n"
    )

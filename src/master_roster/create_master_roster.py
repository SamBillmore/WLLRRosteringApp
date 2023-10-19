import pandas as pd
from copy import copy

from import_export.import_export_classes import DataImports
from import_export.import_export_classes import DataExports
from standard_labels.standard_labels import StandardLabels


def create_master_roster(
    working_roster_path,
    master_availability,
    master_roster_save_location,
):
    master_roster = Master_Roster(master_availability)
    master_roster.import_data(working_roster_path)
    master_roster.create_master_roster()
    master_roster.export_data(
        filepath=master_roster_save_location, sheet_name="master_roster"
    )


class Master_Roster(DataImports, DataExports):
    """Master roster."""

    def __init__(self, master_availability):
        """Initiates the class."""
        self.data_import = None
        self.master_availability = copy(master_availability.data_export)
        self.crew_members = master_availability.crew_members
        self.working_availability = None
        self.crew_members_points = None
        self.data_export = None
        self.expected_columns = {
            StandardLabels.date: object,
            StandardLabels.timetable: object,
            StandardLabels.turn: int,
            StandardLabels.points: int,
            StandardLabels.driver: object,
            StandardLabels.fireman: object,
            StandardLabels.trainee: object,
        }

    def create_master_roster(self):
        """Controlling function for creating master roster."""
        self.data_export = (
            self.data_import
        )  # Sets output to be the imported working roster
        self.set_up_points_tally()
        self.initial_points_allocation()
        for grade in StandardLabels.grades:
            self.allocate_crew_members_to_turns(grade=grade)
        self.data_export.pop(StandardLabels.points)

    def set_up_points_tally(self):
        """Creates the points tally attribute containing a list of crew and their points
        initially set to zero."""
        self.crew_members_points = pd.DataFrame(
            [[crew_member.name, 0] for crew_member in self.crew_members],
            columns=[StandardLabels.name, StandardLabels.points],
        )

    def initial_points_allocation(self):
        """Allocate points to individuals already allocated to turns.

        Remove that turn from master_availability.
        """
        for _, row in self.data_export.iterrows():
            for grade in StandardLabels.grades:
                if pd.notnull(row[grade]):
                    crew_member = row[grade]
                    points_to_add = row[StandardLabels.points]
                    self.add_points(crew_member, points_to_add)
                    date_to_remove = row[StandardLabels.date]
                    self.remove_person_from_availability(
                        crew_member, date_to_remove, self.master_availability
                    )

    def allocate_crew_members_to_turns(self, grade):
        """
        Allocates individuals to turns for a single turn type based on:
        - availability in self.master_availability
        - points recorded in self.crew_members_points
        """
        # Filter master_availability for turn type and save to working_availability
        self.working_availability = self.master_availability[
            self.master_availability[StandardLabels.grade] == grade
        ]
        # Loop through number of uncovered turns
        for _, row in self.data_export.iterrows():
            if pd.isnull(row[grade]):
                # Remove days from self.working_availability with all turns covered
                self.remove_rostered_days(grade)
                # Find day with lowest non-zero number of available people
                if self.working_availability[StandardLabels.date].any():
                    working_date = (
                        self.working_availability[StandardLabels.date]
                        .value_counts()
                        .tail(1)
                        .index[0]
                    )
                    # Find crew_member from that day with least number of points
                    person_for_turn = self.crew_member_lowest_points(working_date)
                    # Allocate person to turn, add points to crew_member.points and
                    # store in self.data_export, remove person from working_availability
                    self.allocate_person_to_turn(person_for_turn, working_date, grade)

    def remove_rostered_days(self, grade):
        """Removes rows from self.working_availability for dates that have all turns
        covered."""
        unallocated_turns = self.data_export.loc[self.data_export[grade].isnull()]
        df = self.working_availability
        self.working_availability = df[
            df[StandardLabels.date].isin(unallocated_turns[StandardLabels.date])
        ]

    def crew_member_lowest_points(self, working_date):
        """Finds crew member for specific date with lowest number of points."""
        left_df = self.working_availability[
            self.working_availability[StandardLabels.date] == working_date
        ]
        right_df = self.crew_members_points
        merged_df = pd.merge(
            left_df,
            right_df,
            left_on=StandardLabels.name,
            right_on=StandardLabels.name,
            how="left",
        )
        merged_df.sort_values(StandardLabels.points, ascending=True, inplace=True)
        return merged_df[StandardLabels.name].iloc[0]

    def allocate_person_to_turn(self, person_for_turn, working_date, grade):
        """
        Allocate person to turn by:
        - updating self.data_export by allocating person to highest scoring turn
        - adding points to self.crew_members_points
        - removing person from self.working_availability for working_date
        """
        # Update self.data_export
        working_day_blanks = self.data_export[
            (self.data_export[StandardLabels.date] == working_date)
            & (self.data_export[grade].isna())
        ]
        row_to_insert = working_day_blanks.sort_values(
            StandardLabels.points, ascending=False
        ).index[0]
        self.data_export.at[row_to_insert, grade] = person_for_turn
        # Remove person from self.working_availability for working_date
        self.remove_person_from_availability(
            person_for_turn, working_date, self.working_availability
        )
        # Add points to self.crew_members_points
        points_to_add = self.data_export[StandardLabels.points][row_to_insert]
        self.add_points(person_for_turn, points_to_add)

    def add_points(self, person, points_to_add):
        """Adds points for person to self.crew_member_points."""
        if person in self.crew_members_points[StandardLabels.name].values:
            row_index = self.crew_members_points.index[
                self.crew_members_points[StandardLabels.name] == person
            ][0]
            existing_points = self.crew_members_points[StandardLabels.points][row_index]
            self.crew_members_points.at[row_index, StandardLabels.points] = (
                points_to_add + existing_points
            )

    def remove_person_from_availability(self, person, date_to_remove, availability_df):
        """Removes person from availability for a specific day."""
        availability_df.drop(
            availability_df[
                (availability_df[StandardLabels.name] == person)
                & (availability_df[StandardLabels.date] == date_to_remove)
            ].index,
            inplace=True,
        )

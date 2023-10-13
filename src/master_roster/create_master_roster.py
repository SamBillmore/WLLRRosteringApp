import pandas as pd

from import_export.import_export_classes import DataImports
from import_export.import_export_classes import DataExports


def create_master_roster(
    working_roster_path,
    master_availability,
    master_roster_save_location,
):
    master_roster = Master_Roster()
    master_roster.import_data(working_roster_path)
    master_roster.create_master_roster(master_availability)
    master_roster.export_data(
        filepath=master_roster_save_location, sheet_name="master_roster"
    )


class Master_Roster(DataImports, DataExports):
    """Master roster."""

    def __init__(self):
        """Initiates the class."""
        self.data_import = None
        self.master_availability = None
        self.working_availability = None
        self.crew_members_points = None
        self.data_export = None
        self.expected_columns = {
            "Date": object,
            "Timetable": object,
            "Turn": int,
            "Points": int,
            "Driver": object,
            "Fireman": object,
            "Trainee": object,
        }

    def create_master_roster(self, master_availability):
        """Controlling function for creating master roster."""
        self.data_export = (
            self.data_import
        )  # Sets output to be the imported working roster
        self.master_availability = master_availability
        self.set_up_points_tally()
        for grade in set(self.master_availability.data_export["Grade"]):
            self.allocate_crew_members_to_turns(grade=grade)
        self.data_export.pop("Points")

    def set_up_points_tally(self):
        """Creates the zeroed points tally."""
        self.master_availability.crew_members.create_points_tally()
        self.crew_members_points = self.master_availability.crew_members.points_tally

    def allocate_crew_members_to_turns(self, grade):
        """
        Allocates individuals to turns for a single turn type based on:
        - availability in self.data_import
        - points recorded in self.crew_members_points
        """
        # Filter master_availability for turn type and save to working_availability
        self.working_availability = self.master_availability.data_export[
            self.master_availability.data_export["Grade"] == grade
        ]
        # Allocate points for turns already allocated in data_export
        self.initial_points_allocation(grade)
        # Loop through number of uncovered turns
        for _, row in self.data_export.iterrows():
            if pd.isnull(row[grade]):
                # Remove days from self.working_availability with all turns covered
                self.remove_rostered_days(grade)
                # Find day with lowest non-zero number of available people
                if self.working_availability["Date"].any():
                    working_date = (
                        self.working_availability["Date"]
                        .value_counts()
                        .tail(1)
                        .index[0]
                    )
                    # Find crew_member from that day with least number of points
                    person_for_turn = self.crew_member_lowest_points(working_date)
                    # Allocate person to turn, add points to crew_member.points and
                    # store in self.data_export, remove person from working_availability
                    self.allocate_person_to_turn(person_for_turn, working_date, grade)

    def initial_points_allocation(self, grade):
        """Allocate points to individuals already allocated to turns Remove that turn
        from working_availability."""
        for _, row in self.data_export.iterrows():
            if pd.notnull(row[grade]):
                crew_member = row[grade]
                points_to_add = row["Points"]
                self.add_points(crew_member, points_to_add)
                date_to_remove = row["Date"]
                self.remove_person_from_working_availability(
                    crew_member, date_to_remove
                )

    def remove_rostered_days(self, grade):
        """Removes rows from self.working_availability for dates that have all turns
        covered."""
        unallocated_turns = self.data_export.loc[self.data_export[grade].isnull()]
        df = self.working_availability
        self.working_availability = df[df["Date"].isin(unallocated_turns["Date"])]

    def crew_member_lowest_points(self, working_date):
        """Finds crew member for specific date with lowest number of points."""
        left_df = self.working_availability[
            self.working_availability["Date"] == working_date
        ]
        right_df = self.crew_members_points
        merged_df = pd.merge(
            left_df, right_df, left_on="Name", right_on="Name", how="left"
        )
        merged_df.sort_values("Points", ascending=True, inplace=True)
        return merged_df["Name"].iloc[0]

    def allocate_person_to_turn(self, person_for_turn, working_date, grade):
        """
        Allocate person to turn by:
        - updating self.data_export by allocating person to highest scoring turn
        - adding points to self.crew_members_points
        - removing person from self.working_availability for working_date
        """
        # Update self.data_export
        working_day_blanks = self.data_export[
            (self.data_export["Date"] == working_date)
            & (self.data_export[grade].isna())
        ]
        row_to_insert = working_day_blanks.sort_values("Points", ascending=False).index[
            0
        ]
        self.data_export.at[row_to_insert, grade] = person_for_turn
        # Remove person from self.working_availability for working_date
        self.remove_person_from_working_availability(person_for_turn, working_date)
        # Add points to self.crew_members_points
        points_to_add = self.data_export["Points"][row_to_insert]
        self.add_points(person_for_turn, points_to_add)

    def add_points(self, person, points_to_add):
        """Adds points for person to self.crew_member_points."""
        if person in self.crew_members_points["Name"].values:
            row_index = self.crew_members_points.index[
                self.crew_members_points["Name"] == person
            ][0]
            existing_points = self.crew_members_points["Points"][row_index]
            self.crew_members_points.at[row_index, "Points"] = (
                points_to_add + existing_points
            )

    def remove_person_from_working_availability(self, person, date_to_remove):
        """Removes person from working availability for a specific day."""
        df = self.working_availability
        self.working_availability = df[
            (df.Name != person) | (df.Date != date_to_remove)
        ]

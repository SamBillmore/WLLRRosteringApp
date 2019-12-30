import pandas as pd

from import_export.import_export_classes import Data_Imports
from import_export.import_export_classes import Data_Exports

from master_roster.create_master_availability import Crew_Members
from master_roster.create_master_availability import Master_Availability

class Master_Roster(Data_Imports,Data_Exports):
    """
    Master roster
    """

    def __init__(self):
        """
        Initiates the class
        """
        self.data_import = None
        self.master_availability = None
        self.working_availability = None
        self.crew_members = None
        self.data_export = None
        self.expected_columns = ['Date','Timetable','Turn','Points','Driver','Fireman','Trainee']

    def create_master_roster(self,availability_folders,master_avail_save_location,master_roster_save_location):
        """
        Controlling function for creating master roster
        """
        self.data_export = self.data_import
        self.create_master_availability(availability_folders,master_avail_save_location)
        for key in availability_folders.keys():
            self.allocate_crew_members_to_turns(key)
        self.data_export.pop('Points')
        self.export_data(filepath=master_roster_save_location,sheet_name='master_roster')

    def create_master_availability(self,availability_folders,save_location):
        """
        Create master availability and create the zeroed points tally
        """
        crew_members = Crew_Members()
        master_availability = Master_Availability()
        for key,value in  availability_folders.items():
            master_availability.create_master_availability(key,value,crew_members)
        master_availability.export_data(filepath=save_location,sheet_name='master_availability')
        crew_members.create_points_tally()
        self.master_availability = master_availability.data_export
        self.crew_members = crew_members

    def allocate_crew_members_to_turns(self,grade):
        """
        Allocates individuals to turns for a single turn type based on:
        - availability in self.data_import
        - points recorded in self.crew_members.points_tally
        """
        # Filter master_availability for turn type and save to working_availability
        self.working_availability = self.master_availability[self.master_availability['Grade']==grade]
        # Allocate points for turns already allocated in data_export
        self.initial_points_allocation(grade)
        # Loop through number of uncovered turns
        for _,row in self.data_export.iterrows():
            if pd.isnull(row[grade]):
                # Remove days from self.working_availability with all turns covered
                self.remove_rostered_days(grade)
                # Find day with lowest non-zero number of available people
                if self.working_availability['Date'].any():
                    working_date = self.working_availability['Date'].value_counts().tail(1).index[0]
                    # Find crew_member from that day with least number of points
                    person_for_turn = self.crew_member_lowest_points(working_date)
                    # Allocate person to turn, add points to crew_member.points and store in self.data_export, remove person from working_availability
                    self.allocate_person_to_turn(person_for_turn,working_date,grade)

    def initial_points_allocation(self,grade):
        """
        Allocate points to individuals already allocated to turns
        Remove that turn from working_availability
        """
        for _,row in self.data_export.iterrows():
            if pd.notnull(row[grade]):
                crew_member = row[grade]
                points_to_add = row['Points']
                row_index = self.crew_members.points_tally.index[self.crew_members.points_tally['Name']==crew_member][0]
                existing_points = self.crew_members.points_tally['Points'][row_index]
                self.crew_members.points_tally.at[row_index,'Points'] = points_to_add + existing_points
                date_to_remove = row['Date']
                df = self.working_availability
                self.working_availability = df[(df.Name != crew_member) | (df.Date != date_to_remove)]

    def remove_rostered_days(self,grade):
        """
        Removes rows from self.working_availability for dates that have all turns covered  
        """
        unallocated_turns = self.data_export.loc[self.data_export[grade].isnull()]
        df = self.working_availability
        self.working_availability = df[df['Date'].isin(unallocated_turns['Date'])]

    def crew_member_lowest_points(self,working_date):
        """
        Finds crew member for specific date with lowest number of points
        """
        left_df = self.working_availability[self.working_availability['Date']==working_date]
        right_df = self.crew_members.points_tally
        merged_df = pd.merge(left_df,right_df, left_on = 'Name', right_on = 'Name', how = 'left')
        merged_df.sort_values('Points',ascending=True,inplace=True)
        return merged_df['Name'][0]

    def allocate_person_to_turn(self,person_for_turn,working_date,grade):
        """
        Allocate person to turn by:
        - updating self.data_export by allocating person to highest scoring turn
        - adding points to self.crew_members.points_tally
        - removing person from self.working_availability for working_date
        """
        # Update self.data_export
        working_day = self.data_export[(self.data_export['Date']==working_date) & (self.data_export[grade].isna())]
        row_to_insert = working_day.sort_values('Points',ascending=False).index[0]
        self.data_export.at[row_to_insert,grade] = person_for_turn
        # Remove person from self.working_availability for working_date
        date_to_remove = working_date
        df = self.working_availability
        self.working_availability = df[(df.Name != person_for_turn) | (df.Date != date_to_remove)]
        # Add points to self.crew_members.points_tally
        points_to_add = self.data_export['Points'][row_to_insert]
        row_index = self.crew_members.points_tally.index[self.crew_members.points_tally['Name']==person_for_turn][0]
        existing_points = self.crew_members.points_tally['Points'][row_index]
        self.crew_members.points_tally.at[row_index,'Points'] = points_to_add + existing_points
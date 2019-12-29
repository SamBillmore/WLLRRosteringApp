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
        for key in  availability_folders.keys():
            self.allocate_crew_members_to_turns(key)
        self.export_data(filepath=master_roster_save_location,sheet_name='master_roster')

    def create_master_availability(self,availability_folders,save_location):
        """
        Creating master availability and zeroed points tally
        """
        crew_members = Crew_Members()
        master_availability = Master_Availability()
        for key,value in  availability_folders.items():
            master_availability.create_master_availability(key,value,crew_members)
        master_availability.export_data(filepath=save_location,sheet_name='master_availability')
        crew_members.create_points_tally()
        self.master_availability = master_availability.data_export
        self.crew_members = crew_members

    def allocate_crew_members_to_turns(self,turn_type):
        """
        Allocates individuals to turns for a single turn type based on:
        - availability in self.data_import
        - points recorded in self.crew_members.points_tally
        """
        # Filter master_availability for turn type and save to working_availability
        # Allocate points for turns already allocated in data_export
        # Loop:
            # Filter out crew members already allocated from working_availability
            # Find day(s) with lowest non-zero number of available people
            # Find day(s) with highest number of required people, then pick one at random
            # Find crew_member from that day with least number of points
            # Allocate person to turn, add points to crew_member.points and store in self.data_export



        # print(self.data_import)
        print(self.master_availability)
        print(self.crew_members.points_tally)
        print(self.data_export)
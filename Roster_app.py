from blank_availability.create_blank_availability import Timetable
from blank_availability.create_blank_availability import Crew_Requirements
from blank_availability.create_blank_availability import Availability_Form
from blank_roster.create_blank_roster import Blank_Roster
from master_roster.create_master_availability import Crew_Member
from master_roster.create_master_availability import Crew_Members
from master_roster.create_master_availability import Master_Availability
from master_roster.create_master_roster import Master_Roster

# Dummy inputs

timetable_path = './/Test input data//Timetable.xlsx'
crew_reqs_path = './/Test input data//Crew requirements.xlsx'

avail_save_location = './/Test output data//Test_Avail_Form.xlsx'
blank_roster_save_location = './/Test output data//Test_Blank_Roster.xlsx'

availability_folders = {
    'Driver':'.//Test input data//01 Driver availability',
    'Fireman':'.//Test input data//02 Fireman availability',
    'Trainee':'.//Test input data//03 Trainee availability'
}
working_roster_path = './/Test input data//Test_Working_Roster.xlsx'
master_roster_save_location = './/Test output data//Test_Master_roster.xlsx'
master_avail_save_location = './/Test output data//Test_Master_availability.xlsx'


def create_blank_availability(timetable_path, save_location):
    """
    Creating blank availability forms
    """
    timetable = Timetable()
    availability_form = Availability_Form()
    timetable.import_data(timetable_path)
    availability_form.get_timetable_dates(timetable)
    availability_form.create_availability_form(save_location)

def create_blank_roster(timetable_path, crew_reqs_path, save_location):
    """
    Creating blank roster
    """
    timetable = Timetable()
    crew_reqs = Crew_Requirements()
    blank_roster = Blank_Roster()
    timetable.import_data(timetable_path)
    crew_reqs.import_data(crew_reqs_path)
    blank_roster.create_blank_roster(timetable.data_import,crew_reqs.data_import,save_location)

def master_roster(working_roster_path,availability_folders,master_avail_save_location,master_roster_save_location):
    """
    Master function to control:
    - creating master availability
    - algorithm to allocate crews to turns
    """
    master_roster = Master_Roster()
    master_roster.import_data(working_roster_path)
    master_roster.create_master_roster(availability_folders,master_avail_save_location,master_roster_save_location)

# -------------------------------------------------------------------------------------------------------------
# Calls below

# To do
# Complete - 0. Refactor code into modules
# Complete - 1. Date formats for output sheets 
# Complete - 2. Autofit columns function for outputs
# Complete - 3. Create master function to call method for master availability
# To test - 4. Complete method 'allocate_turns()'
# 5. Create individual rosters and print to pdf
# 6. Create user interface

if __name__ =='__main__':
    # create_blank_availability(timetable_path,avail_save_location)
    # create_blank_roster(timetable_path,crew_reqs_path,blank_roster_save_location)
    master_roster(working_roster_path,availability_folders,master_avail_save_location,master_roster_save_location)
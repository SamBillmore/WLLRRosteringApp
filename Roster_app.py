from data_imports_and_templates import Timetable
from data_imports_and_templates import Crew_Requirements
from data_imports_and_templates import Availability_Form
from data_imports_and_templates import Blank_Roster
from data_imports_and_templates import Crew_Member
from data_imports_and_templates import Crew_Members
from data_imports_and_templates import Master_Availability
from data_imports_and_templates import Master_Roster

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
master_roster_save_location = './/Test output data//Test_Master_roster.xlsx'
master_availability_save_location = './/Test output data//Test_Master_availability.xlsx'


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

def create_master_availability(availability_folders, save_location):
    """
    Creating master availability
    """
    sheet_name = 'master_availability'
    crew_members = Crew_Members()
    master_availability = Master_Availability()
    for key,value in  availability_folders.items():
        master_availability.create_master_availability(key, value, crew_members)
    master_availability.export_data(filepath=save_location,sheet_name=sheet_name)
    print(crew_members.data)
    print(master_availability.data_export)

# -------------------------------------------------------------------------------------------------------------
# Calls below

# To do
# 1. Date formats for output sheets
# 2. Autofit columns function for outputs
# 3. Continue with allocating availability to turns

# create_blank_availability(timetable_path,avail_save_location)

# create_blank_roster(timetable_path,crew_reqs_path,blank_roster_save_location)

create_master_availability(availability_folders,master_availability_save_location)


import os

from data_imports_and_templates import Timetable
from data_imports_and_templates import Crew_Requirements
from data_imports_and_templates import Availability_Form
from data_imports_and_templates import Blank_Roster
from data_imports_and_templates import Crew_Member
from data_imports_and_templates import Master_Availability

# Dummy inputs

timetable_path = 'C://Users//sambi//OneDrive//Documents//WLLR//Rostering program//Test data//Timetable.csv'
crew_reqs_path = 'C://Users//sambi//OneDrive//Documents//WLLR//Rostering program//Test data//Crew requirements.csv'

avail_save_location = 'C://Users//sambi//OneDrive//Documents//WLLR//Rostering program//Test data//Test_Avail_Form.xlsx'
blank_roster_save_location = 'C://Users//sambi//OneDrive//Documents//WLLR//Rostering program//Test data//Test_Blank_Roster.xlsx'

grade = 'driver'
availability_folder = 'C://Users//sambi//OneDrive//Documents//WLLR//Rostering program//Test data//01 Driver availability'
master_roster_save_location = 'C://Users//sambi//OneDrive//Documents//WLLR//Rostering program//Test data//Test_Master_roster.xlsx'


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

def import_availability(grade, availability_folder):
    """
    Importing availability from completed availability forms
    """
    crew_members = []
    master_availability = Master_Availability()
    for file_name in os.listdir(availability_folder):
        crew_member = Crew_Member()
        crew_member.name = file_name.split('.')[0]
        crew_member.grade = grade
        file_path = os.path.join(availability_folder + "/" + file_name)
        crew_member.import_data(file_path)
        master_availability.append_availability(crew_member)
        crew_members.append(crew_member)
    return crew_members, master_availability


create_blank_availability(timetable_path,avail_save_location)
create_blank_roster(timetable_path,crew_reqs_path,blank_roster_save_location)
crew_members, master_availability = import_availability(grade, availability_folder)

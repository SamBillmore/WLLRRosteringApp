from data_imports_and_templates import Timetable
from data_imports_and_templates import Availability_Form
from data_imports_and_templates import Crew_Requirements
from data_imports_and_templates import Blank_Roster

timetable_path = 'C://Users//sambi//OneDrive//Documents//WLLR//Rostering program//Test data//Timetable.csv'
crew_reqs_path = 'C://Users//sambi//OneDrive//Documents//WLLR//Rostering program//Test data//Crew requirements.csv'

avail_save_location = 'C://Users//sambi//OneDrive//Documents//WLLR//Rostering program//Test data//Test_Avail_Form.xlsx'
blank_timetable_save_location = 'C://Users//sambi//OneDrive//Documents//WLLR//Rostering program//Test data//Test_Blank_Timetable.xlsx'

# Creating blank availability forms

def blank_availability(timetable_path, save_location):
    timetable = Timetable()
    availability_form = Availability_Form()
    if timetable.import_data(timetable_path):
        availability_form.get_timetable_dates(timetable)
        availability_form.create_availability_form(save_location)
    else:
        print('help')

blank_availability(timetable_path,avail_save_location)

# Creating blank roster

def blank_roster(timetable_path, crew_reqs_path, save_location):
    timetable = Timetable()
    crew_reqs = Crew_Requirements()
    blank_roster = Blank_Roster()
    if timetable.import_data(timetable_path) and crew_reqs.import_data(crew_reqs_path):
        blank_roster.create_blank_roster(timetable.data,crew_reqs.data,blank_timetable_save_location)
    else:
        print('help')


blank_roster(timetable_path,crew_reqs_path,blank_timetable_save_location)
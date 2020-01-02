from user_interface.tkinter_user_interface import App


# -------------------------------------------------------------------------------------------------------------


from blank_availability.create_blank_availability import Timetable
from blank_availability.create_blank_availability import Availability_Form
from blank_roster.create_blank_roster import Crew_Requirements
from blank_roster.create_blank_roster import Blank_Roster
from master_roster.create_master_roster import Master_Roster
from individual_rosters.create_individual_rosters import Individual_Rosters


# -------------------------------------------------------------------------------------------------------------

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
master_roster_save_location = './/Test output data//Test_Master_Roster.xlsx'
master_avail_save_location = './/Test output data//Test_Master_Availability.xlsx'

final_roster_path = './/Test input data//Test_Final_Roster.xlsx'
individual_roster_save_folder = './/Test output data//Individual Rosters'


# -------------------------------------------------------------------------------------------------------------

def create_blank_availability(timetable_path,save_location):
    """
    Creating blank availability forms
    """
    timetable = Timetable()
    availability_form = Availability_Form()
    file_import_test = timetable.import_data(timetable_path)
    if file_import_test:
        availability_form.get_timetable_dates(timetable)
        availability_form.create_availability_form(save_location)
    else:
        print(timetable_path)
        print(timetable.expected_columns)

def create_blank_roster(timetable_path,crew_reqs_path,save_location):
    """
    Creating blank roster
    """
    timetable = Timetable()
    crew_reqs = Crew_Requirements()
    blank_roster = Blank_Roster()
    timetable_import_test = timetable.import_data(timetable_path)
    if timetable_import_test:
        crew_reqs_import_test = crew_reqs.import_data(crew_reqs_path)
        if crew_reqs_import_test:
            blank_roster.create_blank_roster(timetable.data_import,crew_reqs.data_import,save_location)
        else:
            print(crew_reqs_path)
            print(crew_reqs.expected_columns)
    else:
        print(timetable_path)
        print(timetable.expected_columns)

def master_roster(working_roster_path,availability_folders,master_avail_save_location,master_roster_save_location):
    """
    Master function to control:
    - creating master availability
    - create master roster by allocating availability to turns
    """
    master_roster = Master_Roster()
    working_roster_import_test = master_roster.import_data(working_roster_path)
    if working_roster_import_test:
        availability_import_test,file_name,expected_columns = master_roster.create_master_roster(availability_folders,master_avail_save_location,master_roster_save_location)
        if availability_import_test == False:
            print(file_name)
            print(expected_columns)
    else:
        print(working_roster_path)
        print(master_roster.expected_columns)

def individual_rosters(final_roster_path,individual_roster_save_folder):
    """
    Create individual rosters from the final roster
    """
    individual_rosters = Individual_Rosters()
    file_import_test = individual_rosters.import_data(final_roster_path)
    if file_import_test:
        individual_rosters.create_individual_rosters(individual_roster_save_folder)
    else:
        print(final_roster_path)
        print(individual_rosters.expected_columns)

def main():
    """
    Main function for app
    """
    app = App()
    app.mainloop()

# -------------------------------------------------------------------------------------------------------------

# To do
# Complete - 0. Refactor code into modules
# Complete - 1. Date formats for output sheets 
# Complete - 2. Autofit columns function for outputs
# Complete - 3. Create master function to call method for master availability
# To test - 4. Complete method 'allocate_turns()'
# Complete - Check whether code needs refactoring
# Complete - Refactor removing person from working_availability and adding point to points_tally
# Complete - 5. Create individual rosters and print to pdf
# Complete - Move print to pdf to import_export
# Complete - Check Crew requirements - should be in blank roster?
# Complete - 6. Error checking for imports
# 7. Create user interface

if __name__ =='__main__':
    # create_blank_availability(timetable_path,avail_save_location)
    # create_blank_roster(timetable_path,crew_reqs_path,blank_roster_save_location)
    # master_roster(working_roster_path,availability_folders,master_avail_save_location,master_roster_save_location)
    # individual_rosters(final_roster_path,individual_roster_save_folder)
    main()
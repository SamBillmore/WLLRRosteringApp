from blank_availability_forms import Timetable, Availability_Form

timetable_path = 'C://Users//sambi//OneDrive//Documents//WLLR//Rostering program//Test data//Timetable.csv'
save_location = 'C://Users//sambi//OneDrive//Documents//WLLR//Rostering program//Test data//Test_Avail_Form.xlsx'

test_timetable = Timetable()
if test_timetable.import_data(timetable_path):
    availability_form = Availability_Form()
    availability_form.get_timetable_dates(test_timetable)
    availability_form.create_availability_form(save_location)
else:
    print('help')
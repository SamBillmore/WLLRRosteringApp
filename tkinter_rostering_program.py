import numpy as np
import pandas as pd
import os
from tkinter import *
from tkinter import filedialog
from functools import partial
import xlsxwriter

# Setup parameters
root = Tk()
program_title = 'WLLR footplate crew rostering program v0.3'
width = '850'
height = '600'
screen_pos_right = '250'
screen_pos_down = '100'
background_col = 'black'
foreground_col = 'white'
font = 'courier 11'

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def browse_file(entry):
    """
    Browse the file system and confirm the file selected is a .csv files
    """
    file_path = filedialog.askopenfilename(title='Choose a file')
    if file_path != None and file_path[-4:] == '.csv':
        entry.delete(0, END)
        entry.insert(0, file_path)

def browse_directory(entry):
    """
    Browse the file system and select a directory
    """
    dir_path = filedialog.askdirectory(title='Choose a folder location')
    if dir_path != None:
        entry.delete(0, END)
        entry.insert(0, dir_path)

def check_import_cols(imported_df,expected_cols):
    """
    Checks if the columns of a dataframe match the expected columns
    """
    output = 'Passed'
    actual_columns = [col for col in imported_df.columns]
    if actual_columns != expected_cols:
        output = 'Column headings are not as expected'
    return output

def check_person_df(imported_df):
    """
    Checks if the columns of a dataframe match the expected columns
    """
    col_err_msg = 'Column headings are not as expected'
    avail_col_err_msg = 'Availablity responses - should be \'Y\' for a positive response'
    output = 'Passed'

    expected_cols = ['Name','Date','Available']
    actual_columns = [col for col in imported_df.columns]
    if actual_columns != expected_cols:
        output = col_err_msg
    if 'Y' not in set(imported_df['Available']):
        output = avail_col_err_msg
    return output

def root_setup_error(frame_to_delete,error_check,file_path):
    """
    Layout for the error screen of the program
    """
    frame_to_delete.grid_forget()

    frame_error = Frame(root, bg=background_col, width=width, height=height)

    error_file = file_path.split('/')
    print(error_file)

    page_header_label = Label(frame_error, text='Oops. Something\'s gone wrong', bg=background_col, fg=foreground_col, font=font)
    page_header_label_2 = Label(frame_error, text='Here\'s some information on the problem:', bg=background_col, fg=foreground_col, font=font)
    error_header = Label(frame_error, text='\tError type:', bg=background_col, fg=foreground_col, font=font)
    error_message_label = Label(frame_error, text=error_check, bg=background_col, fg=foreground_col, font=font)
    file_header = Label(frame_error, text='\tFile:', bg=background_col, fg=foreground_col, font=font)
    file_label = Label(frame_error, text=error_file[-1], bg=background_col, fg=foreground_col, font=font)
    folder_header = Label(frame_error, text='\tFolder location:', bg=background_col, fg=foreground_col, font=font)
    folder_label = Label(frame_error, text=error_file[-2], bg=background_col, fg=foreground_col, font=font)
    back_button_err = Button (frame_error, text='Try again', width=19, command=partial(root_setup_0, frame_error))

    frame_error.grid(row=0, column=0, sticky=W)

    page_header_label.grid(row=0, column=0, sticky=W, padx=25, pady=20, columnspan=3)
    page_header_label_2.grid(row=1, column=0, sticky=W, padx=25, pady=20, columnspan=3)
    error_header.grid(row=2, column=0, sticky=W, padx=25, pady=20, columnspan=1)
    error_message_label.grid(row=2, column=1, sticky=W, padx=25, pady=20, columnspan=1)
    file_header.grid(row=3, column=0, sticky=W, padx=25, pady=20, columnspan=1)
    file_label.grid(row=3, column=1, sticky=W, padx=25, pady=20, columnspan=1)
    folder_header.grid(row=4, column=0, sticky=W, padx=25, pady=20, columnspan=1)
    folder_label.grid(row=4, column=1, sticky=W, padx=25, pady=20, columnspan=1)
    back_button_err.grid(row=5, column=0, sticky=W, padx=25, pady = 20,columnspan=1)


def create_individual_rosters(roster_location, save_location, frame_to_delete):
    """
    Create individual roster requirements table for each individual
    Saves (by default as a .csv) in the user specified save_location
    """
    final_roster_expected_cols = ['Date','Timetable','Turn','Driver','Fireman','Trainee']
    roster_path = roster_location.get()
    save_path = save_location.get()
    final_roster_df = pd.read_csv(roster_path, dtype = {'Driver':str, 'Fireman':str, 'Trainee':str})
    error_check = check_import_cols(final_roster_df,final_roster_expected_cols)
    if error_check == 'Passed':
        filling_na = ' '
        final_roster_df.fillna(filling_na,inplace=True)

        rostered_indivs = final_roster_df['Driver'].append(final_roster_df['Fireman'].append(final_roster_df['Trainee'])).unique()

        for indiv in rostered_indivs:
            if indiv != filling_na:
                driver_filter = final_roster_df['Driver'] == indiv
                fireman_filter = final_roster_df['Fireman'] == indiv
                trainee_filter = final_roster_df['Trainee'] == indiv
                indiv_roster_df = final_roster_df[driver_filter | fireman_filter | trainee_filter]
                indiv_save_path = os.path.join(save_path,r'Individual roster_'+indiv+'.csv')
                indiv_roster_df.to_csv(indiv_save_path,index=False)

        root_setup_0(frame_to_delete)
    else:
        root_setup_error(frame_to_delete,error_check,working_roster_path)

def root_setup_3(frame_to_delete):
    """
    Layout for the third screen of the program - create individual rosters
    """
    frame_to_delete.grid_forget()

    frame_3 = Frame(root, bg=background_col, width=width, height=height)

    indiv_roster_label_1 = Label (frame_3, text='Finalised roster: ', bg=background_col, fg=foreground_col, font=font)
    indiv_roster_entry_1 = Entry(frame_3, width=50)
    indiv_roster_button_1 = Button (frame_3, text='Browse', width=6, command=partial(browse_file, indiv_roster_entry_1))
    indiv_roster_label_2 = Label (frame_3, text='Save location: ', bg=background_col, fg=foreground_col, font=font)
    indiv_roster_entry_2 = Entry(frame_3, width=50)
    indiv_roster_button_2 = Button (frame_3, text='Browse', width=6, command=partial(browse_directory, indiv_roster_entry_2))
    function_plus_args = partial(create_individual_rosters, indiv_roster_entry_1, indiv_roster_entry_2, frame_3)
    create_indiv_roster_button = Button (frame_3, text='Create individual rosters', width=25, command=function_plus_args)
    back_button_3 = Button (frame_3, text='Back', width=19, command=partial(root_setup_0, frame_3))

    frame_3.grid(row=0, column=0, sticky=W)

    indiv_roster_label_1.grid(row=0, column=0, sticky=W, padx=25, pady=20)
    indiv_roster_entry_1.grid(row=0, column=1, sticky=W, padx=0, pady=0)
    indiv_roster_button_1.grid(row=0, column=2, sticky=E, padx=0, pady=0)
    indiv_roster_label_2.grid(row=1, column=0, sticky=W, padx=25, pady=20)
    indiv_roster_entry_2.grid(row=1, column=1, sticky=W, padx=0, pady=0)
    indiv_roster_button_2.grid(row=1, column=2, sticky=E, padx=0, pady=0)
    create_indiv_roster_button.grid(row=2, column=1, sticky=E, padx=0, pady=15)
    back_button_3.grid(row=3, column=0, sticky=W, padx=25, pady = 20)

def combine_availability(dir_path,frame_to_delete):
    """
    Unions together all availability forms into a single dataframe
    Only contains data for dates which are available
    """
    combined_df = pd.DataFrame()
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path + "/" + filename)
        person_df = pd.read_excel(file_path, dayfirst=True, parse_dates=[0], dtype={'Available':str})
        name = filename.split('.')[0]
        person_df.insert(0,'Name',[name for i in range(len(person_df))])
        error_check = check_person_df(person_df)
        if error_check == 'Passed':
            combined_df = pd.concat([combined_df,person_df])
            combined_df = combined_df[combined_df['Available'] == 'Y']
        else:
            root_setup_error(frame_to_delete,error_check,file_path)
            return pd.DataFrame()
    else:
        return combined_df

def remove_rostered_days(available_df,working_roster_df,turn_type):
    """
    Removes rows from available_df for dates that have all turns covered  
    """
    unallocated_turns = working_roster_df.loc[working_roster_df[turn_type].isnull()]
    available_df = available_df[available_df['Date'].isin(unallocated_turns['Date'])]
    return available_df

def remove_rostered_turns(available_df,working_roster_df,turn_type):
    """
    Selects rows from working_roster_df that have already been allocated
    Removes those rows from available_df
    """
    allocated_turns = working_roster_df.loc[working_roster_df[turn_type].notnull()]
    for index, row in allocated_turns.iterrows():
        date_to_remove = row['Date']
        person_to_remove = row[turn_type]
        available_df = available_df[(available_df.Name != person_to_remove) | (available_df.Date != date_to_remove)]
    return available_df

def calculate_score(working_roster_df, working_date_df):
    """
    Adds existing Points score to working_date_df
    """
    for index, row in working_date_df.iterrows():
        person_to_score = row['Name']
        driver_score = 0
        fireman_score = 0
        trainee_score = 0
        if pd.isna(working_roster_df.Driver).all() != True:
            driver_score = working_roster_df.loc[working_roster_df.Driver == person_to_score, 'Points'].sum()
        if pd.isna(working_roster_df.Fireman).all() != True:
            fireman_score = working_roster_df.loc[working_roster_df.Fireman == person_to_score, 'Points'].sum()
        if pd.isna(working_roster_df.Trainee).all() != True:
            trainee_score = working_roster_df.loc[working_roster_df.Trainee == person_to_score, 'Points'].sum()
        total_score = driver_score + fireman_score + trainee_score
        working_date_df.loc[index,'Score'] = total_score
        working_date_df = working_date_df.sort_values(by=['Score']).reset_index(drop=True)
    return working_date_df

def insert_crew(working_roster_df, working_date_df, turn_type, working_date):
    """
    Inserts people into turns on the working_roster_df
    """
    turn_to_insert_df = working_roster_df.loc[working_roster_df[turn_type].isnull()]
    turn_to_insert_df = turn_to_insert_df[(turn_to_insert_df.Date == working_date)]
    turn_to_insert_df = turn_to_insert_df.sort_values(by=['Points'],ascending=False)

    row_to_insert = turn_to_insert_df.iloc[0].name
    person_to_insert = working_date_df.loc[0,'Name']
    working_roster_df.at[row_to_insert,turn_type] = person_to_insert
    return working_roster_df

def availability_manager(locations, blank_roster_entry, frame_to_delete):
    """
    Loops through the driver, fireman and trainee locations, initiates collection of availability 
    and allocates people to turns
    """
    working_roster_expected_cols = ['Date','Timetable','Turn','Points','Driver','Fireman','Trainee']
    working_roster_path = blank_roster_entry.get()
    working_roster_df = pd.read_csv(working_roster_path, dayfirst=True, parse_dates=[0],
        dtype = {'Driver':str, 'Fireman':str, 'Trainee':str})
    error_check = check_import_cols(working_roster_df,working_roster_expected_cols)
    if error_check == 'Passed':
        for i in locations:
            if i == locations[0]:
                turn_type = 'Driver'
            elif i == locations[1]:
                turn_type = 'Fireman'
            else:
                turn_type = 'Trainee'
            dir_path = i.get()
            available_df = combine_availability(dir_path,frame_to_delete)
            if available_df.empty == True:
                break
            turns_to_cover_df = working_roster_df.loc[working_roster_df[turn_type].isnull()]
            number_of_iterations = len(turns_to_cover_df.index)

            for j in range(number_of_iterations):
                available_df = remove_rostered_days(available_df,working_roster_df,turn_type)
                available_df = remove_rostered_turns(available_df,working_roster_df,turn_type)
                print(available_df)
                count_crew_avail_df = available_df['Date'].value_counts().sort_values(ascending=True)
                if len(count_crew_avail_df) > 0:
                    working_date = count_crew_avail_df.index[0]
                    working_date_df = available_df[(available_df.Date == working_date)].reset_index(drop=True)
                    working_date_df = calculate_score(working_roster_df, working_date_df)
                    working_roster_df = insert_crew(working_roster_df, working_date_df, turn_type, working_date)
        else:
            working_roster_df.pop('Points')
            save_location = filedialog.asksaveasfilename(title='Choose a save location',defaultextension='.csv')
            working_roster_df.to_csv(save_location, index=False)
            root_setup_0(frame_to_delete)
    else:
        root_setup_error(frame_to_delete,error_check,working_roster_path)

def summary_availability(locations, frame_to_delete):
    """
    Loops through the driver, fireman and trainee locations, initiates collection of availability 
    and creates a summary of availability by day
    """
    dir_save_path = filedialog.askdirectory(title='Choose a folder location')
    for i in locations:
        if i == locations[0]:
            turn_type = 'Driver'
        elif i == locations[1]:
            turn_type = 'Fireman'
        else:
            turn_type = 'Trainee'
        dir_path = i.get()
        available_df = combine_availability(dir_path,frame_to_delete)
        if available_df.empty == True:
            break  
        else:
            save_location = dir_save_path + '/' + turn_type + '_availability.csv'
            available_df.to_csv(save_location, index=False)
    root_setup_0(frame_to_delete)

def root_setup_2a(frame_to_delete):
    """
    Layout for the second screen of the program - allocation of crews
    """
    frame_to_delete.grid_forget()

    frame_2a = Frame(root, bg=background_col, width=width, height=height)

    text_for_label = '''Please use the buttons below to import the availability data received from crews.'''
    instruction_label = Label(frame_2a, text=text_for_label, bg=background_col, fg=foreground_col, font=font)

    driver = StringVar()
    fireman = StringVar()
    trainee = StringVar()

    driver_avail_label = Label (frame_2a, text='Driver availability folder: ', bg=background_col, fg=foreground_col, font=font)
    driver_avail_entry = Entry(frame_2a, textvariable=driver, width=50)
    driver_avail_button = Button (frame_2a, text='Browse', width=6, command=partial(browse_directory, driver_avail_entry))
    fireman_avail_label = Label (frame_2a, text='Fireman availability folder: ', bg=background_col, fg=foreground_col, font=font)
    fireman_avail_entry = Entry(frame_2a, textvariable=fireman, width=50)
    fireman_avail_button = Button (frame_2a, text='Browse', width=6, command=partial(browse_directory, fireman_avail_entry))
    trainee_avail_label = Label (frame_2a, text='Trainee availability folder: ', bg=background_col, fg=foreground_col, font=font)
    trainee_avail_entry = Entry(frame_2a, textvariable=trainee, width=50)
    trainee_avail_button = Button (frame_2a, text='Browse', width=6, command=partial(browse_directory, trainee_avail_entry))
    back_button_2 = Button (frame_2a, text='Back', width=19, command=partial(root_setup_0, frame_2a))
    
    locations = [driver_avail_entry, fireman_avail_entry, trainee_avail_entry]
    function_plus_args = partial(summary_availability, locations, frame_2a)
    summary_avail_button = Button (frame_2a, text='Create availability summary', width=24, command=function_plus_args)

    frame_2a.grid(row=0, column=0, sticky=W)

    instruction_label.grid(row=0, column=0, sticky=W, padx=25, pady=20, columnspan=2)
    driver_avail_label.grid(row=1, column=0, sticky=W, padx=25, pady=0)
    driver_avail_entry.grid(row=1, column=1, sticky=E, padx=0, pady=0)
    driver_avail_button.grid(row=1, column=2, sticky=W, padx=0, pady=0)
    fireman_avail_label.grid(row=2, column=0, sticky=W, padx=25, pady=0)
    fireman_avail_entry.grid(row=2, column=1, sticky=E, padx=0, pady=0)
    fireman_avail_button.grid(row=2, column=2, sticky=W, padx=0, pady=0)
    trainee_avail_label.grid(row=3, column=0, sticky=W, padx=25, pady=0)
    trainee_avail_entry.grid(row=3, column=1, sticky=E, padx=0, pady=0)
    trainee_avail_button.grid(row=3, column=2, sticky=W, padx=0, pady=0)
    summary_avail_button.grid(row=5, column=1, sticky=E, padx=0, pady=15)
    back_button_2.grid(row=6, column=0, sticky=W, padx=25, pady = 20)

def root_setup_2(frame_to_delete):
    """
    Layout for the second screen of the program - allocation of crews
    """
    frame_to_delete.grid_forget()

    frame_2 = Frame(root, bg=background_col, width=width, height=height)

    text_for_label = '''Please use the buttons below to import the availability data received from crews.'''
    instruction_label = Label(frame_2, text=text_for_label, bg=background_col, fg=foreground_col, font=font)

    driver = StringVar()
    fireman = StringVar()
    trainee = StringVar()

    driver_avail_label = Label (frame_2, text='Driver availability folder: ', bg=background_col, fg=foreground_col, font=font)
    driver_avail_entry = Entry(frame_2, textvariable=driver, width=50)
    driver_avail_button = Button (frame_2, text='Browse', width=6, command=partial(browse_directory, driver_avail_entry))
    fireman_avail_label = Label (frame_2, text='Fireman availability folder: ', bg=background_col, fg=foreground_col, font=font)
    fireman_avail_entry = Entry(frame_2, textvariable=fireman, width=50)
    fireman_avail_button = Button (frame_2, text='Browse', width=6, command=partial(browse_directory, fireman_avail_entry))
    trainee_avail_label = Label (frame_2, text='Trainee availability folder: ', bg=background_col, fg=foreground_col, font=font)
    trainee_avail_entry = Entry(frame_2, textvariable=trainee, width=50)
    trainee_avail_button = Button (frame_2, text='Browse', width=6, command=partial(browse_directory, trainee_avail_entry))
    blank_roster_label = Label (frame_2, text='Working roster location: ', bg=background_col, fg=foreground_col, font=font)
    blank_roster_entry = Entry(frame_2, width=50)
    blank_roster_button = Button (frame_2, text='Browse', width=6, command=partial(browse_file, blank_roster_entry))
    back_button_2 = Button (frame_2, text='Back', width=19, command=partial(root_setup_0, frame_2))
    
    locations = [driver_avail_entry, fireman_avail_entry, trainee_avail_entry]
    function_plus_args = partial(availability_manager, locations, blank_roster_entry, frame_2)
    create_timetable_button = Button (frame_2, text='Allocate crews to roster', width=24, command=function_plus_args)

    frame_2.grid(row=0, column=0, sticky=W)

    instruction_label.grid(row=0, column=0, sticky=W, padx=25, pady=20, columnspan=2)
    driver_avail_label.grid(row=1, column=0, sticky=W, padx=25, pady=0)
    driver_avail_entry.grid(row=1, column=1, sticky=E, padx=0, pady=0)
    driver_avail_button.grid(row=1, column=2, sticky=W, padx=0, pady=0)
    fireman_avail_label.grid(row=2, column=0, sticky=W, padx=25, pady=0)
    fireman_avail_entry.grid(row=2, column=1, sticky=E, padx=0, pady=0)
    fireman_avail_button.grid(row=2, column=2, sticky=W, padx=0, pady=0)
    trainee_avail_label.grid(row=3, column=0, sticky=W, padx=25, pady=0)
    trainee_avail_entry.grid(row=3, column=1, sticky=E, padx=0, pady=0)
    trainee_avail_button.grid(row=3, column=2, sticky=W, padx=0, pady=0)
    blank_roster_label.grid(row=4, column=0, sticky=W, padx=25, pady=20)
    blank_roster_entry.grid(row=4, column=1, sticky=E, padx=0, pady=0)
    blank_roster_button.grid(row=4, column=2, sticky=W, padx=0, pady=0)
    create_timetable_button.grid(row=5, column=1, sticky=E, padx=0, pady=15)
    back_button_2.grid(row=6, column=0, sticky=W, padx=25, pady = 20)

def create_blank_roster(timetable_entry, crew_reqs_entry, frame_to_delete):
    """
    Create intial roster requirements table
    Saves (by default as a .csv) in the user specified location
    """
    timetable_expected_cols = ['Date','Timetable']
    crew_reqs_expected_cols = ['Timetable','Turn','Points']
    timetable_path = timetable_entry.get()
    crew_reqs_path = crew_reqs_entry.get()
    master_df = pd.read_csv(timetable_path)
    error_check_master = check_import_cols(master_df,timetable_expected_cols)
    if error_check_master == 'Passed':
        crew_reqs_df = pd.read_csv(crew_reqs_path)
        error_check_crew_reqs = check_import_cols(crew_reqs_df,crew_reqs_expected_cols)
        if error_check_crew_reqs == 'Passed':
            roster_df = master_df.merge(crew_reqs_df, how='left', on='Timetable').reindex()
            roster_df = roster_df.reindex(columns = roster_df.columns.tolist() + ['Driver','Fireman','Trainee'])
            save_location = filedialog.asksaveasfilename(title='Choose a save location',defaultextension='.csv')
            roster_df.to_csv(save_location, index=False)
            root_setup_0(frame_to_delete)
        else:
            root_setup_error(frame_to_delete,error_check_crew_reqs,crew_reqs_path)
    else:
        root_setup_error(frame_to_delete,error_check_master,timetable_path)

    
def root_setup_1(frame_to_delete):
    """
    Layout for the blank roster screen of the program - create blank roster
    """
    frame_to_delete.grid_forget()

    frame_1 = Frame(root, bg=background_col, width=width, height=height)

    timetable_label = Label (frame_1, text='Timetable dates and colours: ', bg=background_col, fg=foreground_col, font=font)
    timetable_entry = Entry(frame_1, width=50)
    timetable_path = Button (frame_1, text='Browse', width=6, command=partial(browse_file, timetable_entry))
    crew_reqs_label = Label (frame_1, text='Crew requirements by timetable colour: ', bg=background_col, fg=foreground_col, font=font)
    crew_reqs_entry = Entry(frame_1, width=50)
    crew_reqs_path = Button (frame_1, text='Browse', width=6, command=partial(browse_file, crew_reqs_entry))
    function_plus_args = partial(create_blank_roster, timetable_entry, crew_reqs_entry, frame_1)
    create_timetable_button = Button (frame_1, text='Create blank roster', width=19, command=function_plus_args)
    back_button_1 = Button (frame_1, text='Back', width=19, command=partial(root_setup_0, frame_1))

    frame_1.grid(row=0, column=0, sticky=W)

    timetable_label.grid(row=0, column=0, sticky=W, padx=25, pady=20)
    timetable_entry.grid(row=0, column=1, sticky=W, padx=0, pady=0)
    timetable_path.grid(row=0, column=2, sticky=E, padx=0, pady=0)
    crew_reqs_label.grid(row=1, column=0, sticky=W, padx=25, pady=0)
    crew_reqs_entry.grid(row=1, column=1, sticky=W, padx=0, pady=0)
    crew_reqs_path.grid(row=1, column=2, sticky=E, padx=0, pady=0)
    create_timetable_button.grid(row=3, column=1, sticky=E, padx=0, pady=15)
    back_button_1.grid(row=4, column=0, sticky=W, padx=25, pady = 20)
    
def create_blank_availability(timetable_location, frame_to_delete):
    """
    Creates blank availability forms
    """
    timetable_expected_cols = ['Date','Timetable']
    timetable_path = timetable_location.get()
    timetable_df = pd.read_csv(timetable_path)
    error_check = check_import_cols(timetable_df,timetable_expected_cols)
    if error_check == 'Passed':
        roster_avail_df = timetable_df[['Date']].copy()
        roster_avail_df['Available'] = ['' for i in timetable_df['Date']]
        avail_save_path = filedialog.asksaveasfilename(title='Choose a save location',defaultextension='.xlsx')
        writer = pd.ExcelWriter(avail_save_path, engine='xlsxwriter')
        sheet_name = 'Availability'
        roster_avail_df.to_excel(writer, sheet_name=sheet_name,index=False)
        workbook  = writer.book
        worksheet = writer.sheets[sheet_name]
        cell_format = workbook.add_format({'border':1})
        worksheet.set_column(0,0,11)
        data_val_cells = ['B'+str(i+2) for i,j in enumerate(roster_avail_df['Available'])]
        for i in data_val_cells:
            worksheet.data_validation(i,{'validate':'list','source': ['Y', 'N']})
        writer.save()
        root_setup_0(frame_to_delete)
    else:
        root_setup_error(frame_to_delete,error_check,timetable_path)

def root_setup_blank_avail(frame_to_delete):
    """
    Layout for the first screen of the program - create blank roster
    """
    frame_to_delete.grid_forget()

    frame_blank_avail = Frame(root, bg=background_col, width=width, height=height)

    intro_label = Label (frame_blank_avail, text='Create blank roster availability forms', bg=background_col, fg=foreground_col, font=font)
    timetable_label = Label (frame_blank_avail, text='Timetable dates and colours: ', bg=background_col, fg=foreground_col, font=font)
    timetable_entry = Entry(frame_blank_avail, width=50)
    timetable_path = Button (frame_blank_avail, text='Browse', width=6, command=partial(browse_file, timetable_entry))
    function_plus_args = partial(create_blank_availability, timetable_entry, frame_blank_avail)
    create_blank_avail_button = Button (frame_blank_avail, text='Create blank availability', width=25, command=function_plus_args)
    back_button_blank_avail = Button (frame_blank_avail, text='Back', width=19, command=partial(root_setup_0, frame_blank_avail))

    frame_blank_avail.grid(row=0, column=0, sticky=W)

    intro_label.grid(row=0, column=0, sticky=W, padx=25, pady=20, columnspan=2)
    timetable_label.grid(row=1, column=0, sticky=W, padx=25, pady=0)
    timetable_entry.grid(row=1, column=1, sticky=W, padx=0, pady=0)
    timetable_path.grid(row=1, column=2, sticky=E, padx=0, pady=0)
    create_blank_avail_button.grid(row=4, column=1, sticky=E, padx=0, pady=15)
    back_button_blank_avail.grid(row=5, column=0, sticky=W, padx=25, pady = 20)

def root_setup_0(frame_to_delete=0):
    """
    Hub screen
    """ 
    root.title(program_title)
    root.configure(background=background_col)
    window_geom = width + 'x' + height + '+' + screen_pos_right + '+' + screen_pos_down
    root.geometry(window_geom)

    if frame_to_delete != 0:
        frame_to_delete.grid_forget()

    frame_0 = Frame(root, bg=background_col, width=width, height=height)

    logo = PhotoImage(file=resource_path('pic1_4.png'))

    label_0 = Label (frame_0, image=logo)
    label_0.image = logo
    label_1 = Label (frame_0, text='Welcome to the WLLR footplate department rostering program!', bg=background_col, fg=foreground_col, font=font)
    label_2 = Label (frame_0, text='Step 1: Set up input files', bg=background_col, fg=foreground_col, font=font)
    label_3 = Label (frame_0, text='\t(1) timetable dates and colours', bg=background_col, fg=foreground_col, font=font)
    label_4 = Label (frame_0, text='\t(2) crew requirements for each colour timetable', bg=background_col, fg=foreground_col, font=font)
    label_5 = Label (frame_0, text='Step 2: Create blank availability forms', bg=background_col, fg=foreground_col, font=font)
    label_6 = Label (frame_0, text='Step 3: Create a blank roster', bg=background_col, fg=foreground_col, font=font)
    label_7 = Label (frame_0, text='Step 4: Open blank roster file and enter any specific crew allocations', bg=background_col, fg=foreground_col, font=font)
    label_8 = Label (frame_0, text='Step 5: Allocate crews to remaining turns', bg=background_col, fg=foreground_col, font=font)
    label_9 = Label (frame_0, text='Step 5a: Create availability summaries', bg=background_col, fg=foreground_col, font=font)
    label_10 = Label (frame_0, text='Step 6: Review allocations and amend as necessary', bg=background_col, fg=foreground_col, font=font)
    label_11 = Label (frame_0, text='Step 7: Generate individual rosters', bg=background_col, fg=foreground_col, font=font)

    button_5 = Button (frame_0, text='Blank availability', width=18, command=partial(root_setup_blank_avail, frame_0))
    button_6 = Button (frame_0, text='Blank roster', width=18, command=partial(root_setup_1, frame_0))
    button_8 = Button (frame_0, text='Allocate crews', width=18, command=partial(root_setup_2, frame_0))
    button_9 = Button (frame_0, text='Availability summary', width=18, command=partial(root_setup_2a, frame_0))
    button_11 = Button (frame_0, text='Individual rosters', width=18, command=partial(root_setup_3, frame_0))

    frame_0.grid(row=0, column=0, sticky=W)
    
    label_0.grid(row=0, column=0, padx = 5, pady = 5, columnspan=2)
    label_1.grid(row=1, column=0, padx = 25, pady = 15, columnspan=2)
    label_2.grid(row=2, column=0, sticky=W, padx = 25, pady = 0)
    label_3.grid(row=3, column=0, sticky=W, padx = 25, pady = 0)
    label_4.grid(row=4, column=0, sticky=W, padx = 25, pady = 0)
    label_5.grid(row=5, column=0, sticky=W, padx = 25, pady = 15)
    label_6.grid(row=6, column=0, sticky=W, padx = 25, pady = 10)
    label_7.grid(row=7, column=0, sticky=W, padx = 25, pady = 10)
    label_8.grid(row=8, column=0, sticky=W, padx = 25, pady = 10)
    label_9.grid(row=9, column=0, sticky=W, padx = 25, pady = 10)
    label_10.grid(row=10, column=0, sticky=W, padx = 25, pady = 10)
    label_11.grid(row=11, column=0, sticky=W, padx = 25, pady = 10)

    button_5.grid(row=5,column=1,sticky=W)
    button_6.grid(row=6,column=1,sticky=W)
    button_8.grid(row=8,column=1,sticky=W)
    button_9.grid(row=9,column=1,sticky=W)
    button_11.grid(row=11,column=1,sticky=W)

def main():
    root_setup_0()
    root.mainloop()

if __name__ == '__main__':
    main()

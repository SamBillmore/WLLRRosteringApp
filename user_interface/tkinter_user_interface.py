import tkinter as tk
from tkinter import Button
from tkinter import Label
from tkinter import Entry
from tkinter import filedialog
from tkinter import PhotoImage
import os

from blank_availability.create_blank_availability import Timetable
from blank_availability.create_blank_availability import Availability_Form
from blank_roster.create_blank_roster import Crew_Requirements
from blank_roster.create_blank_roster import Blank_Roster
from master_roster.create_master_roster import Master_Roster
from master_roster.create_master_availability import Master_Availability
from individual_rosters.create_individual_rosters import Individual_Rosters

class App(tk.Tk):
    """
    Overall container for app
    Individual screens are raised within this container
    """

    def __init__(self):
        """
        Initialise the class
        """
        tk.Tk.__init__(self)

        self.title('WLLR footplate crew rostering program')
        self.geometry('850x600+250+100')
        self.frame_names_list = (HomeScreen,BlankAvailabilityScreen,BlankRosterScreen,AllocateCrewsScreen,MasterAvailabilityScreen,IndividualRostersScreen,ErrorScreen)
        self.frames = {}
        self.background_col = 'black'
        self.foreground_col = 'white'
        self.font = 'courier 11'

        # the container holds the stack of frames on top of each other. The one to be visible will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create each frame instance and add to self.frames dictionary
        for frame_name in self.frame_names_list:
            frame_object = frame_name(parent=container, controller=self, background_col = self.background_col, foreground_col = self.foreground_col, font = self.font)
            self.frames[frame_name] = frame_object
            frame_object.grid(row=0, column=0, sticky="nsew")
        self.show_frame(HomeScreen)

    def show_frame(self, page_name):
        """
        Show a frame for the given page_name
        """
        frame = self.frames[page_name]
        frame.tkraise()

    def browse_file(self, entry):
        """
        Browse the file system
        """
        file_path = filedialog.askopenfilename(title='Choose a file')
        if file_path != None:
            entry.delete(0, 'end')
            entry.insert(0, file_path)

    def browse_directory(self, entry):
        """
        Browse the file system and select a directory
        """
        dir_path = filedialog.askdirectory(title='Choose a folder location')
        if dir_path != None:
            entry.delete(0, 'end')
            entry.insert(0, dir_path)

class HomeScreen(tk.Frame):
    """
    The home screen for the program
    """

    def __init__(self, parent, controller, background_col, foreground_col, font):
        """
        Layout for the home screen
        """
        tk.Frame.__init__(self, parent, bg=background_col)
        self.controller = controller
        self.parent = parent
        self.picture_path = './/user_interface//home_screen_pic.png'

        self.logo = PhotoImage(file=self.resource_path(self.picture_path))

        self.picture = Label (self, image=self.logo)
        self.picture.image = self.logo
        self.intro_label = Label (self, text='Welcome to the WLLR footplate department rostering program!', bg=background_col, fg=foreground_col, font=font)
        self.step_1_label = Label (self, text='Step 1: Set up input files', bg=background_col, fg=foreground_col, font=font)
        self.step_1a_label = Label (self, text='\t(1) timetable dates and colours', bg=background_col, fg=foreground_col, font=font)
        self.step_1b_label = Label (self, text='\t(2) crew requirements for each colour timetable', bg=background_col, fg=foreground_col, font=font)
        self.step_2_label = Label (self, text='Step 2: Create blank availability forms', bg=background_col, fg=foreground_col, font=font)
        self.step_3_label = Label (self, text='Step 3: Create a blank roster', bg=background_col, fg=foreground_col, font=font)
        self.step_4_label = Label (self, text='Step 4: Open blank roster file and enter any specific crew allocations', bg=background_col, fg=foreground_col, font=font)
        self.step_5_label = Label (self, text='Step 5: Allocate crews to remaining turns', bg=background_col, fg=foreground_col, font=font)
        self.step_6_label = Label (self, text='Step 6: Review allocations and amend as necessary', bg=background_col, fg=foreground_col, font=font)
        self.step_7_label = Label (self, text='Step 7: Generate individual rosters', bg=background_col, fg=foreground_col, font=font)

        self.step_2_button = Button (self, text='Blank availability', width=18, command=lambda: controller.show_frame(BlankAvailabilityScreen))
        self.step_3_button = Button (self, text='Blank roster', width=18, command=lambda: controller.show_frame(BlankRosterScreen))
        self.step_5_button = Button (self, text='Allocate crews', width=18, command=lambda: controller.show_frame(AllocateCrewsScreen))
        self.step_7_button = Button (self, text='Individual rosters', width=18, command=lambda: controller.show_frame(IndividualRostersScreen))
        
        self.picture.grid(row=0, column=0, padx = 5, pady = 5, columnspan=2)
        self.intro_label.grid(row=1, column=0, padx = 25, pady = 15, columnspan=2)
        self.step_1_label.grid(row=2, column=0, sticky='W', padx = 25, pady = 0)
        self.step_1a_label.grid(row=3, column=0, sticky='W', padx = 25, pady = 0)
        self.step_1b_label.grid(row=4, column=0, sticky='W', padx = 25, pady = 0)
        self.step_2_label.grid(row=5, column=0, sticky='W', padx = 25, pady = 15)
        self.step_3_label.grid(row=6, column=0, sticky='W', padx = 25, pady = 10)
        self.step_4_label.grid(row=7, column=0, sticky='W', padx = 25, pady = 10)
        self.step_5_label.grid(row=8, column=0, sticky='W', padx = 25, pady = 10)
        self.step_6_label.grid(row=9, column=0, sticky='W', padx = 25, pady = 10)
        self.step_7_label.grid(row=10, column=0, sticky='W', padx = 25, pady = 10)

        self.step_2_button.grid(row=5,column=1,sticky='W')
        self.step_3_button.grid(row=6,column=1,sticky='W')
        self.step_5_button.grid(row=8,column=1,sticky='W')
        self.step_7_button.grid(row=10,column=1,sticky='W')

    def resource_path(self, relative_path):
        """
        Create full filepath to picture
        """
        base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

class BlankAvailabilityScreen(tk.Frame):
    """
    Blank availability screen
    """

    def __init__(self, parent, controller, background_col, foreground_col, font):
        """
        Initialise the blank availability screen
        """
        tk.Frame.__init__(self, parent, bg=background_col)
        self.controller = controller
        self.parent = parent

        self.intro_label = Label (self, text='Create blank roster availability forms', bg=background_col, fg=foreground_col, font=font)
        self.timetable_label = Label (self, text='Timetable dates and colours: ', bg=background_col, fg=foreground_col, font=font)
        self.timetable_entry = Entry(self, width=50)
        self.timetable_path = Button (self, text='Browse', width=6, command=lambda: self.controller.browse_file(self.timetable_entry))
        self.create_blank_avail_button = Button (self, text='Create blank availability', width=25, command=lambda: self.create_blank_availability(self.timetable_entry.get()))
        self.back_button = Button (self, text='Back', width=19, command=lambda: self.controller.show_frame(HomeScreen))

        self.intro_label.grid(row=0, column=0, sticky='W', padx=25, pady=20, columnspan=2)
        self.timetable_label.grid(row=1, column=0, sticky='W', padx=25, pady=20)
        self.timetable_entry.grid(row=1, column=1, sticky='W', padx=0, pady=0)
        self.timetable_path.grid(row=1, column=2, sticky='E', padx=0, pady=0)
        self.create_blank_avail_button.grid(row=2, column=1, sticky='E', padx=0, pady=15)
        self.back_button.grid(row=3, column=0, sticky='W', padx=25, pady = 20)

    def create_blank_availability(self,timetable_path):
        """
        Creating blank availability forms
        """
        timetable = Timetable()
        availability_form = Availability_Form()
        file_import_test = timetable.import_data(timetable_path)
        if file_import_test:
            save_location = filedialog.asksaveasfilename(title='Choose a save location',defaultextension='.xlsx')
            availability_form.get_timetable_dates(timetable)
            availability_form.create_availability_form(save_location)
            self.controller.show_frame(HomeScreen)
        else:
            self.controller.frames[ErrorScreen].update_error_messages(timetable_path,timetable.expected_columns)
            self.controller.show_frame(ErrorScreen)

class BlankRosterScreen(tk.Frame):
    """
    Blank roster screen
    """

    def __init__(self, parent, controller, background_col, foreground_col, font):
        """
        Initialise the blank roster screen
        """
        tk.Frame.__init__(self, parent, bg=background_col)
        self.controller = controller
        self.parent = parent

        self.intro_label = Label (self, text='Create a blank roster template', bg=background_col, fg=foreground_col, font=font)
        self.timetable_label = Label (self, text='Timetable dates and colours: ', bg=background_col, fg=foreground_col, font=font)
        self.timetable_entry = Entry(self, width=50)
        self.timetable_path = Button (self, text='Browse', width=6, command=lambda: self.controller.browse_file(self.timetable_entry))
        self.crew_reqs_label = Label (self, text='Crew requirements by timetable colour: ', bg=background_col, fg=foreground_col, font=font)
        self.crew_reqs_entry = Entry(self, width=50)
        self.crew_reqs_path = Button (self, text='Browse', width=6, command=lambda: self.controller.browse_file(self.crew_reqs_entry))
        self.create_timetable_button = Button (self, text='Create blank roster', width=19, command=lambda: self.create_blank_roster(self.timetable_entry.get(),self.crew_reqs_entry.get()))
        self.back_button = Button (self, text='Back', width=19, command=lambda: self.controller.show_frame(HomeScreen))

        self.intro_label.grid(row=0, column=0, sticky='W', padx=25, pady=20, columnspan=2)
        self.timetable_label.grid(row=1, column=0, sticky='W', padx=25, pady=20)
        self.timetable_entry.grid(row=1, column=1, sticky='W', padx=0, pady=0)
        self.timetable_path.grid(row=1, column=2, sticky='E', padx=0, pady=0)
        self.crew_reqs_label.grid(row=2, column=0, sticky='W', padx=25, pady=0)
        self.crew_reqs_entry.grid(row=2, column=1, sticky='W', padx=0, pady=0)
        self.crew_reqs_path.grid(row=2, column=2, sticky='E', padx=0, pady=0)
        self.create_timetable_button.grid(row=3, column=1, sticky='E', padx=0, pady=15)
        self.back_button.grid(row=4, column=0, sticky='W', padx=25, pady = 20)

    def create_blank_roster(self,timetable_path,crew_reqs_path):
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
                save_location = filedialog.asksaveasfilename(title='Choose a save location',defaultextension='.xlsx')
                blank_roster.create_blank_roster(timetable.data_import,crew_reqs.data_import,save_location)
                self.controller.show_frame(HomeScreen)
            else:
                self.controller.frames[ErrorScreen].update_error_messages(crew_reqs_path,crew_reqs.expected_columns)
                self.controller.show_frame(ErrorScreen)
        else:
            self.controller.frames[ErrorScreen].update_error_messages(timetable_path,timetable.expected_columns)
            self.controller.show_frame(ErrorScreen)

class AllocateCrewsScreen(tk.Frame):
    """
    Allocate crews screen
    """

    def __init__(self, parent, controller, background_col, foreground_col, font):
        """
        Initialise the allocating crews screen
        """
        tk.Frame.__init__(self, parent, bg=background_col)
        self.controller = controller
        self.parent = parent

        self.instruction_label = Label(self, text='Allocate crews to turns', bg=background_col, fg=foreground_col, font=font)
        self.driver_avail_label = Label (self, text='Driver availability folder: ', bg=background_col, fg=foreground_col, font=font)
        self.driver_avail_entry = Entry(self, width=50)
        self.driver_avail_button = Button (self, text='Browse', width=6, command=lambda: self.controller.browse_directory(self.driver_avail_entry))
        self.fireman_avail_label = Label (self, text='Fireman availability folder: ', bg=background_col, fg=foreground_col, font=font)
        self.fireman_avail_entry = Entry(self, width=50)
        self.fireman_avail_button = Button (self, text='Browse', width=6, command=lambda: self.controller.browse_directory(self.fireman_avail_entry))
        self.trainee_avail_label = Label (self, text='Trainee availability folder: ', bg=background_col, fg=foreground_col, font=font)
        self.trainee_avail_entry = Entry(self, width=50)
        self.trainee_avail_button = Button (self, text='Browse', width=6, command=lambda: self.controller.browse_directory(self.trainee_avail_entry))
        self.blank_roster_label = Label (self, text='Working roster location: ', bg=background_col, fg=foreground_col, font=font)
        self.blank_roster_entry = Entry(self, width=50)
        self.blank_roster_button = Button (self, text='Browse', width=6, command=lambda: self.controller.browse_file(self.blank_roster_entry))
        self.create_timetable_button = Button (self, text='Allocate crews to roster', width=24, command=lambda: self.master_roster(self.blank_roster_entry.get(),self.driver_avail_entry.get(),self.fireman_avail_entry.get(),self.trainee_avail_entry.get()))
        self.back_button = Button (self, text='Back', width=19, command=lambda: self.controller.show_frame(HomeScreen))

        self.instruction_label.grid(row=0, column=0, sticky='W', padx=25, pady=20, columnspan=2)
        self.driver_avail_label.grid(row=1, column=0, sticky='W', padx=25, pady=0)
        self.driver_avail_entry.grid(row=1, column=1, sticky='E', padx=0, pady=0)
        self.driver_avail_button.grid(row=1, column=2, sticky='W', padx=0, pady=0)
        self.fireman_avail_label.grid(row=2, column=0, sticky='W', padx=25, pady=0)
        self.fireman_avail_entry.grid(row=2, column=1, sticky='E', padx=0, pady=0)
        self.fireman_avail_button.grid(row=2, column=2, sticky='W', padx=0, pady=0)
        self.trainee_avail_label.grid(row=3, column=0, sticky='W', padx=25, pady=0)
        self.trainee_avail_entry.grid(row=3, column=1, sticky='E', padx=0, pady=0)
        self.trainee_avail_button.grid(row=3, column=2, sticky='W', padx=0, pady=0)
        self.blank_roster_label.grid(row=4, column=0, sticky='W', padx=25, pady=20)
        self.blank_roster_entry.grid(row=4, column=1, sticky='E', padx=0, pady=0)
        self.blank_roster_button.grid(row=4, column=2, sticky='W', padx=0, pady=0)
        self.create_timetable_button.grid(row=5, column=1, sticky='E', padx=0, pady=15)
        self.back_button.grid(row=6, column=0, sticky='W', padx=25, pady = 20)

    def master_roster(self,working_roster_path,driver_availability_folder,fireman_availability_folder,trainee_availability_folder):
        """
        Master function to control:
        - creating master availability
        - create master roster by allocating availability to turns
        """
        availability_folders = {
            'Driver':driver_availability_folder,
            'Fireman':fireman_availability_folder,
            'Trainee':trainee_availability_folder
        }
        master_roster = Master_Roster()
        master_availability = Master_Availability()
        working_roster_import_test = master_roster.import_data(working_roster_path)
        if working_roster_import_test:
            availability_import_test,file_name,expected_columns = master_roster.create_master_roster(availability_folders,master_availability)
            if availability_import_test:
                master_roster_save_location = filedialog.asksaveasfilename(title='Choose a save location',defaultextension='.xlsx')
                master_roster.export_data(filepath=master_roster_save_location,sheet_name='master_roster')
                # master_avail_save_location = filedialog.asksaveasfilename(title='Choose a save location',defaultextension='.xlsx')
                self.controller.frames[MasterAvailabilityScreen].update_master_availability(master_availability)
                # master_availability.export_data(filepath=master_avail_save_location,sheet_name='master_availability')
                self.controller.show_frame(MasterAvailabilityScreen)
            else:
                self.controller.frames[ErrorScreen].update_error_messages(file_name,expected_columns)
                self.controller.show_frame(ErrorScreen)
        else:
            self.controller.frames[ErrorScreen].update_error_messages(working_roster_path,master_roster.expected_columns)
            self.controller.show_frame(ErrorScreen)

class MasterAvailabilityScreen(tk.Frame):
    """
    Screen to provide the option to download the master availability
    """

    def __init__(self, parent, controller, background_col, foreground_col, font):
        """
        Initialise the master availability screen
        """
        tk.Frame.__init__(self, parent, bg=background_col)
        self.controller = controller
        self.parent = parent
        self.master_availability = None

        self.intro_label = Label (self, text='Would you also like to download a summary of the crew availability?', bg=background_col, fg=foreground_col, font=font)
        self.yes_button = Button (self, text='Yes', width=19, command=lambda: self.save_master_availability())
        self.no_button = Button (self, text='No', width=19, command=lambda: self.controller.show_frame(HomeScreen))

        self.intro_label.grid(row=0, column=0, sticky='W', padx=25, pady=20, columnspan=2)
        self.yes_button.grid(row=1, column=1, sticky='W', padx=25, pady = 20)
        self.no_button.grid(row=1, column=0, sticky='W', padx=25, pady = 20)

    def update_master_availability(self,master_availability):
        """
        Update self.master_availability to hold an instance of the object (master_availability)
        """
        self.master_availability = master_availability

    def save_master_availability(self):
        """
        Save master availability
        """
        master_avail_save_location = filedialog.asksaveasfilename(title='Choose a save location',defaultextension='.xlsx')
        self.master_availability.export_data(filepath=master_avail_save_location,sheet_name='master_availability')
        self.controller.show_frame(HomeScreen)

class IndividualRostersScreen(tk.Frame):
    """
    Individual rosters screen
    """

    def __init__(self, parent, controller, background_col, foreground_col, font):
        """
        Initialise the individual rosters screen
        """
        tk.Frame.__init__(self, parent, bg=background_col)
        self.controller = controller
        self.parent = parent

        self.intro_label = Label (self, text='Create individual rosters from the master roster', bg=background_col, fg=foreground_col, font=font)
        self.fin_roster_label = Label (self, text='Finalised roster: ', bg=background_col, fg=foreground_col, font=font)
        self.fin_roster_entry = Entry(self, width=50)
        self.fin_roster_button = Button (self, text='Browse', width=6, command=lambda: self.controller.browse_file(self.fin_roster_entry))
        self.save_folder_label = Label (self, text='Save location: ', bg=background_col, fg=foreground_col, font=font)
        self.save_folder_entry = Entry(self, width=50)
        self.save_folder_button = Button (self, text='Browse', width=6, command=lambda: self.controller.browse_directory(self.save_folder_entry))
        self.create_indiv_roster_button = Button (self, text='Create individual rosters', width=25, command=lambda: self.individual_rosters(self.fin_roster_entry.get(),self.save_folder_entry.get()))
        self.back_button = Button (self, text='Back', width=19, command=lambda: self.controller.show_frame(HomeScreen))

        self.intro_label.grid(row=0, column=0, sticky='W', padx=25, pady=20, columnspan=2)
        self.fin_roster_label.grid(row=1, column=0, sticky='W', padx=25, pady=20)
        self.fin_roster_entry.grid(row=1, column=1, sticky='W', padx=0, pady=0)
        self.fin_roster_button.grid(row=1, column=2, sticky='E', padx=0, pady=0)
        self.save_folder_label.grid(row=2, column=0, sticky='W', padx=25, pady=20)
        self.save_folder_entry.grid(row=2, column=1, sticky='W', padx=0, pady=0)
        self.save_folder_button.grid(row=2, column=2, sticky='E', padx=0, pady=0)
        self.create_indiv_roster_button.grid(row=3, column=1, sticky='E', padx=0, pady=15)
        self.back_button.grid(row=4, column=0, sticky='W', padx=25, pady = 20)

    def individual_rosters(self,final_roster_path,individual_roster_save_folder):
        """
        Create individual rosters from the final roster
        """
        individual_rosters = Individual_Rosters()
        file_import_test = individual_rosters.import_data(final_roster_path)
        if file_import_test:
            individual_rosters.create_individual_rosters(individual_roster_save_folder)
            self.controller.show_frame(HomeScreen)
        else:
            self.controller.frames[ErrorScreen].update_error_messages(final_roster_path,individual_rosters.expected_columns)
            self.controller.show_frame(ErrorScreen)

class ErrorScreen(tk.Frame):
    """
    Screen for showing errors in data import
    """
    
    def __init__(self, parent, controller, background_col, foreground_col, font):
        """
        Initialise the error screen
        """
        tk.Frame.__init__(self, parent, bg=background_col)
        self.controller = controller
        self.parent = parent

        self.intro_label = Label (self, text='There has been an error with one of the files imported', bg=background_col, fg=foreground_col, font=font)
        self.filepath_label = Label (self, text='The file with errors is: ', bg=background_col, fg=foreground_col, font=font)
        self.expected_columns_label = Label (self, text='The expected columns are: ', bg=background_col, fg=foreground_col, font=font)
        self.error_filepath_label = Label (self, text='', bg=background_col, fg=foreground_col, font=font)
        self.error_expected_columns_label = Label (self, text='', bg=background_col, fg=foreground_col, font=font)
        self.back_button = Button (self, text='Back', width=19, command=lambda: self.controller.show_frame(HomeScreen))

        self.intro_label.grid(row=0, column=0, sticky='W', padx=25, pady=20, columnspan=2)
        self.filepath_label.grid(row=1, column=0, sticky='W', padx=25, pady=0)
        self.expected_columns_label.grid(row=2, column=0, sticky='W', padx=25, pady=0)
        self.error_filepath_label.grid(row=1, column=1, sticky='W', padx=25, pady=0)
        self.error_expected_columns_label.grid(row=2, column=1, sticky='W', padx=25, pady=0)
        self.back_button.grid(row=3, column=0, sticky='W', padx=25, pady = 20)

    def update_error_messages(self,error_filepath,error_expected_columns):
        """
        Update self.error_filepath_label and self.error_expected_columns_label
        """
        error_filename = os.path.basename(error_filepath)
        self.error_filepath_label['text'] = error_filename
        self.error_expected_columns_label['text'] = error_expected_columns
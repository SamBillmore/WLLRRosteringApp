from tkinter import Frame
from tkinter import Button
from tkinter import Label
from tkinter import Entry
from tkinter import filedialog

from blank_availability.create_blank_availability import Timetable
from blank_roster.create_blank_roster import Crew_Requirements
from blank_roster.create_blank_roster import Blank_Roster

class BlankRosterScreen(Frame):
    """
    Blank roster screen
    """

    def __init__(self, parent, controller, background_col, foreground_col, font):
        """
        Initialise the blank roster screen
        """
        Frame.__init__(self, parent, bg=background_col)
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
        self.back_button = Button (self, text='Back', width=19, command=lambda: self.controller.show_frame('HomeScreen'))

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
                self.controller.show_frame('WaitScreen')
                export_test = blank_roster.create_blank_roster(timetable.data_import,crew_reqs.data_import,save_location)
                if export_test:
                    self.controller.show_frame('HomeScreen')
                else:
                    self.controller.show_frame('ErrorScreenExport')
            else:
                self.controller.frames['ErrorScreen'].update_error_messages(crew_reqs_path,crew_reqs.expected_columns)
                self.controller.show_frame('ErrorScreen')
        else:
            self.controller.frames['ErrorScreen'].update_error_messages(timetable_path,timetable.expected_columns)
            self.controller.show_frame('ErrorScreen')
from tkinter import Frame
from tkinter import Button
from tkinter import Label
from tkinter import Entry
from tkinter import filedialog
from time import sleep

from blank_availability.create_blank_availability import Timetable
from blank_availability.create_blank_availability import Availability_Form

class BlankAvailabilityScreen(Frame):
    """
    Blank availability screen
    """

    def __init__(self, parent, controller, background_col, foreground_col, font):
        """
        Initialise the blank availability screen
        """
        Frame.__init__(self, parent, bg=background_col)
        self.controller = controller
        self.parent = parent

        self.intro_label = Label (self, text='Create blank roster availability forms', bg=background_col, fg=foreground_col, font=font)
        self.timetable_label = Label (self, text='Timetable dates and colours: ', bg=background_col, fg=foreground_col, font=font)
        self.timetable_entry = Entry(self, width=50)
        self.timetable_path = Button (self, text='Browse', width=6, command=lambda: self.controller.browse_file(self.timetable_entry))
        self.create_blank_avail_button = Button (self, text='Create blank availability', width=25, command=lambda: self.create_blank_availability(self.timetable_entry.get()))
        self.back_button = Button (self, text='Back', width=19, command=lambda: self.controller.show_frame('HomeScreen'))

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
            self.controller.show_frame('WaitScreen')
            sleep(1.5)
            availability_form.get_timetable_dates(timetable)
            export_test = availability_form.create_availability_form(save_location)
            if export_test:
                self.controller.show_frame('HomeScreen')
            else:
                self.controller.show_frame('ErrorScreenExport')
        else:
            self.controller.frames['ErrorScreen'].update_error_messages(timetable_path,timetable.expected_columns)
            self.controller.show_frame('ErrorScreen')
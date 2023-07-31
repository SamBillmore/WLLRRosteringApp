from tkinter import Frame
from tkinter import Button
from tkinter import Label
from tkinter import filedialog

class MasterAvailabilityScreen(Frame):
    """
    Screen to provide the option to download the master availability
    """

    def __init__(self, parent, controller, background_col, foreground_col, font):
        """
        Initialise the master availability screen
        """
        Frame.__init__(self, parent, bg=background_col)
        self.controller = controller
        self.parent = parent
        self.master_availability = None

        self.intro_label = Label (self, text='Would you also like to download a summary of the crew availability?', bg=background_col, fg=foreground_col, font=font)
        self.yes_button = Button (self, text='Yes', width=19, command=lambda: self.save_master_availability())
        self.no_button = Button (self, text='No', width=19, command=lambda: self.controller.show_frame('HomeScreen'))

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
        self.controller.show_frame('WaitScreen')
        export_test = self.master_availability.export_data(filepath=master_avail_save_location,sheet_name='master_availability')
        if export_test:
            self.controller.show_frame('HomeScreen')
        else:
            self.controller.show_frame('ErrorScreenExport')
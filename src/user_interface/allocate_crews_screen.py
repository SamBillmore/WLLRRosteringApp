from tkinter import Frame
from tkinter import Button
from tkinter import Label
from tkinter import Entry
from tkinter import filedialog

from master_roster.create_master_roster import create_master_roster
from error_handling.error_handling_decorator import handle_errors


class AllocateCrewsScreen(Frame):
    """Allocate crews screen."""

    def __init__(self, parent, controller, background_col, foreground_col, font):
        """Initialise the allocating crews screen."""
        Frame.__init__(self, parent, bg=background_col)
        self.controller = controller
        self.parent = parent

        self.instruction_label = Label(
            self,
            text="Allocate crews to turns",
            bg=background_col,
            fg=foreground_col,
            font=font,
        )
        self.driver_avail_label = Label(
            self,
            text="Driver availability folder: ",
            bg=background_col,
            fg=foreground_col,
            font=font,
        )
        self.driver_avail_entry = Entry(self, width=50)
        self.driver_avail_button = Button(
            self,
            text="Browse",
            width=6,
            command=lambda: self.controller.browse_directory(self.driver_avail_entry),
        )
        self.fireman_avail_label = Label(
            self,
            text="Fireman availability folder: ",
            bg=background_col,
            fg=foreground_col,
            font=font,
        )
        self.fireman_avail_entry = Entry(self, width=50)
        self.fireman_avail_button = Button(
            self,
            text="Browse",
            width=6,
            command=lambda: self.controller.browse_directory(self.fireman_avail_entry),
        )
        self.trainee_avail_label = Label(
            self,
            text="Trainee availability folder: ",
            bg=background_col,
            fg=foreground_col,
            font=font,
        )
        self.trainee_avail_entry = Entry(self, width=50)
        self.trainee_avail_button = Button(
            self,
            text="Browse",
            width=6,
            command=lambda: self.controller.browse_directory(self.trainee_avail_entry),
        )
        self.blank_roster_label = Label(
            self,
            text="Working roster location: ",
            bg=background_col,
            fg=foreground_col,
            font=font,
        )
        self.blank_roster_entry = Entry(self, width=50)
        self.blank_roster_button = Button(
            self,
            text="Browse",
            width=6,
            command=lambda: self.controller.browse_file(self.blank_roster_entry),
        )
        self.create_timetable_button = Button(
            self,
            text="Allocate crews to roster",
            width=24,
            command=lambda: self.run_create_master_roster(
                self.blank_roster_entry.get(),
                self.driver_avail_entry.get(),
                self.fireman_avail_entry.get(),
                self.trainee_avail_entry.get(),
            ),
        )
        self.back_button = Button(
            self,
            text="Back",
            width=19,
            command=lambda: self.controller.show_frame("HomeScreen"),
        )

        self.instruction_label.grid(
            row=0, column=0, sticky="W", padx=25, pady=20, columnspan=2
        )
        self.driver_avail_label.grid(row=1, column=0, sticky="W", padx=25, pady=0)
        self.driver_avail_entry.grid(row=1, column=1, sticky="E", padx=0, pady=0)
        self.driver_avail_button.grid(row=1, column=2, sticky="W", padx=0, pady=0)
        self.fireman_avail_label.grid(row=2, column=0, sticky="W", padx=25, pady=0)
        self.fireman_avail_entry.grid(row=2, column=1, sticky="E", padx=0, pady=0)
        self.fireman_avail_button.grid(row=2, column=2, sticky="W", padx=0, pady=0)
        self.trainee_avail_label.grid(row=3, column=0, sticky="W", padx=25, pady=0)
        self.trainee_avail_entry.grid(row=3, column=1, sticky="E", padx=0, pady=0)
        self.trainee_avail_button.grid(row=3, column=2, sticky="W", padx=0, pady=0)
        self.blank_roster_label.grid(row=4, column=0, sticky="W", padx=25, pady=20)
        self.blank_roster_entry.grid(row=4, column=1, sticky="E", padx=0, pady=0)
        self.blank_roster_button.grid(row=4, column=2, sticky="W", padx=0, pady=0)
        self.create_timetable_button.grid(row=5, column=1, sticky="E", padx=0, pady=15)
        self.back_button.grid(row=6, column=0, sticky="W", padx=25, pady=20)

    @handle_errors
    def run_create_master_roster(
        self,
        working_roster_path,
        driver_availability_folder,
        fireman_availability_folder,
        trainee_availability_folder,
    ):
        """
        Master function to control:
        - creating master availability
        - create master roster by allocating availability to turns
        """
        master_roster_save_location = filedialog.asksaveasfilename(
            title="Choose a save location", defaultextension=".xlsx"
        )
        self.controller.show_frame("WaitScreen")
        master_availability = create_master_roster(
            working_roster_path,
            driver_availability_folder,
            fireman_availability_folder,
            trainee_availability_folder,
            master_roster_save_location,
        )
        self.controller.frames["MasterAvailabilityScreen"].update_master_availability(
            master_availability
        )
        self.controller.show_frame("MasterAvailabilityScreen")

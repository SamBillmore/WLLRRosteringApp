from tkinter import Frame
from tkinter import Button
from tkinter import Label
from tkinter import Entry
from tkinter import filedialog

from blank_roster.create_blank_roster import create_blank_roster
from error_handling.error_handling_decorator import handle_errors


class BlankRosterScreen(Frame):
    """Blank roster screen."""

    def __init__(self, parent, controller, background_col, foreground_col, font):
        """Initialise the blank roster screen."""
        Frame.__init__(self, parent, bg=background_col)
        self.controller = controller
        self.parent = parent

        self.intro_label = Label(
            self,
            text="Create a blank roster template",
            bg=background_col,
            fg=foreground_col,
            font=font,
        )
        self.timetable_label = Label(
            self,
            text="Timetable dates and colours: ",
            bg=background_col,
            fg=foreground_col,
            font=font,
        )
        self.timetable_entry = Entry(self, width=50)
        self.timetable_path = Button(
            self,
            text="Browse",
            width=6,
            command=lambda: self.controller.browse_file(self.timetable_entry),
        )
        self.crew_reqs_label = Label(
            self,
            text="Crew requirements by timetable colour: ",
            bg=background_col,
            fg=foreground_col,
            font=font,
        )
        self.crew_reqs_entry = Entry(self, width=50)
        self.crew_reqs_path = Button(
            self,
            text="Browse",
            width=6,
            command=lambda: self.controller.browse_file(self.crew_reqs_entry),
        )
        self.create_timetable_button = Button(
            self,
            text="Create blank roster",
            width=19,
            command=lambda: self.run_create_blank_roster(
                self.timetable_entry.get(), self.crew_reqs_entry.get()
            ),
        )
        self.back_button = Button(
            self,
            text="Back",
            width=19,
            command=lambda: self.controller.show_frame("HomeScreen"),
        )

        self.intro_label.grid(
            row=0, column=0, sticky="W", padx=25, pady=20, columnspan=2
        )
        self.timetable_label.grid(row=1, column=0, sticky="W", padx=25, pady=20)
        self.timetable_entry.grid(row=1, column=1, sticky="W", padx=0, pady=0)
        self.timetable_path.grid(row=1, column=2, sticky="E", padx=0, pady=0)
        self.crew_reqs_label.grid(row=2, column=0, sticky="W", padx=25, pady=0)
        self.crew_reqs_entry.grid(row=2, column=1, sticky="W", padx=0, pady=0)
        self.crew_reqs_path.grid(row=2, column=2, sticky="E", padx=0, pady=0)
        self.create_timetable_button.grid(row=3, column=1, sticky="E", padx=0, pady=15)
        self.back_button.grid(row=4, column=0, sticky="W", padx=25, pady=20)

    @handle_errors
    def run_create_blank_roster(self, timetable_path, crew_reqs_path):
        save_location = filedialog.asksaveasfilename(
            title="Choose a save location", defaultextension=".xlsx"
        )
        self.controller.show_frame("WaitScreen")
        create_blank_roster(timetable_path, crew_reqs_path, save_location)
        self.controller.show_frame("HomeScreen")

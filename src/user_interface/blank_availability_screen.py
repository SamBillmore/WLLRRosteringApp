from tkinter import Frame
from tkinter import Button
from tkinter import Label
from tkinter import Entry
from tkinter import filedialog

from blank_availability.create_blank_availability import create_blank_availability


class BlankAvailabilityScreen(Frame):
    """Blank availability screen."""

    def __init__(self, parent, controller, background_col, foreground_col, font):
        """Initialise the blank availability screen."""
        Frame.__init__(self, parent, bg=background_col)
        self.controller = controller
        self.parent = parent

        self.intro_label = Label(
            self,
            text="Create blank roster availability forms",
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
        self.create_blank_avail_button = Button(
            self,
            text="Create blank availability",
            width=25,
            command=lambda: self.run_create_blank_availability(
                self.timetable_entry.get()
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
        self.create_blank_avail_button.grid(
            row=2, column=1, sticky="E", padx=0, pady=15
        )
        self.back_button.grid(row=3, column=0, sticky="W", padx=25, pady=20)

    def run_create_blank_availability(self, timetable_path):
        """Creating blank availability forms."""
        save_location = filedialog.asksaveasfilename(
            title="Choose a save location", defaultextension=".xlsx"
        )
        self.controller.show_frame("WaitScreen")
        try:
            create_blank_availability(timetable_path, save_location)
            self.controller.show_frame("HomeScreen")
        except Exception as e:
            self.controller.frames["ErrorScreen"].display_error_message(
                f"There has been an error: {e}"
            )
            self.controller.show_frame("ErrorScreen")

from tkinter import Frame
from tkinter import Button
from tkinter import Label
from tkinter import Entry

from individual_rosters.create_individual_rosters import create_individual_rosters


class IndividualRostersScreen(Frame):
    """Individual rosters screen."""

    def __init__(self, parent, controller, background_col, foreground_col, font):
        """Initialise the individual rosters screen."""
        Frame.__init__(self, parent, bg=background_col)
        self.controller = controller
        self.parent = parent

        self.intro_label = Label(
            self,
            text="Create individual rosters from the master roster",
            bg=background_col,
            fg=foreground_col,
            font=font,
        )
        self.fin_roster_label = Label(
            self,
            text="Finalised roster: ",
            bg=background_col,
            fg=foreground_col,
            font=font,
        )
        self.fin_roster_entry = Entry(self, width=50)
        self.fin_roster_button = Button(
            self,
            text="Browse",
            width=6,
            command=lambda: self.controller.browse_file(self.fin_roster_entry),
        )
        self.save_folder_label = Label(
            self,
            text="Save location: ",
            bg=background_col,
            fg=foreground_col,
            font=font,
        )
        self.save_folder_entry = Entry(self, width=50)
        self.save_folder_button = Button(
            self,
            text="Browse",
            width=6,
            command=lambda: self.controller.browse_directory(self.save_folder_entry),
        )
        self.create_indiv_roster_button = Button(
            self,
            text="Create individual rosters",
            width=25,
            command=lambda: self.run_create_individual_rosters(
                self.fin_roster_entry.get(), self.save_folder_entry.get()
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
        self.fin_roster_label.grid(row=1, column=0, sticky="W", padx=25, pady=20)
        self.fin_roster_entry.grid(row=1, column=1, sticky="W", padx=0, pady=0)
        self.fin_roster_button.grid(row=1, column=2, sticky="E", padx=0, pady=0)
        self.save_folder_label.grid(row=2, column=0, sticky="W", padx=25, pady=20)
        self.save_folder_entry.grid(row=2, column=1, sticky="W", padx=0, pady=0)
        self.save_folder_button.grid(row=2, column=2, sticky="E", padx=0, pady=0)
        self.create_indiv_roster_button.grid(
            row=3, column=1, sticky="E", padx=0, pady=15
        )
        self.back_button.grid(row=4, column=0, sticky="W", padx=25, pady=20)

    def run_create_individual_rosters(
        self, final_roster_path, individual_roster_save_folder
    ):
        self.controller.show_frame("WaitScreen")
        try:
            create_individual_rosters(final_roster_path, individual_roster_save_folder)
            self.controller.show_frame("HomeScreen")
        except Exception as e:
            self.controller.frames["ErrorScreen"].display_error_message(
                f"There has been an error: {e}"
            )
            self.controller.show_frame("ErrorScreen")

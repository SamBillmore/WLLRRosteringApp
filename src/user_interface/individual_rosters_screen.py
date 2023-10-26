from tkinter import Frame
from tkinter import Button
from tkinter import Label
from tkinter import Entry

from individual_rosters.create_individual_rosters import create_individual_rosters
from error_handling.error_handling_decorator import handle_errors


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
            anchor="w",
        )
        self.fin_roster_label = Label(
            self,
            text="Finalised roster: ",
            bg=background_col,
            fg=foreground_col,
            font=font,
            anchor="w",
        )
        self.fin_roster_entry = Entry(self)
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
            anchor="w",
        )
        self.save_folder_entry = Entry(self)
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

        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(2, minsize=350)
        self.grid_columnconfigure(4, weight=2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=3)

        self.intro_label.grid(
            row=1, column=1, sticky="W", padx=25, pady=20, columnspan=2
        )
        self.fin_roster_label.grid(row=2, column=1, sticky="W", padx=25, pady=20)
        self.fin_roster_entry.grid(row=2, column=2, sticky="EW", padx=0, pady=0)
        self.fin_roster_button.grid(row=2, column=3, sticky="W", padx=5, pady=0)
        self.save_folder_label.grid(row=3, column=1, sticky="W", padx=25, pady=20)
        self.save_folder_entry.grid(row=3, column=2, sticky="EW", padx=0, pady=0)
        self.save_folder_button.grid(row=3, column=3, sticky="W", padx=5, pady=0)
        self.create_indiv_roster_button.grid(
            row=4, column=2, sticky="E", padx=0, pady=15
        )
        self.back_button.grid(row=5, column=1, sticky="W", padx=25, pady=20)

    @handle_errors
    def run_create_individual_rosters(
        self, final_roster_path, individual_roster_save_folder
    ):
        self.controller.show_frame("WaitScreen")
        create_individual_rosters(final_roster_path, individual_roster_save_folder)
        self.controller.show_frame("HomeScreen")

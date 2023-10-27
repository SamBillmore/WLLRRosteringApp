from tkinter import Frame
from tkinter import Button
from tkinter import Label
from tkinter import PhotoImage
from tkinter import filedialog

from user_interface.blank_availability_screen import BlankAvailabilityScreen
from user_interface.blank_roster_screen import BlankRosterScreen
from user_interface.allocate_crews_screen import AllocateCrewsScreen
from user_interface.individual_rosters_screen import IndividualRostersScreen
from user_interface.resource_path import ResourcePath
from example_base_inputs.create_example_base_inputs import create_example_base_inputs
from error_handling.error_handling_decorator import handle_errors


class HomeScreen(Frame, ResourcePath):
    """The home screen for the program."""

    def __init__(self, parent, controller, background_col, foreground_col, font):
        """Layout for the home screen."""
        Frame.__init__(self, parent, bg=background_col)
        self.controller = controller
        self.parent = parent
        self.picture_path = "src/user_interface/home_screen_pic.png"

        self.logo = PhotoImage(file=self.resource_path(self.picture_path))

        self.picture = Label(self, image=self.logo)
        self.picture.image = self.logo
        self.intro_label = Label(
            self,
            text="Welcome to the WLLR footplate department rostering program!",
            bg=background_col,
            fg=foreground_col,
            font=font,
        )
        self.step_1_label = Label(
            self,
            text="Step 1: Set up input files and folders",
            bg=background_col,
            fg=foreground_col,
            font=font,
            anchor="w",
        )
        self.step_1a_label = Label(
            self,
            text="\t(1) timetable dates and colours",
            bg=background_col,
            fg=foreground_col,
            font=font,
            anchor="w",
        )
        self.step_1b_label = Label(
            self,
            text="\t(2) crew requirements for each colour timetable",
            bg=background_col,
            fg=foreground_col,
            font=font,
            anchor="w",
        )
        self.step_1c_label = Label(
            self,
            text="\t(3) folders for availability (by grade)",
            bg=background_col,
            fg=foreground_col,
            font=font,
            anchor="w",
        )
        self.step_2_label = Label(
            self,
            text="Step 2: Create blank availability forms",
            bg=background_col,
            fg=foreground_col,
            font=font,
            anchor="w",
        )
        self.step_3_label = Label(
            self,
            text="Step 3: Create a blank roster",
            bg=background_col,
            fg=foreground_col,
            font=font,
            anchor="w",
        )
        self.step_4_label = Label(
            self,
            text="Step 4: Open blank roster file and "
            "enter any specific crew allocations",
            bg=background_col,
            fg=foreground_col,
            font=font,
            anchor="w",
        )
        self.step_5_label = Label(
            self,
            text="Step 5: Allocate crews to remaining turns",
            bg=background_col,
            fg=foreground_col,
            font=font,
            anchor="w",
        )
        self.step_6_label = Label(
            self,
            text="Step 6: Review allocations and amend as necessary",
            bg=background_col,
            fg=foreground_col,
            font=font,
            anchor="w",
        )
        self.step_7_label = Label(
            self,
            text="Step 7: Generate individual rosters",
            bg=background_col,
            fg=foreground_col,
            font=font,
            anchor="w",
        )

        self.step_1_button = Button(
            self,
            text="Create examples",
            width=18,
            command=lambda: self.run_create_example_base_inputs(),
        )
        self.step_2_button = Button(
            self,
            text="Blank availability",
            width=18,
            command=lambda: controller.show_frame(BlankAvailabilityScreen.__name__),
        )
        self.step_3_button = Button(
            self,
            text="Blank roster",
            width=18,
            command=lambda: controller.show_frame(BlankRosterScreen.__name__),
        )
        self.step_5_button = Button(
            self,
            text="Allocate crews",
            width=18,
            command=lambda: controller.show_frame(AllocateCrewsScreen.__name__),
        )
        self.step_7_button = Button(
            self,
            text="Individual rosters",
            width=18,
            command=lambda: controller.show_frame(IndividualRostersScreen.__name__),
        )

        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(1, minsize=600)
        self.grid_columnconfigure(3, weight=2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(13, weight=3)

        self.picture.grid(row=1, column=1, padx=5, pady=5, columnspan=2)
        self.intro_label.grid(row=2, column=1, padx=0, pady=15, columnspan=2)
        self.step_1_label.grid(row=3, column=1, sticky="EW", padx=40, pady=0)
        self.step_1a_label.grid(row=4, column=1, sticky="EW", padx=40, pady=0)
        self.step_1b_label.grid(row=5, column=1, sticky="EW", padx=40, pady=0)
        self.step_1c_label.grid(row=6, column=1, sticky="EW", padx=40, pady=0)
        self.step_2_label.grid(row=7, column=1, sticky="EW", padx=40, pady=10)
        self.step_3_label.grid(row=8, column=1, sticky="EW", padx=40, pady=10)
        self.step_4_label.grid(
            row=9, column=1, sticky="EW", padx=40, pady=10, columnspan=2
        )
        self.step_5_label.grid(row=10, column=1, sticky="EW", padx=40, pady=10)
        self.step_6_label.grid(row=11, column=1, sticky="EW", padx=40, pady=10)
        self.step_7_label.grid(row=12, column=1, sticky="EW", padx=40, pady=10)

        self.step_1_button.grid(
            row=3, column=2, sticky="EW", padx=30, pady=0, rowspan=3
        )
        self.step_2_button.grid(row=7, column=2, sticky="EW", padx=30, pady=0)
        self.step_3_button.grid(row=8, column=2, sticky="EW", padx=30, pady=0)
        self.step_5_button.grid(row=10, column=2, sticky="EW", padx=30, pady=0)
        self.step_7_button.grid(row=12, column=2, sticky="EW", padx=30, pady=0)

    @handle_errors
    def run_create_example_base_inputs(self):
        save_location = filedialog.askdirectory(title="Choose a save location")
        if save_location:
            self.controller.show_frame("WaitScreen")
            create_example_base_inputs(save_location)
            self.controller.show_frame("HomeScreen")

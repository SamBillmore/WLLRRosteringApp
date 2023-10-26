from tkinter import Frame
from tkinter import Label
from tkinter import PhotoImage

from user_interface.resource_path import ResourcePath


class WaitScreen(Frame, ResourcePath):
    """Screen for showing during export of files."""

    def __init__(self, parent, controller, background_col, foreground_col, font):
        """Initialise the error screen."""
        Frame.__init__(self, parent, bg=background_col)
        self.controller = controller
        self.parent = parent
        self.picture_path = "src/user_interface/wait_screen_pic.png"

        self.logo = PhotoImage(file=self.resource_path(self.picture_path))

        self.picture = Label(self, image=self.logo)
        self.picture.image = self.logo
        self.polite_label = Label(
            self,
            text="Working to generate your file(s)...",
            bg=background_col,
            fg=foreground_col,
            font=font,
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=3)

        self.picture.grid(row=1, column=1, padx=50, pady=50)
        self.polite_label.grid(row=2, column=1, sticky="W", padx=25, pady=20)

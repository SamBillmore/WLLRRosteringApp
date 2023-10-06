from tkinter import Frame
from tkinter import Button
from tkinter import Label
from tkinter import PhotoImage

from user_interface.resource_path import ResourcePath


class ErrorScreen(Frame, ResourcePath):
    """Screen for showing errors in data import."""

    def __init__(self, parent, controller, background_col, foreground_col, font):
        """Initialise the error screen."""
        Frame.__init__(self, parent, bg=background_col)
        self.controller = controller
        self.parent = parent
        self.picture_path = "src/user_interface/error_screen_pic.png"
        self.logo = PhotoImage(file=self.resource_path(self.picture_path))
        self.picture = Label(self, image=self.logo)
        self.picture.image = self.logo
        self.intro_label = Label(
            self,
            text="There has been an error.",
            bg=background_col,
            fg=foreground_col,
            font=font,
        )
        self.error_label = Label(
            self,
            text="The errors is: ",
            bg=background_col,
            fg=foreground_col,
            font=font,
        )
        self.error_message = Label(
            self, text="", bg=background_col, fg=foreground_col, font=font
        )
        self.back_button = Button(
            self,
            text="Home",
            width=19,
            command=lambda: self.controller.show_frame("HomeScreen"),
        )
        self.picture.grid(row=0, column=0, padx=5, pady=5, columnspan=2)
        self.intro_label.grid(
            row=1, column=0, sticky="W", padx=25, pady=20, columnspan=2
        )
        self.error_label.grid(row=2, column=0, sticky="W", padx=25, pady=0)
        self.error_message.grid(row=3, column=0, sticky="W", padx=25, pady=0)
        self.back_button.grid(row=4, column=0, sticky="W", padx=25, pady=20)

    def display_error_message(self, error_message):
        """Update self.error_message."""
        self.error_message["text"] = error_message

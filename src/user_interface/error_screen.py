from tkinter import Frame
from tkinter import Button
from tkinter import Label
from tkinter import PhotoImage
from tkinter import Text
from tkinter import Scrollbar
from tkinter import END

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
        self.error_message = Text(
            self,
            bg=background_col,
            fg=foreground_col,
            font=font,
            height=2,
            width=80,
        )
        self.error_scrollbar = Scrollbar(self, command=self.error_message.yview)
        self.traceback_label = Label(
            self,
            text="The full traceback is: ",
            bg=background_col,
            fg=foreground_col,
            font=font,
        )
        self.full_traceback = Text(
            self,
            bg=background_col,
            fg=foreground_col,
            font=font,
            height=5,
            width=80,
        )
        self.traceback_scrollbar = Scrollbar(self, command=self.full_traceback.yview)
        self.back_button = Button(
            self,
            text="Home",
            width=19,
            command=lambda: self.controller.show_frame("HomeScreen"),
        )

        self.error_message["yscrollcommand"] = self.error_scrollbar.set
        self.full_traceback["yscrollcommand"] = self.traceback_scrollbar.set

        self.picture.grid(row=0, column=0, padx=5, pady=5, columnspan=2)
        self.intro_label.grid(
            row=1, column=0, sticky="W", padx=25, pady=20, columnspan=2
        )
        self.error_label.grid(row=2, column=0, sticky="W", padx=25, pady=0)
        self.error_message.grid(row=3, column=0, sticky="NESW", padx=25, pady=20)
        self.error_scrollbar.grid(row=3, column=1, sticky="NESW", padx=0, pady=20)
        self.traceback_label.grid(row=4, column=0, sticky="W", padx=25, pady=0)
        self.full_traceback.grid(row=5, column=0, sticky="NESW", padx=25, pady=20)
        self.traceback_scrollbar.grid(row=5, column=1, sticky="NESW", padx=0, pady=20)
        self.back_button.grid(row=6, column=0, sticky="W", padx=25, pady=20)

        self.grid_columnconfigure(0, weight=1)

    def display_error_message(self, error_message):
        """Update self.error_message."""
        self.error_message.delete(1.0, END)
        self.error_message.insert(1.0, error_message)

    def display_full_traceback(self, full_traceback):
        """Update self.error_message."""
        self.full_traceback.delete(1.0, END)
        self.full_traceback.insert(1.0, full_traceback)

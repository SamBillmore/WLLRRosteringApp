from tkinter import Frame
from tkinter import Button
from tkinter import Label
from tkinter import Entry
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox

from blank_availability.create_blank_availability import create_blank_availability
from error_handling.error_handling_decorator import handle_errors


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
            anchor="w",
        )
        self.timetable_label = Label(
            self,
            text="Timetable dates and colours: ",
            bg=background_col,
            fg=foreground_col,
            font=font,
            anchor="w",
        )
        self.timetable_entry = Entry(self)
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

        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(2, minsize=350)
        self.grid_columnconfigure(4, weight=2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=3)

        self.intro_label.grid(
            row=1, column=1, sticky="W", padx=25, pady=20, columnspan=2
        )
        self.timetable_label.grid(row=2, column=1, sticky="W", padx=25, pady=20)
        self.timetable_entry.grid(row=2, column=2, sticky="EW", padx=0, pady=0)
        self.timetable_path.grid(row=2, column=3, sticky="W", padx=5, pady=0)
        self.create_blank_avail_button.grid(
            row=3, column=2, sticky="E", padx=0, pady=15
        )
        self.back_button.grid(row=4, column=1, sticky="W", padx=25, pady=20)

    @handle_errors
    def run_create_blank_availability(self, timetable_path):
        """Creating blank availability forms with optional password protection."""
        save_location = filedialog.asksaveasfilename(
            title="Choose a save location", defaultextension=".xlsx"
        )
        if save_location:
            # Ask user if they want to password protect the file
            use_password = messagebox.askyesno(
                "Password Protection", "Do you want to password protect the file?"
            )

            password = None
            if use_password:
                while password is None:
                    password_1 = simpledialog.askstring(
                        "Password", "Enter password for file protection:", show="*"
                    )
                    if password_1 is None:
                        messagebox.showinfo(
                            "Cancelled",
                            "Password protection cancelled. File will not be password "
                            "protected.",
                        )
                        password = None
                        break
                    password_2 = simpledialog.askstring(
                        "Password", "Re-enter password for file protection:", show="*"
                    )
                    if password_1 == password_2:
                        password = password_1
                    else:
                        messagebox.showerror("Password Error", "Passwords do not match")
            self.controller.show_frame("WaitScreen")
            create_blank_availability(timetable_path, save_location, password=password)
            self.controller.show_frame("HomeScreen")

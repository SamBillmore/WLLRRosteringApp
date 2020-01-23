import tkinter as tk
from tkinter import Button
from tkinter import Label
import os

class ErrorScreen(tk.Frame):
    """
    Screen for showing errors in data import
    """
    
    def __init__(self, parent, controller, background_col, foreground_col, font):
        """
        Initialise the error screen
        """
        tk.Frame.__init__(self, parent, bg=background_col)
        self.controller = controller
        self.parent = parent

        self.intro_label = Label (self, text='There has been an error with one of the files imported.', bg=background_col, fg=foreground_col, font=font)
        self.filepath_label = Label (self, text='The file with errors is: ', bg=background_col, fg=foreground_col, font=font)
        self.expected_columns_label = Label (self, text='The expected columns are: ', bg=background_col, fg=foreground_col, font=font)
        self.error_filepath_label = Label (self, text='', bg=background_col, fg=foreground_col, font=font)
        self.error_expected_columns_label = Label (self, text='', bg=background_col, fg=foreground_col, font=font)
        self.back_button = Button (self, text='Back', width=19, command=lambda: self.controller.show_frame('HomeScreen'))

        self.intro_label.grid(row=0, column=0, sticky='W', padx=25, pady=20, columnspan=2)
        self.filepath_label.grid(row=1, column=0, sticky='W', padx=25, pady=0)
        self.expected_columns_label.grid(row=2, column=0, sticky='W', padx=25, pady=0)
        self.error_filepath_label.grid(row=1, column=1, sticky='W', padx=25, pady=0)
        self.error_expected_columns_label.grid(row=2, column=1, sticky='W', padx=25, pady=0)
        self.back_button.grid(row=3, column=0, sticky='W', padx=25, pady = 20)

    def update_error_messages(self,error_filepath,error_expected_columns):
        """
        Update self.error_filepath_label and self.error_expected_columns_label
        """
        error_filename = os.path.basename(error_filepath)
        self.error_filepath_label['text'] = error_filename
        self.error_expected_columns_label['text'] = list(error_expected_columns.keys())

class ErrorScreenExport(tk.Frame):
    """
    Screen for showing errors in data export
    """
    
    def __init__(self, parent, controller, background_col, foreground_col, font):
        """
        Initialise the error screen
        """
        tk.Frame.__init__(self, parent, bg=background_col)
        self.controller = controller
        self.parent = parent

        self.intro_label = Label (self, text='There has been an error with the creation of your file.', bg=background_col, fg=foreground_col, font=font)
        self.error_message_label = Label (self, text='Please ensure you do not have the file open, then try again.', bg=background_col, fg=foreground_col, font=font)
        self.back_button = Button (self, text='Back', width=19, command=lambda: self.controller.show_frame('HomeScreen'))

        self.intro_label.grid(row=0, column=0, sticky='W', padx=25, pady=20, columnspan=2)
        self.error_message_label.grid(row=1, column=0, sticky='W', padx=25, pady=0)
        self.back_button.grid(row=2, column=0, sticky='W', padx=25, pady = 20)
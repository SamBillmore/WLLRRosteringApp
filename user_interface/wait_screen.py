import tkinter as tk
from tkinter import Label

class WaitScreen(tk.Frame):
    """
    Screen for showing during export of files
    """
    
    def __init__(self, parent, controller, background_col, foreground_col, font):
        """
        Initialise the error screen
        """
        tk.Frame.__init__(self, parent, bg=background_col)
        self.controller = controller
        self.parent = parent

        self.polite_label = Label (self, text='Working to generate your file(s)...', bg=background_col, fg=foreground_col, font=font)

        self.polite_label.grid(row=0, column=0, sticky='W', padx=25, pady=20, columnspan=2)
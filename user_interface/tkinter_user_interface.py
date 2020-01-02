import tkinter as tk
from tkinter import Button
from tkinter import Label
from tkinter import filedialog
from tkinter import PhotoImage
from functools import partial
import os

class App(tk.Tk):
    """
    Overall container for app
    Individual screens are raised within this container
    """

    def __init__(self):
        """
        Initialise the class
        """
        tk.Tk.__init__(self)

        self.title('WLLR footplate crew rostering program')
        self.geometry('850x600+250+100')
        self.frame_names_list = (WelcomeScreen,ProgressBar)
        self.frames = {}
        self.background_col = 'black'
        self.foreground_col = 'white'
        self.font = 'courier 11'

        # the container is where we'll stack our frames on top of each other, then the one we want visible will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create each frame instance and add to self.frames dictionary
        for frame_name in self.frame_names_list:
            page_name = frame_name.__name__
            frame_object = frame_name(parent=container, controller=self, background_col = self.background_col, foreground_col = self.foreground_col, font = self.font)
            self.frames[page_name] = frame_object

            # put all of the pages in the same location;
            # the one on the top of the stacking order will be the one that is visible.
            frame_object.grid(row=0, column=0, sticky="nsew")

        self.show_frame(self.frame_names_list[0].__name__)

    def show_frame(self, page_name):
        """
        Show a frame for the given page name
        """
        frame = self.frames[page_name]
        frame.tkraise()

class WelcomeScreen(tk.Frame):
    """
    The first screen for the program
    """

    def __init__(self, parent, controller, background_col, foreground_col, font):
        """
        Initialise the welcome screen
        """
        tk.Frame.__init__(self, parent, bg=background_col)
        self.controller = controller
        self.parent = parent
        self.picture_path = './/user_interface//welcome_screen_pic.png'

        logo = PhotoImage(file=self.resource_path(self.picture_path))

        label_0 = Label (self, image=logo)
        label_0.image = logo
        label_1 = Label (self, text='Welcome to the WLLR footplate department rostering program!', bg=background_col, fg=foreground_col, font=font)
        label_2 = Label (self, text='Step 1: Set up input files', bg=background_col, fg=foreground_col, font=font)
        label_3 = Label (self, text='\t(1) timetable dates and colours', bg=background_col, fg=foreground_col, font=font)
        label_4 = Label (self, text='\t(2) crew requirements for each colour timetable', bg=background_col, fg=foreground_col, font=font)
        label_5 = Label (self, text='Step 2: Create blank availability forms', bg=background_col, fg=foreground_col, font=font)
        label_6 = Label (self, text='Step 3: Create a blank roster', bg=background_col, fg=foreground_col, font=font)
        label_7 = Label (self, text='Step 4: Open blank roster file and enter any specific crew allocations', bg=background_col, fg=foreground_col, font=font)
        label_8 = Label (self, text='Step 5: Allocate crews to remaining turns', bg=background_col, fg=foreground_col, font=font)
        label_9 = Label (self, text='Step 5a: Create availability summary', bg=background_col, fg=foreground_col, font=font)
        label_10 = Label (self, text='Step 6: Review allocations and amend as necessary', bg=background_col, fg=foreground_col, font=font)
        label_11 = Label (self, text='Step 7: Generate individual rosters', bg=background_col, fg=foreground_col, font=font)

        button_5 = Button (self, text='Blank availability', width=18)
        button_6 = Button (self, text='Blank roster', width=18)
        button_8 = Button (self, text='Allocate crews', width=18)
        button_9 = Button (self, text='Availability summary', width=18)
        button_11 = Button (self, text='Individual rosters', width=18)

        self.grid(row=0, column=0, sticky='W')
        
        label_0.grid(row=0, column=0, padx = 5, pady = 5, columnspan=2)
        label_1.grid(row=1, column=0, padx = 25, pady = 15, columnspan=2)
        label_2.grid(row=2, column=0, sticky='W', padx = 25, pady = 0)
        label_3.grid(row=3, column=0, sticky='W', padx = 25, pady = 0)
        label_4.grid(row=4, column=0, sticky='W', padx = 25, pady = 0)
        label_5.grid(row=5, column=0, sticky='W', padx = 25, pady = 15)
        label_6.grid(row=6, column=0, sticky='W', padx = 25, pady = 10)
        label_7.grid(row=7, column=0, sticky='W', padx = 25, pady = 10)
        label_8.grid(row=8, column=0, sticky='W', padx = 25, pady = 10)
        label_9.grid(row=9, column=0, sticky='W', padx = 25, pady = 10)
        label_10.grid(row=10, column=0, sticky='W', padx = 25, pady = 10)
        label_11.grid(row=11, column=0, sticky='W', padx = 25, pady = 10)

        button_5.grid(row=5,column=1,sticky='W')
        button_6.grid(row=6,column=1,sticky='W')
        button_8.grid(row=8,column=1,sticky='W')
        button_9.grid(row=9,column=1,sticky='W')
        button_11.grid(row=11,column=1,sticky='W')

    def resource_path(self, relative_path):
        """
        Create full filepath to picture
        """
        base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

class ProgressBar(tk.Frame):

    def __init__(self, parent, controller, background_col, foreground_col, font):
        tk.Frame.__init__(self, parent, bg=background_col)
        self.controller = controller
        self.parent = parent
        self.foreground_col = foreground_col
        self.font = font

        header_label = tk.Label(self, text="Progress: ")
        
        self.progress_bar_var = tk.DoubleVar()
        self.progress_bar_var.set(0)
        # progress_bar = ttk.Progressbar(self, orient='horizontal', length=350, variable=self.progress_bar_var, mode='determinate')

        header_label.grid(row=0, column=0, sticky='W')
        # progress_bar.grid(row=1, column=1)
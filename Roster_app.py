
# To do
# Complete - 0. Refactor code into modules
# Complete - 1. Date formats for output sheets 
# Complete - 2. Autofit columns function for outputs
# Complete - 3. Create master function to call method for master availability
# To test - 4. Complete method 'allocate_turns()'
# Complete - Check whether code needs refactoring
# Complete - Refactor removing person from working_availability and adding point to points_tally
# Complete - 5. Create individual rosters and print to pdf
# Complete - Move print to pdf to import_export
# Complete - Check Crew requirements - should be in blank roster?
# Complete - 6. Error checking for imports
# Complete - 7. Create user interface
# 8. Split user interface into multiple files

from user_interface.tkinter_user_interface import App

def main():
    """
    Main function for app
    """
    app = App()
    app.mainloop()

if __name__ =='__main__':
    main()
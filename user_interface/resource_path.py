import os
import sys

class ResourcePath():
    """
    Parent class to hold methods for importing resources to screens in the user interface
    """

    def __init__(self):
        """
        Initiate class
        """
        pass

    def resource_path(self, relative_path):
        """
        Create full filepath to picture
        """
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        else:
            base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)
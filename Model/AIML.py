from Model.Topics import Topics
from Model.Categories import Categories
from Model.Common import indentation
from textwrap import indent
from Model.Common import debugging

class AIML():

    def __init__(self, name = ""):
        self.name = name
        self.topics = Topics()
        self.categories = Categories()

    def __str__(self):
        output = "<?xml version=\"1.0\" encoding=\"UTF-8\"?> \n<aiml>"
        if debugging:
            output = "[AIML: " + self.name + "]\n"
            output += "[General Categories:]\n"
            output += indent(str(self.categories), indentation)
        else:
            output += str(self.categories) # No need for indentation
        output += str(self.topics)
        output += "</aiml>\n"
        return output
    
    def __enter__(self): # used for the "with" keyword
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # make sure the dbconnection gets closed
        pass
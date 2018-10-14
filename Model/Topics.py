from Model.Categories import Categories
from textwrap import indent
from Model.Common import indentation
from Model.Common import debugging

class Topic():

    def __init__(self, name=""):
        self.name = name
        self.categories = Categories()

    def __str__(self):
        output = "<topic name=\""+self.name+"\">\n"
        output += indent(str(self.categories), indentation)
        output += "</topic>\n"
        return output
    
    def __enter__(self): # used for the "with" keyword
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # make sure the dbconnection gets closed
        pass

class Topics():

    def __init__(self):
        self.topics = {}
        self.current = 0

    def __iter__(self):
        self.current = 0
        return self

    def __next__(self): 
        if self.current >= len(self.topics):
            raise StopIteration
        else:
            self.current += 1
            return self.topics[list(self.topics.keys())[self.current-1]]
    
    def append(self, topic: Topic):
        self.topics[topic.name] = topic

    def find(self, name) -> Topic:
        return self.topics[name]

    def __str__(self):
        output = ""
        for topic_name in list(self.topics.keys()):
            output += str(self.topics[topic_name])
        if debugging:
            output = "[topics:]\n" + indent(output, indentation)
        else:
            pass # There is no need to indent it anymore
        return output

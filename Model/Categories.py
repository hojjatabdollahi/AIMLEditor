import uuid
from textwrap import indent
from Model.Common import indentation
from Model.Common import debugging

class Category():
    
    def __init__(self, template="", that = "", parents = [], chilldren = []):
        self.id = uuid.uuid4()
        self.template = template
        self.that = that
        self.parents = parents
        self.children = chilldren
    
    def __str__(self):
        
        body = ""
        if self.that != "":
            body += "<that>\n"
            body += indent(self.that+"\n", indentation)
            body += "</that>\n"    
        if self.template != "":
            body += "<template>\n"
            body += indent(self.template+"\n", indentation)
            body += "</template>\n"
        output = "<category>\n"
        output += indent(body, indentation)
        output += "</category>\n"
        if debugging:
            output = "[category: " + str(self.id) + "]\n" + output
        return output

class Categories():

    def __init__(self):
        self.categories = {}
        self.current = 0

    def __iter__(self):
        self.current = 0
        return self

    def __next__(self):
        if self.current >= len(self.categories):
            raise StopIteration
        else:
            self.current += 1
            return self.categories[list(self.categories.keys())[self.current-1]]
    
    def append(self, category: Category):
        self.categories[category.id] = category

    def find(self, id):
        return self.categories[id]

    def __str__(self):
        output = ""
        for cat_name in list(self.categories.keys()):
            output += str(self.categories[cat_name])
        if debugging:
            output = "[Categories:]\n" + indent(output, indentation)
        else:
            pass # There is no need to indent the output anymore.
        return output

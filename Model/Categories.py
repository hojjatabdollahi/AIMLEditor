import uuid
from textwrap import indent
from Model.Common import indentation
from Model.Common import debugging
from Utils.Funtions import de_punctuate

class Category():
    
    def __init__(self, pattern="", template="", that = "", parents = [], chilldren = []):
        self.id = uuid.uuid4()
        self.pattern = pattern
        self.template = template
        self.that = de_punctuate(that)
        self.parents = parents
        self.children = chilldren

    def __str__(self):
        
        body = ""
        if self.pattern != "":
            body += "<pattern>\n"
            body += indent(self.pattern+"\n", indentation)
            body += "</pattern>\n" 
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
            output = "[category: " + str(self.id) + "]\nParents: " + str(self.parents) + "\nChildren: " + str(self.children)+"\n" + output
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
    
    

    def check_parents_sanity(self, child: Category) -> bool:
        if len(child.parents) == 0: # make sure the links are sane
            if debugging:
                print("child: " + child.id + " is sane")
            return True
        else:
            for parent_id in child.parents:
                parent = self.find(parent_id)
                if child.that not in de_punctuate(parent.template):
                    if debugging:
                        print("child: " + child.id + " is insane")
                    return False
            return True

    def append(self, category: Category) -> bool:

        # if self.categories.__contains__ category then throw and error otherwise add it the categories
        if category.id in self.categories:
            raise Exception("Category already exists!")

        if not self.check_parents_sanity(category):
            return False # Do not append, because it is insane
        for parent_id in category.parents:
            if category.id not in self.find(parent_id).children:
                self.find(parent_id).children.append(category.id) # add to the parents
        
        self.categories[category.id] = category
        return category.id

        # TODO: Sanity: sanity of the whole project (we can call that after importing)

        # if len(category.children) != 0: # make sure the links are sane
        #     for child_id in category.children:
        #         if category.id not in self.find(child_id).parents:
        #             self.find(child_id).parents.append(category.id)

    def find(self, id) -> Category:
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

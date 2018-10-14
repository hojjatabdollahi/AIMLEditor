
from Model.AIML import AIML
from Model.Categories import Category
from Model.Topics import Topic
import Utils.Storage as Storage
import xml.etree.ElementTree as ET


with AIML(name="hojjat aiml") as aiml:
    aiml.categories.append(Category(template="nice to see you again. how are you?"))
    aiml.categories.append(Category(template="I'm happy that you are well."))
    aiml.categories.append(Category(template="I'm sad that you are not well."))
    with Topic("sports") as sports:
        sports.categories.append(Category(template="Sure, let's talk about sports. What sport do you like?"))
        sports.categories.append(Category(template="I like football too."))
        sports.categories.append(Category(template="I like baseball better."))
        aiml.topics.append(sports)
    with Topic("arts") as arts:
        arts.categories.append(Category(template="Sure, let's talk about arts. What art do you like?"))
        arts.categories.append(Category(template="I like painting too."))
        arts.categories.append(Category(template="I like music better."))
        aiml.topics.append(arts)
Storage.save('test', aiml)
aiml2 = Storage.restore('test')
assert isinstance(aiml2, AIML) # for intellisense purposes
print(aiml2) 
Storage.export('test', aiml2)
xml = str(aiml)
root = ET.fromstring(country_data_as_string)


tree = ET.parse("test.aiml")
root = tree.getroot()
for child in root:
    print(child.tag, child.attrib)




#!! How to cast the output of a function so that we can use intellisense: use:  -> after the funciton declaration
#!! How to indent the output of __str__ by some fixed amount: use: textwrap.indent (it's for python3.3 after)
#!! How to send falgs to __str__ so, to print some extra (verbose) or not
#!!      or, how to have a global Verbose (Debug) tag in python: I used a variable in the Common.py
#!! How to add everything from a folder: use: from x import *

#!! How to save and restore? (Actually, how to serialize?): use: pickle
#?? Exporting is easy, but can we import?




# cats = Categories()
# cats.append(Category(template="t1"))
# cats.append(Category(template="t2"))
# cats.append(Category(template="t3"))
# import copy
# cats2 = copy.copy(cats)
# for cat in cats:
#     print(cat.template)
#     for cat2 in cats2:
#         print(cat2.template)
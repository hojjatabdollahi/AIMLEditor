from Model.AIML import AIML
import pickle
from Model.Categories import Category
from Model.Topics import Topic
import xml.etree.ElementTree as ET


def save(filename,aiml):
    with open(filename+'.aib', 'wb') as output:
        pickle.dump(aiml, output, pickle.HIGHEST_PROTOCOL)

def restore(filename) -> AIML:
    with open('test.aib', 'rb') as input:
       aiml2 = pickle.load(input)
    return aiml2

def exportAIML(filename, aiml):
    with open(filename+'.aiml', 'w') as output:
        output.write(str(aiml))

def decode_tag(child):
    pattern = ""
    template = ""
    that = ""
    try:
        pattern = child.find("pattern").text.strip()
    except:
        pass
    try:
        template = child.find("template").text.strip()
    except:
        pass
    try:
        that = child.find("that").text.strip()
    except:
        pass
    return pattern, template, that


def recursive_decoding(head, tag): # head is the object that we are adding the categories to (either a topic, or the general aiml)
    for child in tag:
        if child.tag == "category":
            pattern, template, that = decode_tag(child)
            head.categories.append(Category(pattern=pattern, template=template, that=that))
        if child.tag == "topic":
            topic = Topic(child.attrib["name"])
            head.topics.append(topic)
            recursive_decoding(topic, child)

def importAIML(filename) -> AIML:
    tree = ET.parse(filename+".aiml")
    root = tree.getroot()
    aiml3 = None
    if root.tag != "aiml":
        print("This is not an AIML file.")
    else:
        aiml3 =  AIML(name="hojjat aiml")
        recursive_decoding(aiml3, root)
    return aiml3
# xml = str(aiml)
# root = ET.fromstring(country_data_as_string)
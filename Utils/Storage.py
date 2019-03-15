import pickle
import xml.etree.ElementTree as ET
from Model.Data import *
from PyQt5.QtWidgets import QErrorMessage


def handleError(error):
    em = QErrorMessage.qtHandler()
    em.showMessage(str(error))


def save(filename, aiml):
    try:
        with open(filename+'.aib', 'wb') as output:
            pickle.dump(aiml, output, pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        handleError(ex)
        print("exception caught!")
        print(ex)


def restore(filename):
    try:
        with open(filename+'.aib', 'rb') as input_file:
            aiml2 = pickle.load(input_file)
        return aiml2
    except Exception as ex:
        handleError(ex)
        print("exception caught!")
        print(ex)


def exportAIML(filename, aiml):
    try:
        with open(filename+'.aiml', 'w') as output:
            output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            output.write(str(aiml))
    except Exception as ex:
        handleError(ex)
        print("exception caught!")
        print(ex)


tag_list = {"aiml": AIML,
            "topic": Topic,
            "category": Category,
            "pattern": Pattern,
            "template": Template,
            "condition": Condition,
            "li": ConditionItem,
            "random": Random,
            "set": Set,
            "think": Think,
            "that": That,
            "oob": Oob,
            "robot": Robot,
            "options": Options,
            "option": Option,
            "image": Image,
            "video": Video,
            "filename": Filename}


def decode_tag(tag_type):
    if tag_type in tag_list:
        return tag_list[tag_type]()
    return False


# head is the object that we are adding the categories to (either a topic, or the general aiml)
def recursive_decoding(head, tag_xml):
    try:
        for child in tag_xml:
            tag_obj = decode_tag(child.tag.lower())
            if(tag_obj != False):
                if child.text:
                    if child.text.strip():
                        tag_obj.append(child.text.strip())
                tag_obj.attrib = child.attrib
                try:
                    head.append(tag_obj)
                except Exception as ex:
                    print(ex)
                if child.tail:
                    if child.tail.strip():
                        head.append(child.tail.strip()) #TODO: remove the extra whitespaces in the text
            else:
                head.append(ET.tostring(child, encoding="unicode"))
            recursive_decoding(tag_obj, child)
    except Exception as ex:
        handleError(ex)
        print(ex)


def importAIML(filename):
    print("parsing file into tree")
    try:
        tree = ET.parse(filename+".aiml")
        print("getting root of the tree")
        root = tree.getroot()
        aiml3 = None
        if root.tag.lower() != "aiml":
            print("This is not an AIML file.")
            print(root.tag)
        else:
            aiml3 = AIML()
            print("decoding file")
            recursive_decoding(aiml3, root)
        return aiml3
    except Exception as ex:
        handleError(ex)
        print("exception caught in import of file (storage)!")
        print(ex)

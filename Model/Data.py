from textwrap import indent
import Utils.Storage as Storage
import xml.etree.ElementTree as ET

class Tag():
    def __init__(self, type, acceptable_tags=[], attrib = {}):
        self.type = type
        self.tags = []
        self.acceptable_tags = acceptable_tags
        self.attrib = attrib
    
    def append(self, tag):
        if type(tag) in self.acceptable_tags:
            self.tags.append(tag)
            return self
        raise Exception("Type: " + str(type(tag)) + " not allowed in " + self.type)
    
    def setAttrib(self, attrib):
        self.attrib = attrib

    def __str__(self):
        attrib = (' ' + ' '.join('{}=\"{}\"'.format(
            key, val) for key, val in self.attrib.items())) if len(self.attrib) > 0 else ""
        if len(self.tags) > 1:
            tags = '\n' + indent('\n'.join(map(str, self.tags)), "    ") + '\n'
        elif len(self.tags) > 0:
            tags = '\n'.join(map(str, self.tags))
        else:
            tags = ""
        return "<{}{}>{}</{}>".format(str(self.type), attrib, tags , str(self.type))

class AIML(Tag):
    def __init__(self):
        super().__init__("AIML", acceptable_tags=[Category, Topic])

class Topic(Tag):
    def __init__(self, name=""):
        if name != "":
            super().__init__("Topic", acceptable_tags=[Category], attrib={'name':name})
        else:
            super().__init__("Topic", acceptable_tags=[Category])

class Category(Tag):
    def __init__(self):
        super().__init__("Category", acceptable_tags=[Pattern, Template, Think])

class Pattern(Tag):
    def __init__(self):
        super().__init__("Pattern", acceptable_tags=[str])

class Template(Tag):
    def __init__(self):
        super().__init__("Template", acceptable_tags=[Think, Condition, Oob, str])

class Condition(Tag):
    def __init__(self, name=""):
        if name!="":
            super().__init__("Condition", attrib={"name":name}, acceptable_tags={ConditionItem})
        else:
            super().__init__("Condition", acceptable_tags={ConditionItem})

class ConditionItem(Tag):
    def __init__(self, value=""):
        if value!="":
            super().__init__("li", attrib={"value":value}, acceptable_tags=[Oob, str])
        else:
            super().__init__("li", acceptable_tags=[Oob, str])

class Set(Tag):
    def __init__(self, name=""):
        if name!="":
            super().__init__("Set", attrib={'name':name}, acceptable_tags=[str])
        else:
            super().__init__("Set", acceptable_tags=[str])

class Think(Tag):
    def __init__(self):
        super().__init__("Think", acceptable_tags=[Set, str])

class Oob(Tag):
    def __init__(self):
        super().__init__("Oob", acceptable_tags=[Robot])

class Robot(Tag):
    def __init__(self):
        super().__init__("Robot", acceptable_tags=[Options])

class Options(Tag):
    def __init__(self):
        super().__init__("Options", acceptable_tags=[Option])
        
class Option(Tag):
    def __init__(self, value=""):
        if value != "":
            super().__init__("Option", acceptable_tags=[str])
            super().append(value)
        else:
            super().__init__("Option", acceptable_tags=[str])

aiml = AIML().append(
    Category().append(
        Pattern().append("START SESSION 1 *")
        ).append(
            Template().append(
                Think().append(
                    Set("username").append("star")
                ).append(
                    Set("topic").append("Session 1")
                )
            ).append("Ok. Let's begin our session. How are you doing today <star/>?").append(
                Oob().append(Robot())
            )
        )
        ).append(
            Topic("session").append(
                Category().append(
                    Pattern().append("*")
                ).append(
                    Template().append(
                        Think().append(Set("data").append("<star/>"))
                    ).append(
                        Condition("getsetimnet").append(
                            ConditionItem("verypositive").append("I am happy").append(
                                Oob().append(
                                    Robot().append(
                                        Options().append(
                                            Option("Yes")
                                        ).append(
                                            Option("No")
                                        )
                                    )
                                )
                            )
                        ).append(
                            ConditionItem("positive").append("I am not as happy")
                        )
                    )
                )
            )
        )
print(aiml)



tag_list = {"category": Category,
            "aiml": AIML,
            "topic": Topic,
            "category": Category,
            "pattern": Pattern,
            "template": Template,
            "condition": Condition,
            "li": ConditionItem,
            "set": Set,
            "think": Think,
            "oob": Oob,
            "robot": Robot,
            "options": Options,
            "option": Option}

def decode_tag(tag_type):
    if tag_type in tag_list:
        return tag_list[tag_type]()
    return False


def recursive_decoding(head, tag_xml): # head is the object that we are adding the categories to (either a topic, or the general aiml)
    for child in tag_xml:
        tag_obj = decode_tag(child.tag.lower())
        if(tag_obj!=False):
            if child.text:
                if child.text.strip():
                    tag_obj.append(child.text.strip())
            tag_obj.attrib = child.attrib
            head.append(tag_obj)
            if child.tail:
                if child.tail.strip():
                    head.append(child.tail.strip())
        else:
            head.append(ET.tostring(child, encoding="unicode"))
        recursive_decoding(tag_obj, child)


def importAIML(filename):
    tree = ET.parse(filename+".aiml")
    root = tree.getroot()
    aiml3 = None
    if root.tag.lower() != "aiml":
        print("This is not an AIML file.")
        print(root.tag)
    else:
        aiml3 =  AIML()
        recursive_decoding(aiml3, root)
    return aiml3


# Storage.save('test2', aiml)
aiml2 = Storage.restore('test2')
assert isinstance(aiml2, AIML) # for intellisense purposes
print(aiml2) 
Storage.exportAIML('test2', aiml2)
aiml4 = importAIML('test2')
print(aiml4)
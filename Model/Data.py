from textwrap import indent
import xml.etree.ElementTree as ET
import Model.Common as Common
from PyQt5.QtCore import QUuid


class Tag():
    def __init__(self, type, acceptable_tags=[], attrib={}):
        self.type = type
        self.tags = []
        self.acceptable_tags = acceptable_tags
        self.attrib = attrib

    def append(self, tag):
        if type(tag) in self.acceptable_tags:
            self.tags.append(tag)
            return self
        raise Exception("Type: " + str(type(tag)) +
                        " not allowed in " + self.type)

    def setAttrib(self, attrib):
        self.attrib = attrib

    def find(self, id):
        print("trying to find category with id of " + str(id))
        if id is None:
            print("Bad id, id was never generated and is currently null")
            return None

        for cat in self.tags:
            if cat.type == "category":
                if cat.id == id:
                    return cat
            else:
                print("tag type: " + cat.type)

        print("No category found")
        return None

    def update(self, newCat):
        if id is None:
            print("Bad id, id was never generated and is currently null")
            return None

        index = 0
        for cat in self.tags:
            if cat.type == "category":
                if cat.id == newCat.id:
                    self.tags[index] = newCat
                    # cat = newCat
                    return cat
            else:
                print("tag type: " + cat.type)
            index = index + 1

        print("No category found with id of: " + newCat.id)
        return None

    """Finds first occurrence of Tag, type, in array tags of Parent Tag"""
    def findTag(self, type):
        if self.tags is None:
            print("This tag has no child tags")
            return None

        for child in self.tags:
            if child.type == type:
                return child

        return None

    def __str__(self):
        attrib = (' ' + ' '.join('{}=\"{}\"'.format(
            key, val) for key, val in self.attrib.items())) if len(self.attrib) > 0 else ""
        if len(self.tags) > 1:
            tags = '\n' + indent('\n'.join(map(str, self.tags)),
                                 Common.indentation) + '\n'
        elif len(self.tags) > 0:
            tags = '\n'.join(map(str, self.tags))
        else:
            tags = ""
        return "<{}{}>{}</{}>".format(str(self.type), attrib, tags, str(self.type))


class AIML(Tag):
    def __init__(self, version="2.0"):
        super().__init__("aiml", acceptable_tags=[Category, Topic], attrib={'version': version})


class Topic(Tag):
    def __init__(self, name=""):
        if name != "":
            super().__init__("topic", acceptable_tags=[
                Category], attrib={'name': name})
        else:
            super().__init__("topic", acceptable_tags=[Category])


class Category(Tag):
    def __init__(self, id=""):
        super().__init__("category", acceptable_tags=[
            Pattern, Template, Think, That])
        # id to distinguish categories within an AIML object
        self.id = id


class Pattern(Tag):
    def __init__(self):
        super().__init__("pattern", acceptable_tags=[Set, str])


class Template(Tag):
    def __init__(self):
        super().__init__("template", acceptable_tags=[
            Set, Think, Condition, Oob, Random, str])


class That(Tag):
    def __init__(self):
        super().__init__("that", acceptable_tags=[str])


class Random(Tag):
    def __init__(self):
        super().__init__("random", acceptable_tags=[ConditionItem, Oob])


class Condition(Tag):
    def __init__(self, name=""):
        if name != "":
            super().__init__("condition", attrib={
                "name": name}, acceptable_tags={ConditionItem})
        else:
            super().__init__("condition", acceptable_tags={ConditionItem})


class ConditionItem(Tag):
    def __init__(self, value=""):
        if value != "":
            super().__init__("li", attrib={
                "value": value}, acceptable_tags=[Oob, Set, str])
        else:
            super().__init__("li", acceptable_tags=[Oob, Set, str])


class Set(Tag):
    def __init__(self, name=""):
        if name != "":
            super().__init__("set", attrib={
                'name': name}, acceptable_tags=[str])
        else:
            super().__init__("set", acceptable_tags=[str])


class Think(Tag):
    def __init__(self):
        super().__init__("think", acceptable_tags=[Set, str])


class Oob(Tag):
    def __init__(self):
        super().__init__("oob", acceptable_tags=[Robot])


class Robot(Tag):
    def __init__(self):
        super().__init__("robot", acceptable_tags=[Options, Video, Image])


class Options(Tag):
    def __init__(self):
        super().__init__("options", acceptable_tags=[Option])


class Option(Tag):
    def __init__(self, value=""):
        if value != "":
            super().__init__("option", acceptable_tags=[str])
            super().append(value)
        else:
            super().__init__("option", acceptable_tags=[str])


class Video(Tag):
    def __init__(self):
        super().__init__("video", acceptable_tags=[Filename])


class Image(Tag):
    def __init__(self):
        super().__init__("image", acceptable_tags=[Filename])


class Filename(Tag):
    def __init__(self):
        super().__init__("filename", acceptable_tags=[str])
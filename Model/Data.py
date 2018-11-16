from textwrap import indent
import xml.etree.ElementTree as ET
import Model.Common as Common


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
    def __init__(self):
        super().__init__("AIML", acceptable_tags=[Category, Topic])


class Topic(Tag):
    def __init__(self, name=""):
        if name != "":
            super().__init__("Topic", acceptable_tags=[
                Category], attrib={'name': name})
        else:
            super().__init__("Topic", acceptable_tags=[Category])


class Category(Tag):
    def __init__(self):
        super().__init__("Category", acceptable_tags=[
            Pattern, Template, Think])


class Pattern(Tag):
    def __init__(self):
        super().__init__("Pattern", acceptable_tags=[str])


class Template(Tag):
    def __init__(self):
        super().__init__("Template", acceptable_tags=[
            Think, Condition, Oob, str])


class Condition(Tag):
    def __init__(self, name=""):
        if name != "":
            super().__init__("Condition", attrib={
                "name": name}, acceptable_tags={ConditionItem})
        else:
            super().__init__("Condition", acceptable_tags={ConditionItem})


class ConditionItem(Tag):
    def __init__(self, value=""):
        if value != "":
            super().__init__("li", attrib={
                "value": value}, acceptable_tags=[Oob, str])
        else:
            super().__init__("li", acceptable_tags=[Oob, str])


class Set(Tag):
    def __init__(self, name=""):
        if name != "":
            super().__init__("Set", attrib={
                'name': name}, acceptable_tags=[str])
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

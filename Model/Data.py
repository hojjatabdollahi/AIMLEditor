
from textwrap import indent

class Tag():
    def __init__(self, type, acceptable_tags=[], attrib = {}):
        self.type = type
        self.tags = []
        self.acceptable_tags = acceptable_tags
    
    def append(self, tag):
        if type(tag) in self.acceptable_tags:
            self.tags.append(tag)
            return self
        raise Exception("This type os tag is not allowed")
    
    def __str__(self):
        # TODO: Print the attribs
        return "<{}>\n{}\n</{}>".format(str(self.type), indent('\n'.join(map(str, self.tags)), "    "), str(self.type))

class AIML(Tag):
    def __init__(self):
        super().__init__("AIML", acceptable_tags=[Category])
   
class Category(Tag):
    def __init__(self):
        super().__init__("Category", acceptable_tags=[Pattern, Template, Think])

class Pattern(Tag):
    def __init__(self):
        super().__init__("Pattern", acceptable_tags=[str])

class Template(Tag):
    def __init__(self):
        super().__init__("Template", acceptable_tags=[Think, Condition, str])

class Condition(Tag):
    def __init__(self, name):
        super().__init__("Condition", attrib={"name":name}, acceptable_tags={ConditionItem})

class ConditionItem(Tag):
    def __init__(self, value):
        super().__init__("li", attrib={"value":value}, acceptable_tags=[str])    
    def add_item(self, value, tag):
        self.value = value
        self.tag = tag
        return self

class Think(Tag):
    def __init__(self):
        super().__init__("Think", acceptable_tags=[str])

aiml = AIML().append(
    Category().append(
        Pattern().append("START SESSION 1 *")
        ).append(
            Template().append(
                Think().append("set stuff")
            )
        )
        ).append(
            Category().append(
                Pattern().append("*")
            ).append(
                Template().append(
                    Think().append("set data")
                ).append(
                    Condition("getsetimnet").append(
                        ConditionItem("verypositive").append("I am happy")
                    ).append(
                        ConditionItem("positive").append("I am not as happy")
                    )
                )
            )
        )
print(aiml)


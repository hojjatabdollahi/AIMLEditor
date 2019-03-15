class RandomHTML():
    def __init__(self):
        super().__init__()
        self.table = ""

        self.initIcon()

    def initIcon(self):
        self.table = "<table name=\"random\" border=\"1\">" \
                         "<tr>" \
                            "<th>Random Responses</th>" \
                         "</tr>" \
                     "</table>"

    """
    Appends an additional row to the end of random table
    """
    def appendConItem(self, resp):
        print("appending an extra row")
        myStr = "</tr>"
        stringIndex = self.table.rfind(myStr) + 5  # looking for last occurrence of </tr> and placing cursor after it
        conItem = "<tr>" \
                  "<td>{0}</td>" \
                  "</tr>".format(resp)

        self.table = self.table[:stringIndex] + conItem + self.table[stringIndex:]
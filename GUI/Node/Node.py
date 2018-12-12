from collections import OrderedDict
from GUI.Node.Utils.Serializable import Serializable
from GUI.Node.QDM.GraphicsNode import QDMGraphicsNode
from GUI.Node.QDM.ContentWidget import QDMNodeContentWidget
from GUI.Node.Utils.Socket import *
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QObject
from Model.Data import *
from GUI import EditorWidget

DEBUG = False


class Node(Serializable):
    def __init__(self, scene, title="Undefined Node", category=None, inputs=[], outputs=[]):
        super().__init__()
        self._title = title
        self.scene = scene
        self.content = QDMNodeContentWidget(self)
        self.grNode = QDMGraphicsNode(self)
        self.title = title
        self.category = category

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.socket_spacing = 22

        # create socket for inputs and outputs
        self.inputs = []
        self.outputs = []

        counter = 0
        for item in inputs:
            socket = Socket(node=self, index=counter,
                            position=LEFT_BOTTOM, socket_type=item)
            counter += 1
            self.inputs.append(socket)

        counter = 0
        for item in outputs:
            socket = Socket(node=self, index=counter,
                            position=RIGHT_TOP, socket_type=item)
            counter += 1
            self.outputs.append(socket)

        self.tag_list = {"aiml": AIML,
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

    def decode_tag(self, tag_type):
        if tag_type in self.tag_list:
            return self.tag_list[tag_type]()
        return False

    def __str__(self):
        return "<Node %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

    def updateSocketPos(self):
        for item in self.inputs:
            item.setSocketPosition()

        for item in self.outputs:
            item.setSocketPosition()

    @property
    def pos(self):
        return self.grNode.pos()        # QPointF

    def setPos(self, x, y):
        self.grNode.setPos(x, y)

    @property
    def title(self): return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.grNode.title = self._title

    def getSocketPosition(self, index, position):
        x = 0 if (position in (LEFT_TOP, LEFT_BOTTOM)) else self.grNode.width

        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            # start from bottom
            y = self.grNode.height - self.grNode.edge_size - \
                self.grNode._padding - index * self.socket_spacing
        else:
            # start from top
            y = self.grNode.title_height + self.grNode._padding + \
                self.grNode.edge_size + index * self.socket_spacing

        return [x, y]

    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                socket.edge.updatePositions()

    def remove(self):
        if DEBUG:
            print("> Removing Node", self)
        if DEBUG:
            print(" - remove all edges from sockets")
        for socket in (self.inputs+self.outputs):
            if socket.hasEdge():
                if DEBUG:
                    print("    - removing from socket:",
                          socket, "edge:", socket.edge)
                socket.edge.remove()
        if DEBUG:
            print(" - remove grNode")
        self.scene.grScene.removeItem(self.grNode)
        self.grNode = None
        if DEBUG:
            print(" - remove node from the scene")
        self.scene.removeNode(self)
        if DEBUG:
            print(" - everything was done.")

    def serialize(self):
        print("Serializing Node")
        inputs, outputs = [], []
        for socket in self.inputs:
            inputs.append(socket.serialize())
        for socket in self.outputs:
            outputs.append(socket.serialize())
        return OrderedDict([
            ('id', self.objId),
            ('title', self.title),
            ('pos_x', self.grNode.scenePos().x()),
            ('pos_y', self.grNode.scenePos().y()),
            ('inputs', inputs),
            ('outputs', outputs),
            ('content', self.content.serialize()),
            ('category', self.category.serialize())
        ])

    def deserialize(self, data, hashmap={}, restore_id=True):
        print("Deserializing Node")
        if restore_id:
            self.objId = data['id']
        hashmap[data['id']] = self

        self.setPos(data['pos_x'], data['pos_y'])
        self.title = data['title']
        print("tag type: " + data['category']['type'])
        self.category = self.decode_tag(data['category']['type'])
        print(self.category)
        self.category.deserialize(data['category'])

        self.content.node = self
        self.content.node.category = self.category
        self.content.wdg_label.imageLabel.displayVisuals(self.category)

        data['inputs'].sort(
            key=lambda socket: socket['index'] + socket['position'] * 10000)
        data['outputs'].sort(
            key=lambda socket: socket['index'] + socket['position'] * 10000)

        self.inputs = []
        for socket_data in data['inputs']:
            new_socket = Socket(node=self, index=socket_data['index'], position=socket_data['position'],
                                socket_type=socket_data['socket_type'])
            new_socket.deserialize(socket_data, hashmap, restore_id)
            self.inputs.append(new_socket)

        self.outputs = []
        for socket_data in data['outputs']:
            new_socket = Socket(node=self, index=socket_data['index'], position=socket_data['position'],
                                socket_type=socket_data['socket_type'])
            new_socket.deserialize(socket_data, hashmap, restore_id)
            self.outputs.append(new_socket)

        return True

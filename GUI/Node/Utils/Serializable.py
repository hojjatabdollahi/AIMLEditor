class Serializable():
    def __init__(self):
        self.objId = id(self)

    def serialize(self):
        raise NotImplemented()

    def deserialize(self, data, hashmap={}):
        raise NotImplemented()

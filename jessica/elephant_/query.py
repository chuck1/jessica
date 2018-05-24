import elephant.file

class Query(elephant.file._AArray):
    def to_array(self):
        d = dict(self.d)
        d["_collection"] = "tasks queries"
        return d

class Engine(elephant.file.Engine):
    def _factory(self, d):
        return Query(self.coll, d)


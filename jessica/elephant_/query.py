import elephant.local_

class Query(elephant.local_.File):
    def to_array(self):
        d = dict(self.d)
        d["_collection"] = "texts queries"
        return d

class Engine(elephant.local_.Engine):
    def _factory(self, d):
        return Query(self.coll, d)


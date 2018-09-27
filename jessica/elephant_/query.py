import elephant.local_

class Query(elephant.local_.File):
    def __init__(self, e, d, _d):
        super().__init__(e, d, _d)
        self.d["_collection"] = "texts queries"

class Engine(elephant.local_.Engine):
    def __init__(self, h, coll):
        super().__init__(coll)
        self.h = h
        self._doc_class = Query


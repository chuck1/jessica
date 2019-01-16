import elephant.local_
import elephant.local_.doc

class Query(elephant.local_.doc.Query):
    def __init__(self, e, d, _d, is_subobject, ):
        super().__init__(e, d, _d, is_subobject, )
        self.d["_collection"] = "texts queries"

class Engine(elephant.local_.Engine):
    def __init__(self, h, coll):
        super().__init__(coll)
        self.h = h
        self._doc_class = Query


import elephant.local_

class Query(elephant.local_.File):
    async def __encode__(self):
        d = dict(self.d)
        d["_collection"] = "texts queries"
        return {'Document': d}

class Engine(elephant.local_.Engine):
    async def _factory(self, d):
        return Query(self, d)


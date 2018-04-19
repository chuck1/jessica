import datetime
import bson
import jessica.aarray

class Text(jessica.aarray._AArray):
    def __init__(self, engine, d):
        super(Text, self).__init__(engine, d['_id'], d)

    def to_array(self):
        def _f(k, v):
            if isinstance(v, datetime.datetime):
                v = str(v)

            if isinstance(v, bson.objectid.ObjectId):
                v = str(v)

            return k, v

        d0 = dict(_f(k, v) for k, v in self.d.items())

        del d0['_elephant']

        return d0



import json
import datetime
import bson
import jessica.aarray

class Text(jessica.aarray._AArray):
    def __init__(self, engine, d):
        super(Text, self).__init__(engine, d['_id'], d)

    async def to_array(self):
        
        d0 = dict(self.d)

        # render
        s = await self.engine.get_file({'_id': self.d['_id']})
            
        if '_temp' not in d0:
            d0['_temp'] = {}
        
        d0['_temp']['html'] = s

        del d0['_elephant']

        # test json encode
        if False:
            try:
                bson.json_util.dumps(d0)
            except:
                print(d0)
                raise

        return d0



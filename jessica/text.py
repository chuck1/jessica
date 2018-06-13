import json
import datetime
import traceback
import bson
import elephant.global_

class Text(elephant.global_.File):
    def __init__(self, e, d):
        super(Text, self).__init__(e, d)

    async def to_array(self):
        
        d0 = dict(self.d)

        # render
        try:
            d0['_temp']['html'] = await self.render()
        except Exception as e:
            d0['_temp']['html'] = str(e)

        del d0['_elephant']

        d0['_collection'] = 'texts'

        return d0

    def check(self):
        super(Text, self).check()

        if '_texts' in self.d:
             logger.error('has field "_texts"')
             #f["texts"] = f.d["_texts"]
             #self.e_texts.coll_files.update_one({"_id": f.d["_id"]}, {"$unset": {"_texts": ""}})

    async def render(self):
        context_2 = {'d': self}
        print(f'render')
        print(f'context_2 = {context_2}')
        try:
            return await self.e.get_file(
                    {"_id": self.d["_id"]},
                    context_2=context_2,
                    )
        except Exception as e:
            traceback.print_exc()
            return str(e)


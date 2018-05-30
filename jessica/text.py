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
            s = await self.e.get_file({'_id': self.d['_id']})
        
            d0['_temp']['html'] = s
        except Exception as e:
            d0['_temp']['html'] = str(e)

        del d0['_elephant']

        # test json encode
        if False:
            try:
                bson.json_util.dumps(d0)
            except:
                print(d0)
                raise

        return d0

    async def render(self):
        context_2 = {'d': self}
        print(f'render')
        print(f'context_2 = {context_2}')
        try:
            return await self.e.get_file(
                    {'_id': self.d['_id']},
                    context_2=context_2,
                    )
        except Exception as e:
            traceback.print_exc()
            return str(e)


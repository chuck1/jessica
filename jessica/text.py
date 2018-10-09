import json
import datetime
import logging
import traceback

import bson
import elephant.global_

logger = logging.getLogger(__name__)

class Text(elephant.global_.File):
    def __init__(self, e, d, _d, *args):
        super().__init__(e, d, _d, *args)
        self.d['_collection'] = 'texts'

    async def update_temp(self, user):
        logger.info("update temp")

        await super().update_temp(user)

        # render
        try:
            self.d['_temp']['html'] = await self.render()
        except Exception as e:
            logger.error("error in text render: {e!r}")
            self.d['_temp']['html'] = repr(e)

        #logger.info(f'temp = {self.d["_temp"]}')

    async def check(self):
        await super().check()

        if '_texts' in self.d:
             logger.error('has field "_texts"')
             #f["texts"] = f.d["_texts"]
             #self.e_texts.coll_files.update_one({"_id": f.d["_id"]}, {"$unset": {"_texts": ""}})

    async def render(self):
        context_2 = {'d': self}
        #logger.debug(f'render')
        #logger.debug(f'context_2 = {context_2}')
        try:
            return await self.e.get_file(
                    {"_id": self.d["_id"]},
                    doc       = self,
                    context_2 = context_2,
                    )
        except Exception as e:
            traceback.print_exc()
            return str(e)


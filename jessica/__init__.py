import os

import elephant.global_
import aardvark
import jinja2
import markdown
import bson
import pymongo

def breakpoint():
    import pdb; pdb.set_trace()

class Engine:
    def __init__(self):
        self.globals_1 = {}
        self._context_2 = {}
    
    async def render_text_2(self, text, context={}):

        template = self.template_env.from_string(text)

        template.globals.update(self.globals_1)

        #print(f'render_text_2')
        #print(f'context = {context}')
        #print(f'template text = {text!r}')

        ret = await template.render_async(context)

        #print(f'ret = {ret!r}')

        return template, ret

    def get_template_name(self, path):
        return 'default.html'

    async def render_text_4(self, path, text, template_1, context_2={}):

        # TODO module attribute not available in async mode. reimplement the following
        #if 'template' in dir(template_1.module):
        #    template_file = template_1.module.template
        #else:
        
        template_file = self.get_template_name(path)

        block_name = 'body'

        template_text = f'{{% extends {template_file!r} %}} {{% block {block_name} %}}{text}{{% endblock %}}'
        
        template = self.template_env.from_string(template_text)

        c = dict(self._context_2)
        c.update(context_2)

        text_2 = await template.render_async(c)

        return text_2

    async def render(self, path, context_1={}, context_2={}):
        return await self.get_file(path, context_1, context_2)

    async def get_file(self, path, context_1={}, context_2={}):
        # source is rendered twice.
        # first to get the body as html and get variables set by the template, and 
        # second to but the body into the page.
        #
        #        jinja        markdown        jinja
        # text_1 ----> text_2 -------> html_1 ----> html_2
        
        text_1 = await self.get_raw(path)

        template_1, text_2 = await self.render_text_2(text_1, context_1)

        text_3 = self.render_text_3(path, template_1, text_2)

        text_4 = await self.render_text_4(path, text_3, template_1, context_2)

        return text_4
       


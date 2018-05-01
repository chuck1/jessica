import os

import elephant.global_
import aardvark
import jinja2
import markdown
import bson
import pymongo

import jessica

def breakpoint():
    import pdb; pdb.set_trace()

class Engine(jessica.Engine):
    def __init__(self, directory):
        jessica.Engine.__init__(self)

        self.directory = directory

        self.template_loader = jinja2.FileSystemLoader(os.path.join(self.directory, 'templates'))

        self.template_env = jinja2.Environment(
                loader=self.template_loader,
                autoescape=jinja2.select_autoescape(['html', 'xml']),
                )

        self.ext_mapping = {
                '.html': '.md',
                }

    async def get_raw(self, path0):
        h, ext = os.path.splitext(path0)
        ext2 = self.ext_mapping[ext]
        path1 = h + ext2
        path2 = os.path.join(self.directory, path1)
        with open(path2) as f:
            return f.read()

    async def write_file(self, path, text):
        h, ext = os.path.splitext(path)
        ext2 = self.ext_mapping[ext]
        path2 = h + ext2

        path3 = os.path.join(self.directory, path2)
        
        with open(path3, 'w') as f:
            f.write(text)

    def render_text_3(self, path, template_1, text_2):
        
        mapping = {
                '.html': self.render_text_3_md_to_html,
                }

        h, ext = os.path.splitext(path)

        f = mapping[ext]

        return f(path, template_1, text_2)

    def render_text_3_md_to_html(self, path, template_1, text_2):
        
        html = markdown.markdown(text_2)

        return html



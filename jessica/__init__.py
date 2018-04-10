import os

import jinja2
import markdown

class Source:
    pass

class SourceMongo:
    def __init__(self, db_name):
        client = pymongo.MongoClient(os.environ['MONGO_URI'])
        self.db = client[db_name]

    async def get_raw(self, filt):
        return

    async def write_file(self, filt, text):
        return 

class SourceFile:
    def __init__(self, directory):
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

class Engine:
    def __init__(self, source_dir):
        self.source_dir = source_dir

        self.mapping = {
                '.html': self.get_md_to_html,
                }

        self.source = SourceFile(source_dir)
    
    async def get_raw(self, path):
        return await self.source.get_raw(path)

    async def get_file(self, path, **kwargs):
        h, ext = os.path.splitext(path)
        f = self.mapping[ext]
        return await f(path, h, ext, **kwargs)

    async def write_file(self, path, text):
        await self.source.write_file(path, text)

    def render_text_2(self, text, context={}):

        template = self.source.template_env.from_string(text)

        return template, template.render(context)

    def render_html_2(self, html, template_1, context_2={}):

        if 'template' in dir(template_1.module):
            template_file = template_1.module.template
        else:
            template_file = 'default.html'

        block_name = 'body'

        template_text = f'{{% extends {template_file!r} %}} {{% block {block_name} %}}{html}{{% endblock %}}'
        
        template = self.source.template_env.from_string(template_text)

        html_2 = template.render(context_2)

        return html_2

    def render_html(self, template_1, text_2):
        
        html = markdown.markdown(text_2)

        return html

    async def get_md_to_html(self, path, h, ext, context_1={}, context_2={}):
        # source is rendered twice.
        # first to get the body as html and get variables set by the template, and second to but the body into the page.
        #
        # text_1 -> text_2 -> html_1 -> html_2
        
        text_1 = await self.source.get_raw(path)

        template_1, text_2 = self.render_text_2(text_1, context_1)

        html_1 = self.render_html(template_1, text_2)

        html_2 = self.render_html_2(html_1, template_1, context_2)

        return html_2
       



import os

import jinja2
import markdown

class Source:
    pass

class SourceFile:
    def __init__(self, directory):
        self.directory = directory

        self.template_loader = jinja2.FileSystemLoader(os.path.join(self.directory, 'templates'))

        self.template_env = jinja2.Environment(
                loader=self.template_loader,
                autoescape=jinja2.select_autoescape(['html', 'xml']),
                )

    def get_raw(self, path):
        path1 = os.path.join(self.directory, path)
        with open(path1) as f:
            return f.read()

class Engine:
    def __init__(self, source_dir):
        self.source_dir = source_dir

        self.mapping = {
                '.html': self.get_md_to_html,
                }

        self.ext_mapping = {
                '.html': '.md',
                }

        self.source = SourceFile(source_dir)
    
    async def get_raw(self, path):
        h, ext = os.path.splitext(path)
        ext2 = self.ext_mapping[ext]
        path2 = h + ext2

        return self.source.get_raw(path2)

    async def get_file(self, path, **kwargs):
        h, ext = os.path.splitext(path)
        f = self.mapping[ext]
        return await f(h, ext, **kwargs)

    async def write_file(self, path, text):
        h, ext = os.path.splitext(path)
        ext2 = self.ext_mapping[ext]
        path2 = h + ext2

        path3 = os.path.join(self.source_dir, path2)
        
        with open(path3, 'w') as f:
            f.write(text)

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

    async def get_md_to_html(self, h, ext, context_1={}, context_2={}):
        # source is rendered twice.
        # first to get the body as html and get variables set by the template, and second to but the body into the page.
        #
        # text -> text_2 -> html -> html_2

        file_source = os.path.join(self.source_dir, h + '.md')
        
        with open(file_source) as f:
            text = f.read()
        

        template_1, text_2 = self.render_text_2(text, context_1)

        html = markdown.markdown(text_2)

        html_2 = self.render_html_2(html, template_1, context_2)

        return html_2
       



import os

import jinja2
import markdown

class Engine:
    def __init__(self, source_dir, source_package):
        self.source_dir = source_dir

        self.mapping = {
                '.html': self.get_md_to_html,
                }

        self.env = jinja2.Environment(
                loader=jinja2.PackageLoader(source_package, 'templates'),
                autoescape=jinja2.select_autoescape(['html', 'xml']),
                )
    
    async def get_file(self, path):
        h, ext = os.path.splitext(path)
        f = self.mapping[ext]
        return await f(h, ext)

    def render_text_2(self, text):

        template = self.env.from_string(text)

        return template.render()

    async def get_md_to_html(self, h, ext):
        # source is rendered twice.
        # first to get the body as html and get variables set by the template, and second to but the body into the page.
        #
        # text -> text_2 -> html -> html_2

        file_source = os.path.join(self.source_dir, h + '.md')
        
        with open(file_source) as f:
            text = f.read()
        

        text_2 = self.render_text_2(text)

        html = markdown.markdown(text_2)

        template_file = 'default.html'
        block_name = 'body'

        template_text = f'{{% extends {template_file!r} %}} {{% block {block_name} %}}{html}{{% endblock %}}'
        print(f'template_text={template_text!r}')
        
        template = self.env.from_string(template_text)

        html_2 = template.render()

        return html_2
       



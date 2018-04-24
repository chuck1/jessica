import os

import elephant.database_global
import aardvark
import jinja2
import markdown
import bson
import pymongo

def breakpoint():
    import pdb; pdb.set_trace()

class Source:
    pass

SAMPLE_COLLECTIONS = {
        'refs': [
            {
                '_id': '1',
                'name': 'master',
                'commit_id': '2',
                },
            ],
        'texts': [ # working_tree
            {
                '_id': '1',
                'commit_id': '2',
                'content': {}
                },
            ],
        'commits': [
            {
                '_id': '2',
                'parent': '1',
                'files': [
                    {
                        'id': '1',
                        'changes': [],
                        }
                    ],
                }
            ],
        }

class MongoLoader(jinja2.BaseLoader):
    def __init__(self, source):
        self.source = source

    def get_source(self, environment, template):
        # filter that describes file
        filt = {'template': template}
        raw = self.source._get_raw(filt)

        if raw is None:
            if template == 'default.html':
                raw = '{% block body %}{% endblock %}'
            else:
                raise jinja2.TemplateNotFound(template)

        return (raw, None, lambda: False)

class SourceMongo:
    def __init__(self, db, ref_name):
        self.engine = elephant.database_global.DatabaseGlobal(db, ref_name)

        self.template_loader = MongoLoader(self)

        self.template_env = jinja2.Environment(
                loader=self.template_loader,
                autoescape=jinja2.select_autoescape(['html', 'xml']),
                )

        self.working_tree_id = None

    def commit_history_rev(self, commit_id):

        while commit_id:
            c = self.db.commits.find_one({'_id': commit_id})
            yield c
            commit_id = c['parent']

    def commit_history(self, commit_id):
        return reversed(list(self.commit_history_rev(commit_id)))
    
    def construct_file_content(self, file_id, commit_id):

        content = {}

        for c in self.commit_history(commit_id):
    
            for cf in c['files']:
                if cf['file_id'] != file_id: continue

                diffs0 = cf['changes']
                diffs1 = [aardvark.from_array(d) for d in diffs0]

                content = aardvark.apply(content, diffs1)
            
        return content

    def working_tree_file(self, file_id):
        
        file0 = self.db.texts.find_one({'_id': file_id})

        c0 = file0['commit_id'] 

        if c0 == self.ref['commit_id']:
            return file0['content']

        else:
            content = self.construct_file_content(file_id, self.ref['commit_id'])

            self.db.texts.update_one({'_id': file_id}, {'$set': {'content': content}})

            return content

    def update_tree(self):

        for file0 in self.db.texts.find():
            self.working_tree_file(file0['_id'])

    def _get_raw(self, filt):
        
        file0 = self._get_text_item(filt)

        if file0 is None: return
        
        if not isinstance(file0['text'], str):
            raise TypeError(f'text field must be string. {file0!r}')

        return file0['text']

    async def get_raw(self, filt):
        return self._get_raw(filt)

    def _get_text_item(self, filt0):
        
        #self.update_tree()

        #filt1 = dict((f'content.{k}', v) for k, v in filt0.items())

        #item = self.db.texts.find_one(filt)

        item = self.engine.get_content(filt0)

        return item

    async def get_text_item(self, filt0):
        return self._get_text_item(filt0)

    async def insert_text_item(self, item):
        return self.engine.put(None, item)

    def put_new(self, item):
        return self.engine.put(None, item)

    def put(self, item_id, item):
        return self.engine.put(item_id, item)
      
    def render_text_3(self, filt, template_1, text_2):
        
        return self.render_text_3_md_to_html(filt, template_1, text_2)

    def render_text_3_md_to_html(self, filt, template_1, text_2):
        
        text_3 = markdown.markdown(text_2)

        return text_3

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

class Engine:
    def __init__(self, source):
        self.source = source #SourceFile(source_dir)
    
    async def get_raw(self, path):
        return await self.source.get_raw(path)

    async def write_file(self, path, text):
        await self.source.write_file(path, text)

    def render_text_2(self, text, context={}):
        template = self.source.template_env.from_string(text)

        return template, template.render(context)

    def render_text_4(self, text, template_1, context_2={}):

        if 'template' in dir(template_1.module):
            template_file = template_1.module.template
        else:
            template_file = 'default.html'

        block_name = 'body'

        template_text = f'{{% extends {template_file!r} %}} {{% block {block_name} %}}{text}{{% endblock %}}'
        
        template = self.source.template_env.from_string(template_text)

        text_2 = template.render(context_2)

        return text_2

    async def get_file(self, path, context_1={}, context_2={}):
        # source is rendered twice.
        # first to get the body as html and get variables set by the template, and second to but the body into the page.
        #
        # text_1 -> text_2 -> html_1 -> html_2
        
        text_1 = await self.source.get_raw(path)

        template_1, text_2 = self.render_text_2(text_1, context_1)

        html_1 = self.source.render_text_3(path, template_1, text_2)

        text_4 = self.render_text_4(html_1, template_1, context_2)

        return text_4
       
class EngineDB(Engine):
    
    def __init__(self, db, ref_name):
        super(EngineDB, self).__init__(SourceMongo(db, ref_name))

    async def get_file(self, filt, context_1={}, context_2={}):

        if 'template' in filt:
            return await self.source.get_raw(filt)
        
        return await super(EngineDB, self).get_file(filt, context_1, context_2)

    def put(self, item_id, item):
        return self.source.put(item_id, item)

    def put_new(self, item):
        return self.source.put_new(item)

    def find(self, filt):
        return self.source.engine.find(filt)


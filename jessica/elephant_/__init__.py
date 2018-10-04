import jinja2_async
import logging
import markdown
import pprint
import tempfile
import bson.json_util
import elephant.global_
import jessica
import jessica.text
import jessica.elephant_.query

logger = logging.getLogger(__name__)

class Loader(jinja2_async.BaseLoader):
    def __init__(self, e):
        self.e = e
        self.template_filter = {}

    async def get_source(self, environment, template):
        # filter that describes file
        filt = {'template': template}
        filt.update(self.template_filter)

        raw = await self.e.get_raw(filt)

        if raw is None:
            if template == 'default.html':
                raw = '{% block body %}{% endblock %}'
            else:
                raise jinja2_async.TemplateNotFound(template)

        return (raw, None, lambda: False)

class Engine(elephant.global_.Engine, jessica.Engine):

    def __init__(self, h, coll, ref_name):
        self.h = h
        jessica.Engine.__init__(self)
        elephant.global_.Engine.__init__(
                self, 
                coll, 
                ref_name,
                jessica.elephant_.query.Engine(h, coll.queries)
                )

        self.template_loader = Loader(self)

        self.template_env = jinja2_async.Environment(
                loader=self.template_loader,
                autoescape=jinja2_async.select_autoescape(['html', 'xml']),
                )

        self.working_tree_id = None

        self._doc_class = jessica.text.Text

    async def create_indices(self):
        self.coll.files.create_index([
                ("title", "text"), 
                ("text", "text")])

    def commit_history_rev(self, commit_id):

        while commit_id:
            c = self.coll_commits.find_one({'_id': commit_id})
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
        
        file0 = self.coll_files.find_one({'_id': file_id})

        c0 = file0['commit_id'] 

        if c0 == self.ref['commit_id']:
            return file0['content']

        else:
            content = self.construct_file_content(file_id, self.ref['commit_id'])

            self.coll_files.update_one({'_id': file_id}, {'$set': {'content': content}})

            return content

    def update_tree(self):

        for file0 in self.coll_files.find():
            self.working_tree_file(file0['_id'])

    async def get_raw(self, filt):
        
        file0 = await self.get_text_item(filt)

        if file0 is None: return ""
        
        if not "text" in file0.d:
            return ""

        if not isinstance(file0.d['text'], str):
            raise TypeError(f'text field must be string. {file0!r}')

        return file0.d['text']

    async def get_text_item(self, filt0):
        
        #self.update_tree()

        #filt1 = dict((f'content.{k}', v) for k, v in filt0.items())

        #item = self.coll_files.find_one(filt)

        item = await self._find_one(filt0)

        return item

    async def insert_text_item(self, item):
        return self.put(None, item)

    async def get_template_name(self, filt, doc=None):
        if doc is None:
            doc = await self._find_one(filt)

        if 'template_' in doc.d:
            return doc.d['template_']
        return 'default.html'

    def render_text_3(self, filt, template_1, text_2):
        return self.render_text_3_md_to_html(filt, template_1, text_2)

    def render_text_3_md_to_html(self, filt, template_1, text_2):
        
        text_3 = markdown.markdown(text_2)

        return text_3

    def render_text_3_dot(self, filt, template_1, text_2, doc=None):
        logger.info('render dot')

        with tempfile.NamedTemporaryFile('r+') as f0:
            with tempfile.NamedTemporaryFile('r+b', suffix='.svg') as f1:
                f0.write(text_2)
                f0.flush()
                f0.seek(0)

                import pygraphviz
                B = pygraphviz.AGraph(f0.name)
                B.layout(prog=doc.d['lang'])
                B.draw(f1.name)

                f1.flush()
                f1.seek(0)
                text_3 = f1.read()

        
        # debug
        a = text_3
        b = bson.json_util.dumps(a)
        logger.info('a',a)
        logger.info('b',b)


        return text_3

    async def render_dot(self, path, context_1={}, context_2={}, doc=None):
        
        text_1 = await self.get_raw(path)

        template_1, text_2 = await self.render_text_2(text_1, context_1)

        text_3 = self.render_text_3_dot(path, template_1, text_2, doc=doc)

        return text_3.decode()

    async def get_file(self, filt, doc=None, context_1={}, context_2={}):

        logger.debug('render')
        logger.debug(filt)

        if doc is None:
            doc = await self._find_one(filt)

        text_1 = doc.d.get('text', '')

        assert isinstance(text_1, str)

        if 'template' in filt:
            return text_1
 
        language = doc.d.get('lang', 'markdown')

        if language == 'markdown':
            return await super().get_file(filt, text_1=text_1, context_1=context_1, context_2=context_2, doc=doc)

        if language in ('dot', 'neato'):
            return await self.render_dot(filt, context_1, context_2, doc=doc)
       
        return await super().get_file(filt, context_1, context_2)




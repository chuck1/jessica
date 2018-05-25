import jinja2
import markdown

import elephant.global_
import jessica
import jessica.text
import jessica.elephant_.query

class Loader(jinja2.BaseLoader):
    def __init__(self, e):
        self.e = e

    def get_source(self, environment, template):
        # filter that describes file
        filt = {'template': template}
        raw = self.e._get_raw(filt)

        if raw is None:
            if template == 'default.html':
                raw = '{% block body %}{% endblock %}'
            else:
                raise jinja2.TemplateNotFound(template)

        return (raw, None, lambda: False)

class Engine(elephant.global_.Global, jessica.Engine):
    def __init__(self, coll, ref_name):
        jessica.Engine.__init__(self)
        elephant.global_.Global.__init__(
                self, 
                coll, 
                ref_name,
                jessica.elephant_.query.Engine(coll.queries)
                )

        self.template_loader = Loader(self)

        self.template_env = jinja2.Environment(
                loader=self.template_loader,
                autoescape=jinja2.select_autoescape(['html', 'xml']),
                )

        self.working_tree_id = None

    def _factory(self, d):
        return jessica.text.Text(self, d)

    def commit_history_rev(self, commit_id):

        while commit_id:
            c = self.coll_commits.find_one({'_id': commit_id})
            yield c
            commit_id = c['parent']

    def commit_history(self, commit_id):
        return reversed(list(self.commit_history_rev(commit_id)))
 
    async def get_file(self, filt, context_1={}, context_2={}):

        if 'template' in filt:
            return await self.source.get_raw(filt)
        
        return await super(Engine, self).get_file(filt, context_1, context_2)

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

    def _get_raw(self, filt):
        
        file0 = self._get_text_item(filt)

        if file0 is None: return
        
        if not "text" in file0.d:
            return ""

        if not isinstance(file0.d['text'], str):
            raise TypeError(f'text field must be string. {file0!r}')

        return file0.d['text']

    async def get_raw(self, filt):
        return self._get_raw(filt)


    def _get_text_item(self, filt0):
        
        #self.update_tree()

        #filt1 = dict((f'content.{k}', v) for k, v in filt0.items())

        #item = self.coll_files.find_one(filt)

        item = self.get_content(filt0)

        return item

    async def get_text_item(self, filt0):
        return self._get_text_item(filt0)

    async def insert_text_item(self, item):
        return self.put(None, item)

    def render_text_3(self, filt, template_1, text_2):
        
        return self.render_text_3_md_to_html(filt, template_1, text_2)

    def render_text_3_md_to_html(self, filt, template_1, text_2):
        
        text_3 = markdown.markdown(text_2)

        return text_3


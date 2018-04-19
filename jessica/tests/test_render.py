import time
import sys
import os
import tempfile

import pytest

import jessica

@pytest.mark.asyncio
async def test_render():

    with tempfile.TemporaryDirectory() as d:

        d1 = os.path.join(d, 'source')

        os.makedirs(d1)
        os.makedirs(os.path.join(d1, 'templates'))

        with open(os.path.join(d1, 'index.md'), 'w') as f:
            f.write('{% set template = "temp1.html" %}\n# hello\n\n[test](a/b/c)')

        with open(os.path.join(d1, 'templates', 'default.html'), 'w') as f:
            f.write('{% block body %}{% endblock %}')

        with open(os.path.join(d1, 'templates', 'temp1.html'), 'w') as f:
            f.write('<html><head></head><body>{% block body %}{% endblock %}</body></html>')

        e = jessica.Engine(jessica.SourceFile(d1))
        
        e.source.template_env.get_template('default.html')

        e.source.template_env.get_template('temp1.html')

        print(await e.get_file('index.html'))

@pytest.mark.asyncio
async def test_render_mongo():

        e = jessica.EngineDB(f'test_{int(time.time())}')

        text = '{% set template = "temp1.html" %}\n# hello\n\n[test](a/b/c)'

        temp_1_text = '{% block body %}{% endblock %}'
        temp_2_text = '<html><head></head><body>{% block body %}{% endblock %}</body></html>'

        print('write file')

        await e.put_new({'title': 'i like kittens'}, text)

        await e.put_new({'template': 'default.html'}, temp_1_text)

        await e.put_new({'template': 'temp1.html'}, temp_2_text)

        e.source.template_env.get_template('default.html')

        e.source.template_env.get_template('temp1.html')

        print(await e.get_file({'title': 'i like kittens'}))




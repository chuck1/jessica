import time
import sys
import os
import tempfile

import pytest
import jessica.elephant_
import jessica.filesystem_

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

        e = jessica.filesystem_.Engine(d1)
        
        e.template_env.get_template('default.html')

        e.template_env.get_template('temp1.html')

        print(await e.get_file('index.html'))

@pytest.mark.asyncio
async def test_render_mongo(database):

        e = jessica.elephant_.Engine(database, "master")

        text = '{% set template = "temp1.html" %}\n# hello\n\n[test](a/b/c)'

        temp_1_text = '{% block body %}{% endblock %}'
        temp_2_text = '<html><head></head><body>{% block body %}{% endblock %}</body></html>'

        print('write file')

        e.put_new({'title': 'i like kittens', "text": text})

        e.put_new({'template': 'default.html', "text": temp_1_text})

        e.put_new({'template': 'temp1.html', "text": temp_2_text})

        e.template_env.get_template('default.html')

        e.template_env.get_template('temp1.html')

        print(await e.get_file({'title': 'i like kittens'}))




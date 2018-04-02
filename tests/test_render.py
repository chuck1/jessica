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

        e = jessica.Engine(d1)
        
        e.env.get_template('default.html')

        e.env.get_template('temp1.html')

        print(await e.get_file('index.html'))




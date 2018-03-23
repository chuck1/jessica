import sys
import os
import tempfile

import pytest

import jessica

@pytest.mark.asyncio
async def test_render():

    with tempfile.TemporaryDirectory() as d:

        d1 = os.path.join(d, 'source_package')

        os.makedirs(d1)
        os.makedirs(os.path.join(d1, 'templates'))

        with open(os.path.join(d1, '__init__.py'), 'w') as f:
            f.write('')

        with open(os.path.join(d1, 'index.md'), 'w') as f:
            f.write('# hello\n\n[test](a/b/c)')

        with open(os.path.join(d1, 'templates', 'default.html'), 'w') as f:
            f.write('{% block body %}{% endblock %}')

        sys.path.append(d)
        
        e = jessica.Engine(d1, 'source_package')
        
        await e.get_file('index.html')




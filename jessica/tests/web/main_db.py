import os
import sys
import aiohttp.web
import jessica
import json
import jinja2
import pymongo

def breakpoint(): import pdb;pdb.set_trace()

client = pymongo.MongoClient(os.environ['MONGO_URI'])
db = client.texts_personal
e = jessica.EngineDB(db, "master")

async def icon(request):
    return aiohttp.web.HTTPFound('https://s3-us-west-2.amazonaws.com/19f075ca4a482833.media/j.ico')

async def index(request):
    print('index')
    print(request.url)

    filt = dict(request.query)

    raw = await e.get_raw(filt)

    if raw is None:
        print('file does not exist')
        await e.write_file(filt, '')

        raw = await e.get_raw(filt)

        if raw is None:
            raise Exception()

    text = await e.get_file(filt, context_2={
        })

    env = jinja2.Environment(
            loader=jinja2.FileSystemLoader('jessica/tests/web/static/'),
            autoescape=jinja2.select_autoescape(['html', 'xml'])
            )
        
    t = env.get_template('index.html')

    html = t.render({
        'path': repr(json.dumps(filt)),
        'raw': repr(raw),
        'body': text,
        })

    return aiohttp.web.Response(text=html, content_type='text/html')

async def edit(request):
    print('edit')
    data = await request.json()
    print(data)
    filt = json.loads(data['path'])
    print(filt)

    await e.write_file(filt, data['text'])
    
    print('write complete')

    return aiohttp.web.json_response('hello')

app = aiohttp.web.Application()

app.router.add_static('/static/', 'jessica/tests/web/static/', name='static')
app.router.add_get('/favicon.ico', icon)
app.router.add_post('/edit', edit)
app.router.add_get('/index', index)

aiohttp.web.run_app(app, host='192.168.56.2', port=8002)




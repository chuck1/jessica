import sys
import aiohttp.web
import jessica

e = jessica.Engine(sys.argv[1])

async def icon(request):
    return aiohttp.web.HTTPFound('https://s3-us-west-2.amazonaws.com/19f075ca4a482833.media/j.ico')

async def index(request):
    print('index')
    print(request.url)

    path = request.match_info.get('path')

    raw = await e.get_raw(path)

    html = await e.get_file(path, context_2={
        'path': path,
        'raw': repr(raw),
        })

    return aiohttp.web.Response(text=html, content_type='text/html')

async def edit(request):
    print('edit')
    data = await request.json()
    
    await e.write_file(data['path'], data['text'])
    
    return aiohttp.web.json_response('hello')

app = aiohttp.web.Application()

app.router.add_static('/static/', 'jessica/tests/web/static/', name='static')
app.router.add_get('/favicon.ico', icon)
app.router.add_post('/edit', edit)
app.router.add_get('/{path:.*}', index)

aiohttp.web.run_app(app, host='192.168.56.2', port=8002)




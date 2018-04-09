import sys
import aiohttp.web
import jessica

async def icon(request):
    return aiohttp.web.HTTPFound('https://s3-us-west-2.amazonaws.com/19f075ca4a482833.media/j.ico')

async def index(request):

    print(request.url)

    page = request.match_info.get('path')

    e = jessica.Engine(sys.argv[1])

    html = await e.get_file(page, context_1={})

    return aiohttp.web.Response(text=html, content_type='text/html')


app = aiohttp.web.Application()

app.router.add_static('/static/', 'jessica/tests/web/static/', name='static')
app.router.add_get('/favicon.ico', icon)
app.router.add_get('/{path}', index)

aiohttp.web.run_app(app, host='192.168.56.2', port=8002)




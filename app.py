from quart import Quart, render_template, request
import aiohttp

app = Quart(__name__)

async def fetch_proxies(timeout=1000):
    url = f"https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout={timeout}&country=all"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            proxies = [f"socks5://{proxy}" for proxy in (await response.text()).split("\r\n") if proxy.strip()]
    return proxies

@app.route('/')
async def index():
    return await render_template('index.html')

@app.route('/get_proxies', methods=['POST'])
async def get_proxies():
    form = await request.form
    timeout = int(form['timeout'])
    proxies = await fetch_proxies(timeout)
    return {'proxies': proxies}

if __name__ == '__main__':
    app.run(debug=True)

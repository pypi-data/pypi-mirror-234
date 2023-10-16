from pyppeteer import launch
import threading
import asyncio

urls = [
    'https://finance.yahoo.com/quote/APPL/holders?p=APPL',
    'https://finance.yahoo.com/quote/MSFT/holders?p=MSFT',
    'https://finance.yahoo.com/quote/GOOG/holders?p=GOOG',
    'https://finance.yahoo.com/quote/AMZN/holders?p=AMZN',
    'https://finance.yahoo.com/quote/NVDA/holders?p=NVDA'
]

async def test_pyppeteer(url):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url, waitUntil='networkidle0')
    html = await page.content()
    await browser.close()
    return html

def get(url):
    # Test it
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(test_pyppeteer(url))
    return (result)

def get_async(url, res:list):
    # Test it
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(test_pyppeteer(url))
    res.append(result)

def wrapper(urls):
    res = []
    threads = []
    for url in urls:
        threads.append(
            threading.Thread(target=get_async, args=[url, res])
        )
        threads[-1].start()
    
    for thread in threads:
        thread.join()
    
    return res

# =============================================

async def test_pyppeteer(url):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url, waitUntil='networkidle0')
    html = await page.content()
    await browser.close()
    return html

async def wrapper(urls):
    return await asyncio.gather(*(test_pyppeteer(url) for url in urls))

def run_pyppeteer(urls):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(wrapper(urls))
        return result
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()

print(run_pyppeteer(urls))
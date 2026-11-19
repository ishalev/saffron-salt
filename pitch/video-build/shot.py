import asyncio, json, pathlib
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1920, 'height': 1080})
        await pg.goto(pathlib.Path('cards/cards.html').resolve().as_uri()); await pg.wait_for_timeout(2500)
        await pg.locator('#close').screenshot(path='cards/close.png')
        B = json.load(open('cards/boxes.json'))
        for c in ['url', 'names', 'lead', 'mail']:
            r = await pg.evaluate(f"(()=>{{const c=document.querySelector('#close').getBoundingClientRect();const r=document.querySelector('#close .{c}').getBoundingClientRect();return [r.x-c.x,r.y-c.y,r.width,r.height].map(Math.round)}})()")
            B['close.' + c] = r
        json.dump(B, open('cards/boxes.json', 'w')); print(B)
        await b.close()
asyncio.run(main())

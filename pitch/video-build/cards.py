import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1920,'height':1080})
        import pathlib; await pg.goto(pathlib.Path('cards/cards.html').resolve().as_uri()); await pg.wait_for_timeout(2500)
        for i in ['title','close']: await pg.locator('#'+i).screenshot(path=f'cards/{i}.png')
        await b.close()
asyncio.run(main())

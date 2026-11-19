import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); ctx=await b.new_context(viewport={'width':1600,'height':1900},device_scale_factor=3); pg=await ctx.new_page()
        await pg.goto('http://localhost:8773/index.html'); await pg.wait_for_timeout(800)
        await pg.evaluate("window.__mul=0; window.__ev=[]; window.__peek=0")
        await pg.click('[data-act=setN][data-v="4"]')
        for i in range(4): await pg.locator(f'[data-act=seatType][data-i="{i}"]').nth(1).click()
        await pg.fill('#seed','fennel-nutmeg-110'); await pg.locator('#seed').dispatch_event('input')
        await pg.click('[data-act=start]')
        await pg.wait_for_selector('.results h1', timeout=120000)
        await pg.get_by_role('button', name='Game log').first.click(); await pg.wait_for_timeout(800)
        await pg.screenshot(path='log1x.png')
        await pg.evaluate("for (const el of document.querySelectorAll('*')) { if (el.scrollHeight > el.clientHeight + 20 && getComputedStyle(el).overflowY.match(/auto|scroll/)) el.scrollTop = el.scrollHeight; }")
        await pg.wait_for_timeout(500); await pg.screenshot(path='log2x.png')
        await b.close()
asyncio.run(main())

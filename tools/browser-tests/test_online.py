# Online game through relay.php: host and guest in separate browsers, both change a choice.
# Start ./serve.sh first, then: python3 test_online.py
import asyncio
from playwright.async_api import async_playwright
from drv import step, launch_args
URL = 'http://localhost:8772/'
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(**launch_args())
        c1 = await b.new_context(viewport={'width': 1300, 'height': 950}); c2 = await b.new_context(viewport={'width': 1300, 'height': 950})
        for c in (c1, c2): await c.add_init_script(script='window.__fast=true')
        host = await c1.new_page(); guest = await c2.new_page(); errs = []
        for pg, n in [(host, 'host'), (guest, 'guest')]: pg.on('pageerror', lambda e, n=n: errs.append(f'{n}: {e}'))
        await host.goto(URL); await guest.goto(URL)
        await host.click('[data-act=openOnline]'); await host.wait_for_timeout(800); await host.fill('#hn', 'Host'); await host.click('[data-act=hostCreate]'); await host.wait_for_timeout(500)
        code = (await host.locator('h1').inner_text()).replace(' ', '').strip()
        await guest.click('[data-act=openOnline]'); await guest.wait_for_timeout(800); await guest.fill('#jn', 'Guest'); await guest.fill('#jc', code); await guest.click('[data-act=guestJoin]')
        for _ in range(40):
            await host.wait_for_timeout(250)
            if 'Guest' in await host.locator('.panel').inner_text(): break
        await host.click('[data-act=hostStart]')
        changes = []
        for _ in range(9000):
            await host.wait_for_timeout(50)
            g = guest.locator('[data-act=guestUndo]'); h = host.locator('[data-act=undoBid]')
            if len(changes) < 4 and await g.count(): changes.append('guest'); await g.click(); continue
            if len(changes) < 4 and await h.count(): changes.append('host'); await h.click(); continue
            await step(host); await step(guest)
            if await guest.locator('.results h1').count() and await host.locator('.results h1').count(): break
        same = await host.locator('.podium').inner_text() == await guest.locator('.podium').inner_text()
        print('online game finished with identical results:', same, '| changes made:', changes)
        print('page errors:', errs or 'none'); await b.close()
asyncio.run(main())

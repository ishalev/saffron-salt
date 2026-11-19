# v1.22a options: U20 lot numbers, G8 specialization off, T2 final auction; local and online.
# Start ./serve.sh first, then: python3 test_options.py
import asyncio
from playwright.async_api import async_playwright
from drv import step, launch_args
URL = 'http://localhost:8772/'

async def watch(pg, seen):
    if await pg.locator('.lot.taken').count(): seen['taken'] = True
    if 'Final auction' in await pg.locator('.stepline').inner_text() if await pg.locator('.stepline').count() else False: seen['final'] = True

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(**launch_args())
        errs = []
        # Local: one human, two bots, both options on.
        ctx = await b.new_context(viewport={'width': 1300, 'height': 950}); await ctx.add_init_script(script='window.__fast=true')
        pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(f'local: {e}'))
        await pg.goto(URL); await pg.wait_for_timeout(300)
        await pg.click('summary:has-text("Rule options")')
        await pg.uncheck('[data-inp=setupSpec]'); await pg.select_option('#setupEnd', 'auction')
        await pg.click('[data-act=start]')
        seen = {'taken': False, 'final': False}
        for _ in range(6000):
            await pg.wait_for_timeout(25)
            if await pg.locator('.results h1').count(): break
            await watch(pg, seen); await step(pg)
        res = await pg.locator('.results').inner_text()
        print('local game finished:', await pg.locator('.results h1').count() > 0)
        print('bought lots kept their numbers (greyed slot seen):', seen['taken'])
        print('final auction phase seen:', seen['final'])
        print('results list the options:', 'no specialization bonus; final auction instead of the cash-out' in res)
        rows = {r.split('\t')[0]: r.split('\t')[1:] for r in (await pg.locator('table.st').nth(1).inner_text()).split('\n') if '\t' in r}
        print('no cash-out or specialization points:', all(v == '0' for k in ('Cash-out', 'Specialization') for v in rows.get(k, ['x'])[:3]))

        # Online: host sets the options in the lobby, guest sees them, results match.
        c1 = await b.new_context(viewport={'width': 1300, 'height': 950}); c2 = await b.new_context(viewport={'width': 1300, 'height': 950})
        for c in (c1, c2): await c.add_init_script(script='window.__fast=true')
        host = await c1.new_page(); guest = await c2.new_page()
        for q, n in [(host, 'host'), (guest, 'guest')]: q.on('pageerror', lambda e, n=n: errs.append(f'{n}: {e}'))
        await host.goto(URL); await guest.goto(URL)
        await host.click('[data-act=openOnline]'); await host.wait_for_timeout(800); await host.fill('#hn', 'Host'); await host.click('[data-act=hostCreate]'); await host.wait_for_timeout(500)
        code = (await host.locator('h1').inner_text()).replace(' ', '').strip()
        await host.click('summary:has-text("Rule options")'); await host.select_option('#lobEnd', 'auction'); await host.wait_for_timeout(200)
        await host.uncheck('[data-inp=lobSpec]'); await host.wait_for_timeout(300)
        await guest.click('[data-act=openOnline]'); await guest.wait_for_timeout(800); await guest.fill('#jn', 'Guest'); await guest.fill('#jc', code); await guest.click('[data-act=guestJoin]')
        for _ in range(40):
            await host.wait_for_timeout(250)
            if 'Guest' in await host.locator('.panel').inner_text(): break
        await guest.wait_for_timeout(1500)
        print('guest sees the options in the lobby:', 'final auction instead of the cash-out' in await guest.locator('.results').inner_text())
        await host.click('[data-act=hostStart]')
        gseen = {'taken': False, 'final': False}
        for _ in range(9000):
            await host.wait_for_timeout(50)
            await watch(guest, gseen)
            await step(host); await step(guest)
            if await guest.locator('.results h1').count() and await host.locator('.results h1').count(): break
        same = await host.locator('.podium').inner_text() == await guest.locator('.podium').inner_text()
        print('online game finished with identical results:', same)
        print('guest saw greyed bought lots and the final auction:', gseen['taken'] and gseen['final'])
        print('page errors:', errs or 'none'); await b.close()
asyncio.run(main())

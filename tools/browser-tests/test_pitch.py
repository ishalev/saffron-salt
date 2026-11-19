# v1.22b pitch features: pitch walkthrough (U25), reference card (U24), season and final-scoring panels (U21, U23),
# and online guests clicking OK before the game moves on. Start ./serve.sh first, then: python3 test_pitch.py
import asyncio
from playwright.async_api import async_playwright
from drv import step, launch_args
URL = 'http://localhost:8772/'

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(**launch_args())
        errs = []
        ctx = await b.new_context(viewport={'width': 1300, 'height': 950}); await ctx.add_init_script(script='window.__fast=true')
        pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(f'local: {e}'))
        await pg.goto(URL); await pg.wait_for_timeout(300)

        # Walkthrough: forward to the end, back one, then Start game opens the publisher demo screen.
        await pg.click('[data-act=openWalk]'); await pg.wait_for_timeout(200)
        titles = [await pg.locator('.walkbox h3').inner_text()]
        while await pg.locator('[data-act=walkNext]').is_enabled():
            await pg.click('[data-act=walkNext]'); await pg.wait_for_timeout(100); titles.append(await pg.locator('.walkbox h3').inner_text())
        await pg.click('[data-act=walkBack]'); await pg.wait_for_timeout(100)
        back = await pg.locator('.walkbox h3').inner_text()
        print('walkthrough steps:', len(titles), '| back works:', back == titles[-2], '| no hands shown:', await pg.locator('.hand').count() == 0)
        await pg.click('[data-act=walkStart]'); await pg.wait_for_timeout(500)
        print('start game opens the publisher demo:', 'Publisher demo' in await pg.locator('body').inner_text())
        await pg.goto(URL); await pg.wait_for_timeout(300)

        # Local game: reference card next to the hand, season panels, final-scoring panel with the cash-out bids.
        await pg.click('[data-act=start]')
        seen = {'ref': False, 'season': 0, 'final': False, 'cash': False}
        for _ in range(6000):
            await pg.wait_for_timeout(25)
            if await pg.locator('.results h1').count(): break
            if await pg.locator('.hand .refcard').count(): seen['ref'] = True
            if await pg.locator('.dialog.bigpanel #sst').count(): seen['season'] += 1
            if await pg.locator('.dialog.finalrev').count():
                seen['final'] = True; seen['cash'] = 'Cash-out' in await pg.locator('.dialog.finalrev').inner_text()
            await step(pg)
        print('local game finished:', await pg.locator('.results h1').count() > 0)
        print('reference card beside the hand:', seen['ref'], '| season panel shown:', seen['season'] > 0, '| final panel with cash-out bids:', seen['final'] and seen['cash'])

        # Online: the game waits until the guest clicks OK on the season results.
        c1 = await b.new_context(viewport={'width': 1300, 'height': 950}); c2 = await b.new_context(viewport={'width': 1300, 'height': 950})
        for c in (c1, c2): await c.add_init_script(script='window.__fast=true')
        host = await c1.new_page(); guest = await c2.new_page()
        for q, n in [(host, 'host'), (guest, 'guest')]: q.on('pageerror', lambda e, n=n: errs.append(f'{n}: {e}'))
        await host.goto(URL); await guest.goto(URL)
        await host.click('[data-act=openOnline]'); await host.wait_for_timeout(800); await host.fill('#hn', 'Host'); await host.click('[data-act=hostCreate]'); await host.wait_for_timeout(500)
        code = (await host.locator('h1').inner_text()).replace(' ', '').strip()
        await guest.click('[data-act=openOnline]'); await guest.wait_for_timeout(800); await guest.fill('#jn', 'Guest'); await guest.fill('#jc', code); await guest.click('[data-act=guestJoin]')
        for _ in range(40):
            await host.wait_for_timeout(250)
            if 'Guest' in await host.locator('.panel').inner_text(): break
        await host.click('[data-act=hostStart]')
        held = None; gfinal = False
        for _ in range(9000):
            await host.wait_for_timeout(50)
            await step(host)
            if held is None and await guest.locator('#overlay [data-act=ackOk]').count():
                if await host.locator('#overlay [data-act=seasonOk]').count(): await host.locator('#overlay [data-act=seasonOk]').click()
                await host.wait_for_timeout(1200)
                held = 'Waiting for Guest' in await host.locator('.stage').inner_text()
            # the guest's OK is clicked only here, after looking at the panel it belongs to
            if await guest.locator('#overlay [data-act=ackOk]').count():
                if await guest.locator('.dialog.finalrev').count(): gfinal = True
                try: await guest.locator('#overlay [data-act=ackOk]').click(timeout=3000)
                except Exception: pass
            await step(guest, skip_ack=True)
            if await guest.locator('.results h1').count() and await host.locator('.results h1').count(): break
        same = await host.locator('.podium').inner_text() == await guest.locator('.podium').inner_text()
        print('online: host waits for the guest to click OK:', held, '| guest saw final scoring:', gfinal, '| identical results:', same)
        print('page errors:', errs or 'none'); await b.close()
asyncio.run(main())

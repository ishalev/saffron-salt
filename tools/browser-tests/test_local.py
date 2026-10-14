# Single-device game, feedback, game logs (local and server), replay, pass-and-play with a changed card.
# Start ./serve.sh first, then: python3 test_local.py
import asyncio
from playwright.async_api import async_playwright
from drv import until_results, launch_args
URL = 'http://localhost:8772/'
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(**launch_args())
        ctx = await b.new_context(viewport={'width': 1300, 'height': 950}); await ctx.add_init_script(script='window.__fast=true')
        pg = await ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(300)
        await pg.click('[data-act=start]'); print('single device game:', await until_results(pg))
        await pg.fill('#fbn', 'Tester'); await pg.click('[data-act=fbSend]'); await pg.wait_for_timeout(500)
        print('feedback sent:', 'Thanks' in await pg.locator('.results').inner_text())
        await pg.click('[data-act=home]'); await pg.click('[data-act=openLogs]'); await pg.wait_for_timeout(300)
        print('local log rows:', await pg.locator('table.logs tbody tr').count())
        await pg.click('[data-act=logsTab][data-v=server]'); await pg.fill('#lpw', 'pw123'); await pg.click('[data-act=logsLogin]'); await pg.wait_for_timeout(600)
        print('server log rows:', await pg.locator('table.logs tbody tr').count())
        await pg.click('[data-act=logReplayRow]'); print('replay from log:', await until_results(pg))
        await pg.click('[data-act=home]'); await pg.click('[data-act=seatType][data-i="1"][data-v=h]'); await pg.click('[data-act=start]')
        changed = {'done': False}
        async def change(pg):
            if not changed['done'] and await pg.locator('[data-act=changeBid]').count():
                changed['done'] = True; await pg.locator('[data-act=changeBid]').first.click(); return True
            return False
        print('pass-and-play with a change:', await until_results(pg, extra=change), changed['done'])
        print('page errors:', errs or 'none'); await b.close()
asyncio.run(main())

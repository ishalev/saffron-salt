import asyncio, sys, json, base64, time, os
from playwright.async_api import async_playwright
W,H=1600,int(sys.argv[3]) if len(sys.argv)>3 else 1900; D=sys.argv[1]; SEED='fennel-nutmeg-110'; MUL=float(sys.argv[2]) if len(sys.argv)>2 else 3
frames=[]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        ctx=await b.new_context(viewport={'width':W,'height':H})
        pg=await ctx.new_page(); await pg.goto('http://localhost:8773/index.html'); await pg.wait_for_timeout(800)
        await pg.evaluate(f"window.__mul={MUL}; window.__ev=[]; window.__peek=0")
        await pg.click('[data-act=setN][data-v="4"]')
        for i in range(4):
            btn=pg.locator(f'[data-act=seatType][data-i="{i}"]').nth(1)
            await btn.click()
        await pg.fill('#seed', SEED); await pg.locator('#seed').dispatch_event('input'); await pg.locator('#seed').dispatch_event('change')
        await pg.wait_for_timeout(300)
        print('seed field', await pg.input_value('#seed'), flush=True)
        cdp=await ctx.new_cdp_session(pg)
        async def on_frame(f):
            i=len(frames); frames.append(f['metadata']['timestamp'])
            open(f'{D}/frames/{i:06d}.jpg','wb').write(base64.b64decode(f['data']))
            await cdp.send('Page.screencastFrameAck',{'sessionId':f['sessionId']})
        cdp.on('Page.screencastFrame', lambda f: asyncio.ensure_future(on_frame(f)))
        await cdp.send('Page.startScreencast',{'format':'jpeg','quality':92,'maxWidth':W,'maxHeight':H,'everyNthFrame':1})
        await pg.wait_for_timeout(1000)
        await pg.click('[data-act=start]')
        t=time.time()
        while True:
            await pg.wait_for_timeout(1000)
            if await pg.locator('.results h1').count():
                await pg.wait_for_timeout(6000); break
            if time.time()-t>3600: print('timeout'); break
        ev=await pg.evaluate("window.__ev")
        seed=await pg.evaluate("window.__g && window.__g.seed")
        await cdp.send('Page.stopScreencast'); await pg.wait_for_timeout(500)
        json.dump({'frames':frames,'events':ev,'seed':seed},open(f'{D}/log.json','w'))
        print('frames',len(frames),'span',frames[-1]-frames[0],'events',len(ev),'seed',seed, flush=True)
        await b.close()
asyncio.run(main())

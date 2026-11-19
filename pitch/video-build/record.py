import asyncio, sys, json, base64, time
from playwright.async_api import async_playwright
W,H=1600,1240
SEED=sys.argv[1] if len(sys.argv)>1 else None
frames=[]; events=[]; t0=None
async def main():
    global t0
    async with async_playwright() as p:
        b=await p.chromium.launch()
        ctx=await b.new_context(viewport={'width':W,'height':H})
        pg=await ctx.new_page(); await pg.goto('http://localhost:8772/'); await pg.wait_for_timeout(800)
        cdp=await ctx.new_cdp_session(pg)
        async def on_frame(f):
            ts=f['metadata']['timestamp']; i=len(frames)
            open(f'rec/frames/{i:06d}.jpg','wb').write(base64.b64decode(f['data'])); frames.append(ts)
            await cdp.send('Page.screencastFrameAck',{'sessionId':f['sessionId']})
        cdp.on('Page.screencastFrame', lambda f: asyncio.ensure_future(on_frame(f)))
        await cdp.send('Page.startScreencast',{'format':'jpeg','quality':92,'maxWidth':W,'maxHeight':H,'everyNthFrame':1})
        t0=time.time()
        def ev(s): events.append((round(time.time()-t0,2),s)); print(events[-1],flush=True)
        ev('home'); await pg.wait_for_timeout(1500)
        await pg.click('[data-act=start]'); ev('start')
        last=None
        while True:
            await pg.wait_for_timeout(80)
            if await pg.locator('.results h1').count():
                ev('results'); await pg.wait_for_timeout(8000); break
            st=await pg.evaluate("(()=>{const h=document.querySelector('h2');return (h?h.innerText:'')+' | '+(document.querySelector('.prompt h3')?.innerText||'')})()")
            if st!=last: ev(st); last=st
            for sel in ['[data-act=handoffGo]','[data-act=coachOk]','[data-act=revealBids]']:
                if await pg.locator(sel).count(): await pg.locator(sel).first.click(); break
            if await pg.locator('[data-act=seasonOk]').count():
                ev('season modal'); await pg.wait_for_timeout(5000); await pg.locator('[data-act=seasonOk]').first.click(); continue
            conf=pg.locator('[data-act=confirm]')
            if not await conf.count(): continue
            h3=(await pg.locator('.prompt h3').first.inner_text()).lower()
            await pg.wait_for_timeout(1200)
            if 'bid' in h3 or 'seed' in h3:
                cards=pg.locator('.hand [data-act=selCard]')
                if await cards.count(): await cards.nth(min(1,await cards.count()-1)).click()
            elif 'lot' in h3: await pg.locator('[data-act=selLot]').first.click()
            elif 'order' in h3:
                rec=pg.locator('.opt.rec'); await (rec.first if await rec.count() else pg.locator('[data-act=selOpt]').first).click()
            elif 'keep' in h3: await pg.locator('.prompt [data-act=selCard]').first.click()
            await pg.wait_for_timeout(900)
            if await conf.is_enabled(): await conf.click()
        await cdp.send('Page.stopScreencast'); await pg.wait_for_timeout(500)
        json.dump({'frames':[f-frames[0] for f in frames],'t0_offset':frames[0]-t0 if False else 0,'events':events,'first_ts':frames[0]},open('rec/log.json','w'))
        print('frames',len(frames),'span',frames[-1]-frames[0])
        await b.close()
asyncio.run(main())

import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); ctx=await b.new_context(viewport={'width':1600,'height':1900},device_scale_factor=3); pg=await ctx.new_page()
        await pg.goto('http://localhost:8773/index.html'); await pg.wait_for_timeout(800)
        await pg.evaluate("window.__mul=30; window.__ev=[]; window.__peek=0")
        await pg.click('[data-act=setN][data-v="4"]')
        for i in range(4): await pg.locator(f'[data-act=seatType][data-i="{i}"]').nth(1).click()
        await pg.fill('#seed','fennel-nutmeg-110'); await pg.locator('#seed').dispatch_event('input')
        await pg.click('[data-act=start]'); await pg.wait_for_timeout(2500)
        await pg.screenshot(path='../fig/setup3x.png')
        boxes={}
        for sel in ['.market','.hand','.tracks']:
            l=pg.locator(sel)
            if await l.count(): boxes[sel]=await l.first.bounding_box()
        cards=await pg.evaluate("[...document.querySelectorAll('.card')].map(e=>{const r=e.getBoundingClientRect();return [e.getAttribute('aria-label'),r.x,r.y,r.width,r.height]})")
        import json; json.dump({'boxes':boxes,'cards':cards},open('../fig/setup_boxes.json','w'),indent=1)
        await b.close()
asyncio.run(main())

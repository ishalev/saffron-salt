# Shared helper: performs whatever action the page is asking for (first legal choice).
EX = None  # set to a Chromium path if Playwright's own browser isn't installed
async def step(pg):
    for sel in ['[data-act=handoffGo]', '[data-act=coachOk]', '[data-act=seasonOk]', '[data-act=revealBids]']:
        loc = pg.locator(sel)
        if await loc.count():
            await loc.first.click(); return sel
    conf = pg.locator('[data-act=confirm]')
    if not await conf.count(): return None
    h3 = (await pg.locator('.prompt h3').first.inner_text()).lower()
    if 'bid' in h3 or 'seed' in h3:
        cards = pg.locator('.hand [data-act=selCard]')
        if await cards.count(): await cards.first.click()
    elif 'lot' in h3: await pg.locator('[data-act=selLot]').first.click()
    elif 'order' in h3:
        rec = pg.locator('.opt.rec')
        await (rec.first if await rec.count() else pg.locator('[data-act=selOpt]').first).click()
    elif 'keep' in h3: await pg.locator('.prompt [data-act=selCard]').first.click()
    if await conf.is_enabled(): await conf.click(); return h3
    return None
async def until_results(pg, n=4000, extra=None):
    for _ in range(n):
        await pg.wait_for_timeout(25)
        if await pg.locator('.results h1').count(): return True
        if extra and await extra(pg): continue
        await step(pg)
    return False
def launch_args():
    return {'executable_path': EX} if EX else {}

# Shared helper: performs whatever action the page is asking for (first legal choice).
# Clicks use a short timeout: the page re-renders often, and a click that lands mid-render is simply retried on the next step.
EX = None  # set to a Chromium path if Playwright's own browser isn't installed
T = 3000
async def _step(pg, skip_ack=False):
    for sel in ['[data-act=handoffGo]', '[data-act=coachOk]', '#overlay [data-act=seasonOk]', '[data-act=seasonOk]', '#overlay [data-act=ackOk]', '[data-act=ackOk]', '[data-act=revealBids]']:
        if skip_ack and 'ackOk' in sel: continue
        loc = pg.locator(sel)
        if await loc.count():
            await loc.first.click(timeout=T); return sel
    conf = pg.locator('[data-act=confirm]')
    if not await conf.count(): return None
    h3 = (await pg.locator('.prompt h3').first.inner_text(timeout=T)).lower()
    if 'bid' in h3 or 'seed' in h3:
        cards = pg.locator('.hand [data-act=selCard]')
        if await cards.count(): await cards.first.click(timeout=T)
    elif 'lot' in h3: await pg.locator('[data-act=selLot]').first.click(timeout=T)
    elif 'order' in h3:
        rec = pg.locator('.opt.rec')
        await (rec.first if await rec.count() else pg.locator('[data-act=selOpt]').first).click(timeout=T)
    elif 'keep' in h3: await pg.locator('.prompt [data-act=selCard]').first.click(timeout=T)
    if await conf.is_enabled(): await conf.click(timeout=T); return h3
    return None
async def step(pg, skip_ack=False):
    try: return await _step(pg, skip_ack)
    except Exception as e:
        if 'Timeout' in type(e).__name__ or 'Timeout' in str(e) or 'detached' in str(e): return None
        raise
async def until_results(pg, n=4000, extra=None):
    for _ in range(n):
        await pg.wait_for_timeout(25)
        if await pg.locator('.results h1').count(): return True
        if extra and await extra(pg): continue
        await step(pg)
    return False
def launch_args():
    return {'executable_path': EX} if EX else {}

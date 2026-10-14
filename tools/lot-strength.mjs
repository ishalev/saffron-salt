// Lot strength by rollouts: at sampled auctions the first picker is forced to take each lot,
// and the game is replayed K times with a reshuffled deck. Strength = effect on that player's
// final margin over the average opponent, relative to the other lots in the same market.
// Long runs: split into chunks with START, each writes lot-rows-<players>-<start>.json; then run merge-lot-strength.mjs.
// Usage: node tools/lot-strength.mjs <games> <K> <players> <start>
import { Game, BotAgent, hashSeed } from './engine.mjs';
import { writeFileSync } from 'fs';
const [GAMES = 50, K = 12, n = 3, START = 0] = process.argv.slice(2).map(Number);
const mk = () => Array.from({ length: n }, (_, i) => ({ name: 'B' + i, agent: BotAgent }));
const suitOf = h => h >= 79 ? 'coin' : h >= 74 ? 'saffron' : h >= 66 ? 'curry' : h >= 57 ? 'oregano' : h >= 47 ? 'turmeric' : h >= 35 ? 'garlic' : h >= 20 ? 'cinnamon' : 'chili';
const typeOf = h => h === 83 ? 'Coin 83' : h >= 81 ? 'Coin 81/82' : h >= 79 ? 'Coin 79/80' : suitOf(h)[0].toUpperCase() + suitOf(h).slice(1);
async function baseline(seed) {
  const g = new Game({ seed, players: mk() }); const recs = [];
  g.hooks.pause = async (kind, bids) => { if (kind === 'reveal' && bids[0].owner !== 'bot') recs.push({ s: g.season, a: g.auction, p: bids[0].idx, lots: g.market.map(l => l.cards[0].c.n) }); };
  await g.run(); return recs;
}
async function rollout(seed, t, head, rseed) {
  let forced = false; const players = mk();
  players[t.p].agent = { decide(gg, i, req) {
    if (!forced && req.type === 'lot' && gg.season === t.s && gg.auction === t.a) { forced = true; const l = gg.market.find(x => x.cards[0].c.n === head); gg.rngState = hashSeed(rseed); gg.shuffle(gg.deck); return l.id; }
    return BotAgent.decide(gg, i, req);
  } };
  const r = await new Game({ seed, players }).run();
  const others = r.players.filter((_, k) => k !== t.p).map(p => p.score); if (r.bot) others.push(r.bot.score);
  return r.players[t.p].score - others.reduce((a, b) => a + b, 0) / others.length;
}
const rows = [];
for (let k = START; k < START + GAMES; k++) {
  const seed = `lots-${n}-${k}`;
  for (const t of (await baseline(seed)).filter(r => r.lots.some(h => h >= 74) || k % 4 === 0).slice(0, 3)) {
    const eq = {};
    for (const h of t.lots) { let s = 0; for (let j = 0; j < K; j++) s += await rollout(seed, t, h, `${seed}-${t.s}-${t.a}-${j}`); eq[h] = s / K; }
    const vals = Object.values(eq), m = vals.reduce((a, b) => a + b, 0) / vals.length, best = Math.max(...vals);
    for (const h of t.lots) rows.push({ n, s: t.s, type: typeOf(h), rel: eq[h] - m, isBest: eq[h] === best, options: t.lots.length });
  }
}
writeFileSync(`lot-rows-${n}-${START}.json`, JSON.stringify(rows));
console.log(`Wrote lot-rows-${n}-${START}.json (${rows.length} evaluations).`);

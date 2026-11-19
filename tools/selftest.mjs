// Engine self-test: same seed gives the same game, replays reproduce exactly, no cards lost,
// and the demo seed still deals every player a pair, a Saffron or coin card, and a salted double.
// Usage: node tools/selftest.mjs
import { Game, BotAgent, RULES_VERSION, DEMO_SEED, DEMO_PLAYERS, demoHandOk } from './engine.mjs';
const mk = n => Array.from({ length: n }, (_, i) => ({ name: 'B' + i, agent: BotAgent }));
let ok = true;
for (const n of [2, 3, 4, 5]) for (let k = 0; k < 5; k++) {
  const seed = `selftest-${n}-${k}`;
  const g1 = new Game({ seed, players: mk(n) }); const a = await g1.run();
  const b = await new Game({ seed, players: mk(n) }).run();
  const g3 = new Game({ seed, players: mk(n), replay: a.decisions }); const c = await g3.run();
  const pass = a.log.join() === b.log.join() && a.log.join() === c.log.join() && g1.cardCount() === 83 && g3.cardCount() === 83;
  if (!pass) { ok = false; console.log(`FAIL ${seed}`); }
}
{
  let hands = null;
  const peek = { decide(g, i, req) { if (req.type === 'seed' && !hands) hands = g.players.map(p => p.hand.slice()); return BotAgent.decide(g, i, req); } };
  await new Game({ seed: DEMO_SEED, players: Array.from({ length: DEMO_PLAYERS }, (_, i) => ({ name: 'B' + i, agent: peek })) }).run();
  const bad = hands.map((h, i) => (demoHandOk(h) ? null : i + 1)).filter(Boolean);
  if (bad.length) { ok = false; console.log(`FAIL demo seed ${DEMO_SEED}: seat(s) ${bad.join(', ')} lack a pair + Saffron/coin + salted double`); }
}
// v1.22a options: G8 (specialization bonus off) and T2 (final auction endgame), alone and together.
let optGames = 0;
for (const variants of [{ spec: false }, { endgame: 'auction' }, { spec: false, endgame: 'auction' }]) for (const n of [2, 3, 4, 5]) for (let k = 0; k < 2; k++) {
  const seed = `selftest-opt-${n}-${k}`, tag = `${seed} ${JSON.stringify(variants)}`;
  const g1 = new Game({ seed, players: mk(n), variants }); const a = await g1.run();
  const g2 = new Game({ seed, players: mk(n), variants, replay: a.decisions }); const c = await g2.run();
  optGames++;
  const fail = msg => { ok = false; console.log(`FAIL ${tag}: ${msg}`); };
  if (a.log.join() !== c.log.join()) fail('replay differs');
  if (g1.cardCount() !== 83) fail(`card count ${g1.cardCount()}`);
  if (variants.spec === false && a.players.some(p => p.breakdown.spec)) fail('specialization scored while off');
  if (variants.endgame === 'auction') {
    if (a.players.some(p => p.breakdown.cashout) || (a.bot && a.bot.breakdown.cashout)) fail('cash-out scored with the final auction');
    const labels = a.history.map(h => h.label);
    if (!(labels.indexOf('S3 A3') < labels.indexOf('Final auction') && labels.indexOf('Final auction') < labels.indexOf('S3 end'))) fail(`history order ${labels.join(',')}`);
    const buys = a.log.filter(l => l.startsWith('[S3 Final]') && / buys lot /.test(l)).length;
    if (buys !== n + (n === 2 ? 1 : 0)) fail(`${buys} lots bought in the final auction`);
    if (a.decisions.some(d => d.s === 3 && d.a === 4 && d.type === 'store')) fail('stored a card in the final auction');
  }
}
// U20: lots keep their market number when earlier lots are bought.
{
  const g = new Game({ seed: 'selftest-lots', players: mk(4) }); const a = await g.run();
  const bad = a.log.filter(l => / buys lot (\d+)/.test(l) && !(+l.match(/ buys lot (\d+)/)[1] >= 1 && +l.match(/ buys lot (\d+)/)[1] <= 4));
  const seen = new Map(); for (const l of a.log) { const m = l.match(/^\[(S\d A\d)\] .* buys lot (\d+)/); if (m) { const s = seen.get(m[1]) || new Set(); if (s.has(m[2])) bad.push(l); s.add(m[2]); seen.set(m[1], s); } }
  if (bad.length) { ok = false; console.log(`FAIL lot numbers: ${bad[0]}`); }
}
console.log(ok ? `All checks passed (version ${RULES_VERSION}, ${20 + optGames} games incl. ${optGames} with options, demo seed ${DEMO_SEED}).` : 'Some checks FAILED.');
process.exit(ok ? 0 : 1);

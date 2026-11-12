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
console.log(ok ? `All checks passed (version ${RULES_VERSION}, 20 games, demo seed ${DEMO_SEED}).` : 'Some checks FAILED.');
process.exit(ok ? 0 : 1);

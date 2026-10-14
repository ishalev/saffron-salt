// Engine self-test: same seed gives the same game, replays reproduce exactly, no cards lost.
// Usage: node tools/selftest.mjs
import { Game, BotAgent, RULES_VERSION } from './engine.mjs';
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
console.log(ok ? `All checks passed (version ${RULES_VERSION}, 20 games).` : 'Some checks FAILED.');
process.exit(ok ? 0 : 1);

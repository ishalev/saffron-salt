import { Game, BotAgent } from 'file:///C:/Users/ishal/OneDrive/Documents/GitHub/saffron-salt/tools/engine.mjs';
const SP = ['ginger','cardamom','clove','nutmeg','sumac','anise','fennel','pepper'];
const out = []; const C = {};
for (let k = 1; k <= 6000; k++) {
  const seed = `${SP[k % 8]}-${SP[(k * 3 + 1) % 8]}-${k}`;
  const g = new Game({ seed, players: Array.from({ length: 4 }, (_, i) => ({ name: `Bot ${i + 1}`, agent: BotAgent })), botRules: { seasonAdvance: 'notLeadingNoSaffron', scoring: true } });
  await g.run();
  const L = g.log;
  const S1 = L.filter(l => /^\[S1 A\d\]/.test(l));
  // first auction only
  const rev = L.find(l => l.startsWith('[S1 A1] Bids revealed'));
  const parts = rev.replace(/.*revealed: /, '').split(' | ');
  const top = parts[0];
  const m = top.match(/pair \w+ (\d+).* \+ \w+ (\d+)/);
  if (!m) continue;
  const hi = Math.max(+m[1], +m[2]);
  const singles = parts.slice(1).filter(p => !/pair/.test(p)).map(p => +p.match(/: \w+ (\d+)/)[1]);
  if (!singles.some(s => s > hi)) continue;
  C.pair = (C.pair || 0) + 1;
  const S12 = L.filter(l => /^\[S[12] A\d\]/.test(l)); const knock = S12.findIndex(l => /» Bot \d knocks Bot \d down/.test(l));
  if (knock < 0) continue;
  const salt = S1.some(l => /blocked by salt/.test(l)), skip = S1.some(l => /skips [3-9] spaces/.test(l));
  if (!salt || !skip) continue;
  const spec = L.filter(l => /untouched track/.test(l)).map(l => +l.match(/(\d) untouched/)[1]);
  const ci = L.findIndex(l => /Final cash-out/.test(l));
  out.push(`${seed} | ${parts.join(' | ')} | ${S12[knock].trim()} | cash1: ${L[ci + 1].trim()} | spec ${spec.join('')}`);
}
console.log(C); console.log(out.slice(0, 20).join('\n'), '\n', out.length);

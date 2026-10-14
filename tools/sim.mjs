// Batch simulation with bots in every seat; prints a Markdown report.
// Usage: node tools/sim.mjs [games=500] [counts=2,3,4,5] [botRule=notLeadingNoSaffron] [saffronCube=1] [botScoring=1]
import { Game, BotAgent, SPICES, SUIT_NAME, RULES_VERSION } from './engine.mjs';
const [N = 500, counts = '2,3,4,5', botRule = 'notLeadingNoSaffron', cube = '1', botScoring = '1'] = process.argv.slice(2);
const mean = a => a.reduce((x, y) => x + y, 0) / (a.length || 1);
const pct = x => `${Math.round(100 * x)}%`, f1 = x => x.toFixed(1);
const out = [`# Saffron Salt simulation`, `Version ${RULES_VERSION}. ${N} games per player count. Deck Bot rule ${botRule}${botScoring === '1' ? '' : ' (not scoring)'}; Saffron cube ${cube === '1' ? 'on' : 'off'}.`, ''];
for (const n of counts.split(',').map(Number)) {
  const games = [];
  for (let k = 1; k <= +N; k++) games.push(await new Game({ seed: `sim-${n}-${k}`, players: Array.from({ length: n }, (_, i) => ({ name: `Bot ${i + 1}`, agent: BotAgent })), botRules: { seasonAdvance: botRule, scoring: botScoring === '1' }, variants: { saffronCube: cube === '1' } }).run());
  const ps = games.flatMap(g => g.players.map((p, i) => ({ ...p, w: g.winners.includes(i) ? 1 / g.winners.length : 0 })));
  const win = games.map(g => Math.max(...g.players.map(p => p.score)));
  const grp = f => { const a = ps.filter(f); return a.length ? `${pct(mean(a.map(x => x.w)))} (${a.length})` : '–'; };
  out.push(`## ${n} players`,
    `- Average score ${f1(mean(ps.map(p => p.score)))}; average winning score ${f1(mean(win))}`,
    `- Win rate by seat: ${Array.from({ length: n }, (_, i) => pct(mean(games.map(g => (g.winners.includes(i) ? 1 / g.winners.length : 0))))).join(', ')}`,
    `- Points by source: ${['top', 'lead', 'moq', 'coin', 'cashout', 'spec'].map(k => `${k} ${f1(mean(ps.map(p => p.breakdown[k])))}`).join(', ')}`,
    `- Specialization: ${f1(mean(ps.map(p => p.breakdown.spec)))} points per player (${pct(mean(ps.map(p => p.breakdown.spec)) / mean(ps.map(p => p.score)))} of score); winners ${f1(mean(ps.filter(p => p.w > 0).map(p => p.breakdown.spec)))} vs others ${f1(mean(ps.filter(p => p.w === 0).map(p => p.breakdown.spec)))}`,
    `- Win rate by untouched tracks (players): none ${grp(p => p.untouched === 0)}, one ${grp(p => p.untouched === 1)}, two ${grp(p => p.untouched === 2)}, three+ ${grp(p => p.untouched >= 3)}; fair share ${pct(1 / n)}`,
    ...(n === 2 ? [`- Deck Bot: average ${f1(mean(games.map(g => g.bot.score)))}; beats both players ${pct(mean(games.map(g => +(g.bot.score > Math.max(...g.players.map(p => p.score))))))}`] : []),
    '', '| Track | Player sole lead | No leader | Avg final space |', '|---|---|---|---|',
    ...SPICES.map(s => { const L = games.flatMap(g => g.seasonLeaders.map(x => x[s])); return `| ${SUIT_NAME[s]} | ${pct(mean(L.map(x => +(!!x && x !== 'bot'))))} | ${pct(mean(L.map(x => +!x)))} | ${f1(mean(ps.map(p => p.finalPos[s])))} |`; }), '');
}
console.log(out.join('\n'));

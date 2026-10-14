// Compare Deck Bot season-end rules in 2-player games.
// Usage: node tools/deckbot.mjs [games=1000] [rules=notLeadingNoSaffron,all,noSaffron,saltedNoSaffron,draw3]
import { Game, BotAgent } from './engine.mjs';
const [N = 1000, rules = 'notLeadingNoSaffron,all,noSaffron,saltedNoSaffron,draw3'] = process.argv.slice(2);
console.log('| Rule | Bot avg | Players avg | Bot beats both |\n|---|---|---|---|');
for (const rule of rules.split(',')) {
  let b = 0, p = 0, beat = 0;
  for (let k = 0; k < +N; k++) {
    const r = await new Game({ seed: 'deckbot-' + k, players: [0, 1].map(i => ({ name: 'B' + i, agent: BotAgent })), botRules: { seasonAdvance: rule } }).run();
    b += r.bot.score; const ps = r.players.map(x => x.score); p += (ps[0] + ps[1]) / 2; if (r.bot.score > Math.max(...ps)) beat++;
  }
  console.log(`| ${rule} | ${(b / N).toFixed(1)} | ${(p / N).toFixed(1)} | ${Math.round(100 * beat / N)}% |`);
}

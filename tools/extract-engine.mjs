// Pulls the rules engine and bots out of game/index.html into tools/engine.mjs,
// so the simulation and analysis scripts always use the exact released game logic.
// Usage: node tools/extract-engine.mjs
import { readFileSync, writeFileSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';
const here = dirname(fileURLToPath(import.meta.url));
const html = readFileSync(join(here, '..', 'game', 'index.html'), 'utf8');
const script = html.slice(html.indexOf('<script type="module">') + '<script type="module">'.length, html.lastIndexOf('</script>'));
const cut = script.indexOf('// ================= UI');
if (cut < 0) throw new Error('Could not find the UI marker in index.html');
const engine = script.slice(0, cut) + `
export { Game, BotAgent, BotAgentV1, BOT_TUNING, SPICES, SUIT_NAME, TRACKS, CARDS, RULES_VERSION, ENGINE_VERSION, hashSeed, leaderOf };
`;
writeFileSync(join(here, 'engine.mjs'), engine);
const v = (engine.match(/RULES_VERSION = '([^']+)'/) || [])[1];
console.log(`Wrote tools/engine.mjs (version ${v}).`);

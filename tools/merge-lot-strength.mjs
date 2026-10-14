// Merge lot-rows-*.json files into a table. Usage: node tools/merge-lot-strength.mjs
import { readFileSync, readdirSync } from 'fs';
const rows = readdirSync('.').filter(f => /^lot-rows-\d+-\d+\.json$/.test(f)).flatMap(f => JSON.parse(readFileSync(f)));
const mean = a => a.reduce((x, y) => x + y, 0) / a.length;
const sd = a => { const m = mean(a); return Math.sqrt(a.reduce((x, y) => x + (y - m) ** 2, 0) / Math.max(1, a.length - 1)); };
const g = {}; for (const r of rows) (g[r.type] ||= []).push(r);
console.log(`${rows.length} lot evaluations\n\n| Lot | vs. average option (95% range) | Best choice | Par |\n|---|---|---|---|`);
for (const [k, v] of Object.entries(g).sort((a, b) => mean(b[1].map(x => x.rel)) - mean(a[1].map(x => x.rel)))) {
  const rel = v.map(x => x.rel);
  console.log(`| ${k} | ${mean(rel) >= 0 ? '+' : ''}${mean(rel).toFixed(1)} (±${(1.96 * sd(rel) / Math.sqrt(v.length)).toFixed(1)}) | ${Math.round(100 * mean(v.map(x => +x.isBest)))}% | ${Math.round(100 * mean(v.map(x => 1 / x.options)))}% |`);
}

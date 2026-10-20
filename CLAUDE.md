# Saffron Salt — working brief for Claude

Read this first in every session. It replaces the context that used to live in Isaac's claude.ai Project.

## The project

- **Saffron Salt** is a spice-trading auction board game designed by **Isaac** (owner of this repository, GitHub `ishalev`) and his co-designer **Mitch**. They playtest together, including two-player games against the Deck Bot.
- This repository holds the **digital playtest edition**: a single-page browser game for playtesting and demos. It is **not** a commercial product: don't overdesign for scale.
- Live site: **https://kindfortress.com/saffron-salt/** (WordPress site on Bluehost shared hosting; PHP available, no Node.js).
- The analog rules document (v1.20) is in Isaac's Google Drive folder "Saffron Salt". The digital rules have moved on since; [docs/RULES.md](docs/RULES.md) is the current rules as implemented.
- Design decisions, open issues, rejected ideas and all test results: [docs/DECISIONS.md](docs/DECISIONS.md). This is the **single source of truth**; the older Claude Doc copy is archived.

## Start of every session

1. Pull the latest from GitHub.
2. Check the version in `RELEASES.md`, the top of `docs/DECISIONS.md`, and `RULES_VERSION` in `game/index.html` all agree. If they don't, stop and tell Isaac.
3. Run `node tools/extract-engine.mjs` then `node tools/selftest.mjs` before changing anything.

## Working agreements

- **Nothing gets built until Isaac authorizes it.** When he gives feedback or ideas, file them as planned items in `docs/DECISIONS.md` (with an ID: G = gameplay, U = UI, T = test before inclusion, D = deferred, N = found in testing, R = rejected) and confirm. Build only when he says go.
- **Surface questions before building**, with a proposed default for each, so he can answer only where he disagrees.
- **Versioning:** the version string is `RULES_VERSION` in `game/index.html` (currently `1.21c`). Minor changes increment the letter (1.21c → 1.21d). **Isaac decides when the number changes.** Any change that alters setup or rules gets a new letter, because it breaks replays recorded under the old version.
- **Decisions log:** every decision gets a dated row with the version, the decision, and the reasoning and evidence. Closed issues move to "Closed in vX". Record test results with method and sample size.
- **Writing style for Isaac:** plain language; lead with the answer; short tables for comparisons; say what you couldn't test.
- Isaac often dictates; expect filler words and occasional mis-transcriptions, and ask when something is ambiguous rather than guessing.

## Release checklist

A release isn't done until every step is complete.

1. Make the changes in `game/` (and `tools/` if needed). Bump `RULES_VERSION`.
2. Run `node tools/extract-engine.mjs`, `node tools/selftest.mjs`, then the browser tests (`tools/browser-tests/serve.sh`, or `serve.ps1` on Windows; then `test_local.py`, `test_online.py`; Windows commands in [tools/README.md](tools/README.md)). Add or update tests for new behavior. All must pass.
3. Update `RELEASES.md` (one line), `docs/DECISIONS.md` (decision row, closed items, any test results), and `docs/RULES.md` if rules changed.
4. Commit with message `vX.YYz: short summary`, push, and tag `vX.YYz`.
5. Tell Isaac which files to deploy to the server: usually just `game/index.html`. Deployment to Bluehost is currently manual (cPanel File Manager → `saffron-salt` folder). An automatic GitHub Actions deploy is a possible next step but is not set up.

## Safety rules

- **Never commit the real `feedback.php`.** The server copy contains Isaac's notification email and review password. The repository holds only the template with `you@example.com` / `change-me`. Never put credentials, tokens or passwords in the repository, commit messages or logs.
- Never overwrite the server's `feedback.php` when deploying.
- `relay.php`, `games.php` and `feedback.php` create data folders (`saffron-tables`, `saffron-games`, `saffron-feedback`) protected by `.htaccess`. Keep that protection.

## How the code is organized

- `game/index.html` is the whole game in one self-contained file (no build step): CSS, then a single `<script type="module">` containing, in order:
  1. **Rules engine** (`Game` class, deck, tracks, scoring, the Deck Bot, seeded RNG) and **bot AI** (`BotAgent`, style `v2`; `BotAgentV1` kept for comparison). Everything before the `// ================= UI` marker. `tools/extract-engine.mjs` relies on that marker.
  2. **UI**: rendering, animations, walkthrough, results, game logs, simulator, replay loading.
  3. **Online play**: host-authoritative; the host's browser runs the game; guests send choices via presence; backend is `relay.php` (polling) when self-hosted.
  4. **Feedback form** and rules reference text.
- Engine conventions: track spaces numbered from the bottom (1 = start); all randomness through the seeded RNG; every decision goes through `decide`/`decideAll` and is recorded, so `seed + decisions` reproduces a game exactly. Keep it that way.
- `window.__fast = true` (set by the browser tests) skips animation delays.

## Players' feedback and game records

- Players submit feedback after each game; it's emailed to Isaac and reviewable at `/saffron-salt/feedback.php` (password-protected).
- Finished games are stored per browser and on the server via `games.php`; the "All games on this site" view uses the same password.

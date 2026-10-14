# Tools

Everything here works from `game/index.html`, so results always match the released game.

## Setup (once)

- Node.js 18 or later
- For browser tests: Python 3, `pip install playwright`, then `python -m playwright install chromium`, and PHP 7.4+ (`php -S`)

## Rules engine

```
node tools/extract-engine.mjs     # writes tools/engine.mjs from game/index.html (re-run after every new release)
node tools/selftest.mjs           # same seed = same game, replays reproduce exactly, all 83 cards accounted for
```

## Simulation and analysis

```
node tools/sim.mjs 500 2,3,4,5                       # balance report: scores, sources, specialization, track leads
node tools/sim.mjs 500 2,3 notLeadingNoSaffron 0     # same, without the Saffron cube
node tools/deckbot.mjs 1000                          # compare Deck Bot season-end rules (2 players)
node tools/lot-strength.mjs 50 12 3 0                # lot strength: 50 games, 12 replays, 3 players, chunk start 0
node tools/merge-lot-strength.mjs                    # combine all lot-rows-*.json chunks into a table
```

Lot strength is slow: run it in chunks (different start values) and merge.

## Browser tests

```
cd tools/browser-tests
./serve.sh &               # test copy of game/ at http://localhost:8772 (test password pw123)
python3 test_local.py      # single device, feedback, game logs, replay, pass-and-play change
python3 test_online.py     # host and guest in two browsers, both change a choice, results must match
```

## Restoring after a lost workspace

1. Download the repository (Code → Download ZIP) or read it from GitHub.
2. Check `RELEASES.md` and the Issues and Decisions Log agree on the current version.
3. Run `extract-engine.mjs` and `selftest.mjs` before changing anything.

# Saffron Salt — Issues and Decisions Log

**Current release: v1.21c** (Oct 9, 2026). This file is the single source of truth from Oct 14, 2026; it was moved here from the Claude Doc "Saffron Salt — Issues and Decisions Log", which is now an archived copy.

## How to use this log

Every issue and decision is tied to the version it was found in or tested on.

- **Status values:** Planned (accepted, scheduled for a version), To test (needs a simulation before a decision), Deferred, Rejected, Closed (shipped or resolved).
- **IDs:** G = gameplay, U = UI, T = test before inclusion, D = deferred, N = found in testing, R = rejected. IDs stay fixed once assigned; continue numbering from the highest used (G7, U18, T1, D5, N3, R5).
- **Sources:** Isaac's in-chat feedback, Isaac–Mitch playtest calls (Oct 6, 2026, [recording](https://fathom.video/calls/848473309)), and simulations.
- **Updating:** when a decision is made or an issue closes, add a dated row to the Decisions log, move the issue, and record any test results with method and sample size.

## Open issues

### Planned for the next build

None.

### Awaiting a decision

| ID | Issue | Found in | Evidence |
| --- | --- | --- | --- |
| N2 | +1 spice lots are weak: Curry −2.5, Turmeric −3.2, Oregano −3.3 vs. the average option; best choice only 13–16% of the time. No fix decided yet. | v1.21a | Lot strength, v1.21a |

### Deferred

| ID | Issue | Source |
| --- | --- | --- |
| D1 | Extra neutral cube on Chili, so a player knocked from the top can realistically climb back. Proposed metric: how often a knocked-down player regains the lead or top. | Mitch, call |
| D2 | Salt logjams in 2-player games with the bot. Ideas: salt on one icon of a double, or fewer salted cards. | Isaac and Mitch, call |
| D3 | Simulator report clarity: explain each figure; drop columns with no information (player leads read 100% at 3+ players). | Mitch, call |
| D4 | Universal rule: the base card of any lot cannot be stored (G4 applies it to Saffron and coins only). | Isaac, call |
| D5 | Option to store the top card of the deck instead of a card from the lot. Mitch was against it: it weakens the link between choosing a lot and what you store. | Isaac, call |

### Infrastructure (not game changes)

| Item | Status |
| --- | --- |
| Automatic deploy to kindfortress.com via GitHub Actions on each release tag (FTP credentials as repository secrets; never touches `feedback.php`) | Proposed, not set up |

## Decisions log

Newest first. "Version" is the version the decision was tested on or applies from.

| Date | Version | Decision | Reasoning and evidence |
| --- | --- | --- | --- |
| Oct 14, 2026 | v1.21c | Build and release work moves to Claude Code; this log, the rules (`docs/RULES.md`) and the working brief (`CLAUDE.md`) move into the repository. The Claude Doc log is archived. | Isaac doesn't want to update GitHub by hand each release. Claude Code commits, tags and pushes with Isaac's own GitHub sign-in; keeping the log in the repository lets it be updated with each release. |
| Oct 14, 2026 | v1.21c | Project archive is the public GitHub repository `ishalev/saffron-salt` (game files, tools, RELEASES.md). A release isn't done until it's committed and tagged; each session starts by checking the repository's version against this log. | A workspace reset lost the working test and analysis scripts (the game itself was recoverable from the released file). Public so Claude can read it directly. The real feedback.php is never committed; the repository holds a template. |
| Oct 9, 2026 | v1.21c | Released v1.21c (U15, G7, U16, U17, U18). Only index.html changes. | Authorized by Isaac. Tested in a browser against a local copy of the PHP setup: single device, pass-and-play with a changed market card, and online where host and guest both changed their market card and their bid (identical results). Replays exact; all 83 cards accounted for at every player count. |
| Oct 7, 2026 | v1.21b | Released v1.21b: Saffron cube (T1) standard in 2–3 player games; simulator reports specialization records. Only index.html changes. | Requested as an addition to the 1.21a build; numbered 1.21b because the setup change means 1.21a replays can't reproduce under the new rules. Verified: cube on Saffron space 4 at 2–3 players only; replays exact; all 83 cards accounted for. |
| Oct 7, 2026 | v1.21a | N1 closed: Coin 83 stays as is (+7 points, +1 faceup extra card). | It's an outlier (+4.6 vs. average, best 63%), but it's a single card and its value doesn't look game-winning. Being clearly the best lot creates a good decision: whether your hand's bids can win it, or whether to keep your powder dry, close to a Nash-equilibrium style choice. |
| Oct 7, 2026 | v1.21a | N3 closed: Deck Bot strength accepted for now (beats both players about 15% of the time). | A 15% win rate is acceptable; no rule change. |
| Oct 7, 2026 | v1.21a | T1 adopted: neutral cube on Saffron space 4 in 2–3 player games. | Measured impact is modest (scores +1.5 to +2; Saffron investment pays better), but it's psychologically useful and meaningful on the board. |
| Oct 7, 2026 | v1.21a | G6 bot specialization level accepted; no further bot tuning. | Anecdotally similar to humans, who also rarely keep three tracks untouched. Specialization rises steadily with player count (see Test results). |
| Oct 7, 2026 | v1.21a | Released v1.21a (G1–G6, U1–U14) for kindfortress.com: index.html updated, games.php added. | Authorized by Isaac. Browser-tested: single device, pass-and-play with bid changes, online with bid undo (host and guest, identical results), walkthrough, game logs (local and server), replay, feedback, standalone file. |
| Oct 7, 2026 | v1.21a | G6 bots: pick up to 3 untouched tracks to keep for the specialization bonus (those they hold fewest cards for, preferring crowded tracks); value the bonus more at 3+ players; discount leads on crowded tracks. | Head-to-head, one new bot vs. old bots won 108% (2p), 106% (3p), 128% (4p), 126% (5p) of its fair share. Specialization points per player rose about 50–70%. |
| Oct 7, 2026 | v1.21a | T1 tested as: neutral cube on Saffron space 4 (one empty space above the MOQ), 2–3 players only. | Placement specified by Isaac. |
| Oct 7, 2026 | v1.21a | Accepted G5, G6, U12, U13, U14 (cash-out shown in season 3 only); T1 to test after G6; deferred D1–D5; rejected R1–R3. | Triage of the Isaac–Mitch call. G6 was a prerequisite for T1 because the old bots didn't pursue specialization. |
| Oct 7, 2026 | v1.21a | G4: Saffron and coin lots get faceup extra cards; their base card can't be stored and is shown sideways. | Facedown extras made these lots weak and random (Saffron −3.3 vs. average option, best 15%). The no-store rule prevents a Saffron cycling engine. |
| Oct 7, 2026 | v1.21a | G3: facedown cards never move anyone; facedown coins are not cashed. | Rules as written; the build had applied them by mistake. Found in play by Isaac and Mitch. |
| Oct 7, 2026 | v1.21a | Coin lots unchanged (83 stays 7 points). | Not outliers under the facedown rules: Coin 83 +1.1, Coins 81/82 −0.8, Coins 79/80 −0.6 vs. average option. |
| Oct 7, 2026 | v1.21a | U1 "recommended" = Pareto improvement in your own track positions; more points breaks ties. | Not meant as a hard puzzle, but order must stay visible because analog players need to understand it. |
| Oct 7, 2026 | v1.21a | Builds target kindfortress.com only; the claude.ai link stays at v1.20d. | Isaac uses the self-hosted version. |
| Oct 6, 2026 | v1.20d | Online tables use five seats (Human, Bot, Nobody); two filled seats adds the Deck Bot. | Lets the host set the player count in the waiting room. |
| Oct 6, 2026 | v1.20c | Player feedback form after each game; email notification and password-protected review on kindfortress.com. | Playtesting with outside players. |
| Oct 6, 2026 | v1.20b | Removed the "4" neutral cube from Curry. | Bot comparisons barely moved (players −1 point). |
| Oct 6, 2026 | v1.20b | Deck Bot season-end rule: advance one space on each track it isn't leading, never Saffron; a tie counts as not leading. | Bot beat both players ~23% of the time then. "Every track" was too strong (75%); "except Saffron" alone 47%; draw-N rules are a clean dial but tedious in analog play; salted advances too weak (0%). |
| Oct 6, 2026 | v1.20 | Ties for the lead score nothing, and can only occur on the start space. | Once any marker reaches the top, someone always holds it; confirmed in 4,000 simulated games (84,000 scorings, 122 ties, all on space 1). |

## Rejected ideas

| ID | Idea | Rejected | Reasoning |
| --- | --- | --- | --- |
| R1 | Automated Deck Bot that picks its own lot at random. | Oct 7, 2026 | Random removal makes markets hard to value and feels unfair: a one-in-three chance the bot takes the lot you bid big for. |
| R2 | Double icon on Saffron cards. | Oct 7, 2026 | A dealt Saffron would just be stored for two guaranteed Saffron steps. |
| R3 | Deck Bot always takes the last remaining lot. | Oct 7, 2026 | Barely changes bot strength, but removes the tension of choosing the bot's lot. |
| R4 | Deck Bot draws N cards at season end and applies them. | Oct 6, 2026 | A clean difficulty dial in simulation (draw 3: bot beats both 2%; draw 5: 12–16%), but too tedious in analog play. |
| R5 | Deck Bot advances as if salted at season end. | Oct 6, 2026 | Too weak: about 55% of advances blocked; bot beats both 0% of the time. |

## Closed issues

### Closed in v1.21c

| ID | Issue | Resolution |
| --- | --- | --- |
| U15 | Home page layout | Play online is a large featured panel at the top of the left column; "New game" renamed "Play a local game" below it; other panels in the right column |
| G7 | Market seeding couldn't be changed | Same undo flow as bids: "Change card" online; "All market cards are chosen" step in pass-and-play |
| U16 | Animations too small; moments not in text | Larger labels and markers; a large banner names each major moment; the status box describes the move; the game log and Latest box get a highlighted line for every skip, MOQ, lead, top, knockdown and salt block |
| U17 | Scoring animations not tied to players | Each scorer's marker glows with a "+5 lead" / "+2 MOQ" label in their color; the banner names the scorers |
| U18 | Empty market showed wrong text | An empty market shows only its heading |
| — | Found in testing: a guest who changed a choice before the host received it could leave the game waiting | The guest's choice is simply asked for again |
| — | Found in testing: log lines during buying lost their auction number | Restored |

### Closed in v1.21b

| ID | Issue | Resolution |
| --- | --- | --- |
| T1 | Saffron not contested enough at 2–3 players | Neutral cube on Saffron space 4 in standard 2–3 player setup; simulator can still test without it |
| — | Simulator didn't report whether specialization wins | Report shows specialization points, share of score, winners' vs. others' specialization, and win rate by untouched tracks |

### Closed in v1.21a

| ID | Issue | Resolution |
| --- | --- | --- |
| G1 | Next season's market visible during storage | Base cards only until storage ends; extras dealt after season scoring |
| G2 | No way to take back a bid | Undo until all bids are in, online and pass-and-play |
| G3 | Facedown cards moved players | Facedown cards never move or get cashed |
| G4 | Saffron and coin lots weak and random | All extras faceup; Saffron or coin base card sideways, not storable |
| G5 | Deck Bot bookkeeping | "Deck Bot keeps score" setting (on by default) |
| G6 | Bots ignored specialization | Planning bots |
| U1 | Card order hard to judge | Options show the cards; Pareto-better option marked Recommended |
| U2 | Movement hard to see | Step-by-step animation on the tracks |
| U3 | Big moments not visible | Distinct effects: skip, MOQ, lead, top, knockdown, salt block |
| U4 | Scores hid specialization | Potential bonus beside each score |
| U5 | No sign of your bid | Bid cards raised and labeled, with Undo where it applies |
| U6 | No season summary | Track-by-track scoring effects, then a season results table |
| U7 | No preview before buying | Ghost markers and a text summary of the best order |
| U8 | Deck Bot missing from statistics | Deck Bot column; the engine records its statistics |
| U9 | "Checkpoint" wording | "MOQ" everywhere, with tooltip |
| U10 | Season scores not exact | Score-by-season table with points gained |
| U11 | No game history | Game logs screen: this browser, plus all games on the site behind the feedback password |
| U12 | Unclear phase | Phase heading and pop-up notices |
| U13 | Stale highlights | Last-move rings fade; previews use dashed rings |
| U14 | Cash-out values unclear | Prizes shown during season 3 |

### Earlier

| Version | Issue | Resolution |
| --- | --- | --- |
| v1.20d | Host couldn't change the player count in the online waiting room | Five-seat lobby |
| v1.20c | No way for players to send feedback | Feedback form, email notice, review page |
| v1.20b | Deck Bot too strong (beat both players 70–75%) | New season-end rule |
| v1.20b | Track layout changed | Engine updated to the v1.20b board |
| v1.20 | Quit button did nothing (blocked browser popup) | In-page confirmation |
| v1.20 | Track order reversed on screen | Restored: Chili left, Saffron right |
| v1.20 | Market off to the side, far from the hand | Market centered, hand directly beneath |

## Test results

All runs use bots in every seat; human play may differ. Reproduce with the scripts in `tools/` (see `tools/README.md`).

### Specialization by player count (Oct 7, 2026; review of existing runs)

Specialization rises steadily with player count in every dataset. It isn't an artifact of the G6 tuning: the old bots show the same pattern.

| Players | Avg specialization points, old bots | Same, G6 bots | Players with 1+ untouched track (G6) | 3+ untouched (G6) | Share of avg score (G6) |
| --- | --- | --- | --- | --- | --- |
| 2 | 2.9 | 4.7 | 51% | 1% | 6% |
| 3 | 4.5 | 6.0 | 63% | 1% | 8% |
| 4 | 7.1 | 9.3 | 78% | 4% | 12% |
| 5 | 9.2 | 11.2 | 83% | 8% | 15% |

First read on whether it wins (v1.21b simulator, 100 games per count): players with more untouched tracks won more often at every count; three or more untouched won 69% of 4-player and 51% of 5-player games (fair shares 25% and 20%). A larger run would firm this up.

### v1.21a runs (Oct 7, 2026; G6 bots)

**Lot strength under G4.** At sampled auctions the first picker was forced to take each lot and the game was replayed 12 times with a reshuffled deck; strength is the effect on the buyer's final margin over the average opponent, relative to the other lots in the same market. About 4,100 evaluations (200 games at 2 and 3 players, 120 at 4). Par for best choice is about 31%.

| Lot | vs. average option (95% range) | Best choice |
| --- | --- | --- |
| Coin 83 (+7, +1) | +4.6 (±0.8) | 63% |
| Chili (+3) | +2.7 (±0.5) | 46% |
| Coin 81/82 (+5, +1) | +1.8 (±0.6) | 41% |
| Cinnamon (+2) | +0.6 (±0.6) | 32% |
| Garlic (+2) | +0.2 (±0.7) | 31% |
| Coin 79/80 (+2, +2) | +0.1 (±0.6) | 27% |
| Saffron (+1) | −1.3 (±0.6) | 23% |
| Curry (+1) | −2.5 (±0.6) | 13% |
| Turmeric (+1) | −3.2 (±0.6) | 15% |
| Oregano (+1) | −3.3 (±0.6) | 16% |

**Deck Bot rules** (1,000 two-player games each)

| Rule | Bot avg | Players avg | Bot beats both |
| --- | --- | --- | --- |
| Every track (v1.20 as written) | 94.5 | 76.2 | 68% |
| Every track except Saffron | 81.3 | 77.3 | 39% |
| Not leading, never Saffron (current) | 70.5 | 79.6 | 15% |
| Draw 3 | 53.0 | 82.8 | 2% |
| Salted, except Saffron | 46.0 | 85.1 | 1% |

**T1: Saffron cube on space 4** (800 games per row)

| Players | Cube | Avg score | Saffron leader changes per game | Players on Saffron | Avg final Saffron space | Win share: on Saffron vs. off |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | No | 79.2 | 0.56 | 1.84 of 2 | 4.72 | 50% vs. 54% |
| 2 | Yes | 81.4 | 0.53 | 1.81 of 2 | 4.98 | 51% vs. 39% |
| 3 | No | 78.6 | 0.66 | 2.21 of 3 | 3.85 | 33% vs. 35% |
| 3 | Yes | 80.0 | 0.64 | 2.19 of 3 | 4.02 | 35% vs. 29% |

### Earlier runs

**Lot strength, v1.20d rules with G3 applied** (Oct 7, 2026; about 10,000 evaluations, 16 replays, old bots): Chili +2.5, Coin 83 +1.1, Garlic +1.0, Cinnamon +0.4, Coin 79/80 −0.6, Coin 81/82 −0.8, Oregano −1.3, Turmeric −2.0, Curry −2.0, Saffron (+1 facedown) −3.3 (best only 15%). An earlier ~18,800-evaluation run gave the same ordering.

**Deck Bot rules, v1.20b board** (Oct 6, 2026; 1,000 games each, with the facedown bug): every track 98 vs. players 75, beats both 75%; except Saffron 84/76, 47%; not leading, never Saffron 74/78, 23%; draw 5 68/80, 12%; below MOQ only 70/82, 12%; draw 3 54/83, 2%; salted except Saffron 46/85, 0%.

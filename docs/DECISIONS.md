# Saffron Salt — Issues and Decisions Log

**Current release: v1.22b** (Nov 19, 2026). This file is the single source of truth from Oct 14, 2026; it was moved here from the Claude Doc "Saffron Salt — Issues and Decisions Log", which is now an archived copy.

## How to use this log

Every issue and decision is tied to the version it was found in or tested on.

- **Status values:** Planned (accepted, scheduled for a version), To test (needs a simulation before a decision), Deferred, Rejected, Closed (shipped or resolved).
- **IDs:** G = gameplay, U = UI, T = test before inclusion, D = deferred, N = found in testing, R = rejected. IDs stay fixed once assigned; continue numbering from the highest used (G8, U25, T2, D6, N4, R5).
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
| D6 | Alternatives to the no-store base rule, if it stays clunky after more playtesting: (a) no lot's base card can be stored; (b) no Saffron, coin or Curry card can be stored anywhere (needs a rule for lots with nothing storable). Isaac and Mitch keep the current rule for now; Mitch is adding a clear visual indicator to the rules text. | Isaac–Mitch debrief, Nov 19, 2026 ([recording](https://fathom.video/calls/908734495)) |

### Infrastructure (not game changes)

| Item | Status |
| --- | --- |
| Automatic deploy to kindfortress.com via GitHub Actions on each release tag (FTP credentials as repository secrets; never touches `feedback.php`) | Proposed, not set up |

## Decisions log

Newest first. "Version" is the version the decision was tested on or applies from.

| Date | Version | Decision | Reasoning and evidence |
| --- | --- | --- | --- |
| Nov 19, 2026 | v1.22b | Released v1.22b: U21–U25 (slower scoring with everyone-clicks-OK, final scoring reveal, taller log, prominent season results, reference card, pitch walkthrough). UI only; rules, setup and engine decisions are unchanged (the engine only records extra display data for the final panel). | Approved by Isaac after the Isaac–Mitch debrief. Engine self-test passes (44 games). Browser tests: new `test_pitch.py` (walkthrough forward and back, Start game, reference card, season and final panels, host waits for the guest's OK, identical results); `test_options.py`, `test_local.py`, `test_online.py` pass. The test driver now uses short click timeouts and retries, which also fixed the old `test_online.py` timing flake (4 of 4 runs pass). |
| Nov 19, 2026 | v1.22b | Approved U25: pitch walkthrough with Next and Back through every step, and a Start game button on each step that opens the publisher demo table. Planned for the next build. | Debrief with Mitch: a controlled screen-share walkthrough avoids showing hands; Isaac wants to move both ways and jump into a game anytime. |
| Nov 19, 2026 | v1.22b | Approved U24: on-screen reference card beside the hand, modeled on the printed card (ranges and quantities, no zero), with the bidding, order and scoring summary where it fits. Planned for the next build. | Isaac: the analog card's disguise role isn't needed digitally, but its content is. Printed card's Curry range (66–76) is a typo; the deck is 66–73. |
| Nov 19, 2026 | v1.22b | Approved U23: season results as a large centered panel for everyone, with tooltips on each point type and on the lead bonus. Planned for the next build. | Debrief with Mitch: the summary wasn't prominent and point values weren't explained. |
| Nov 19, 2026 | v1.22b | Approved U22: the Latest box shows the last 16 lines without scrolling. Planned for the next build. | Debrief with Mitch: the log scrolled during the pitch. |
| Nov 19, 2026 | v1.22b | Approved U21: one OK per season after track-by-track scoring; final scoring shows each player's cash-out bid, ranking and points, then specialization, and waits for OK. Planned for the next build. | Isaac: the cash-out currently jumps straight to the point summary, so nobody sees what everyone bid. |
| Nov 19, 2026 | v1.22a | Debrief with Mitch: keep specialization and the final auction in pitches but present them as removable modules (already options in v1.22a, G8 and T2); keep the no-store Saffron/coin base rule for now (alternatives filed as D6); demo UI items filed as U21–U25, awaiting Isaac's go. | Frank and Vinny found both mechanics swingy; the core game held up. Fathom summary, checked against Home Base's notes. |
| Nov 19, 2026 | v1.22a | Released v1.22a: U20 (fixed lot numbers), G8 (specialization bonus option) and T2 (final auction endgame option). Options default to the standard game; they are saved with replays, game records and online tables. | Approved by Isaac after the R&R pitch so Frank can test both options. Engine self-test covers 24 games with the options (replays exact, 83 cards, no cash-out or specialization points when off, final auction between S3 A3 and season 3 scoring, nothing stored in it). Browser-tested locally and online (new `test_options.py`: greyed bought lots, final auction phase, options shown to the guest and on results, identical host and guest results); existing local and online tests pass. `test_online.py` sometimes times out clicking a re-rendering button (1 of 8 runs on v1.21e, 2 of 9 on v1.22a); a test-timing flake, not a game fault. Endgame comparison under Test results. |
| Nov 19, 2026 | v1.22a | Next build is v1.22a, not v1.21f. Versioning: the number changes when rules or gameplay are added, even as optional settings; the letter is for fixes and UI changes. | Isaac: G8 and T2 add gameplay, and which settings become the default is still to be tested. |
| Nov 19, 2026 | v1.22a | Approved T2: "Endgame" setting, Cash-out (default) or Final auction (stored cards return to hand, one more auction for plain lots from season 3's last bids, unbid cards discarded, season 3 scoring after it, no cash-out points). Planned for the next build, then simulate against the cash-out. | R&R pitch feedback (Frank, Vinny): the cash-out felt passive and swung results; Vinny's one-more-bid idea, with Isaac's choice of plain lots. |
| Nov 19, 2026 | v1.22a | Approved G8: "Specialization bonus" on/off setting, default on, in local, online and simulator games; saved with each game record. Planned for the next build. | R&R pitch feedback (Frank, Vinny): bonus swings frustrate new players; Isaac wants an option for testing, not removal. |
| Nov 19, 2026 | v1.22a | Approved U20: lots keep their numbers until the next market; a bought lot leaves a greyed "bought by" slot. Planned for the next build. | R&R pitch feedback (Vinny): renumbering made it hard to track which lot was taken. UI only. |
| Nov 19, 2026 | v1.21e | Storing rules confirmed as implemented; no change, no new version. Only a Saffron or coin **base** card can't be stored. Saffron and coin **extras** can be stored (a coin extra is cashed first, then may be stored). A stored coin left in hand at season end does nothing; a stored Saffron moves you at season end like any spice. No facedown cards since v1.21a. Closes N4 without change. | Isaac confirmed this matches what he and Mitch decided, after the R&R pitch raised "money cards shouldn't be storable." Engine check: 1,000 bot games, no violations of the written rules (Storing check, Nov 19, 2026). |
| Nov 11, 2026 | v1.21e | Released v1.21e: the demo is a single "Demo to publisher" button (bottom of the right column) that creates an online table for 4 with the demo deal. v1.21d's local Demo option and lobby Deal choice are removed. Only index.html changes. | Isaac: pitches always use online play, even in the same room, so the local option and the lobby toggle are unnecessary; he wants one discreet button that sets everything up. Demo tables can't drop below 4 seats (no Nobody option) so the deal guarantee holds; empty seats can be Bots. Host name is remembered on the device. Browser-tested: first use asks for a name, second use opens the table in one click, guest joined and both screens show seed demo-3904; existing local and online tests pass. v1.21d was pushed to GitHub but not deployed. |
| Nov 11, 2026 | v1.21d | Released v1.21d (U19): a Demo game with fixed seed `demo-3904` for publisher pitches, offered locally ("Demo" beside the player counts) and online ("Deal: Demo" when 4 seats are filled). Only index.html changes. | Requested by Isaac: in a 4-player pitch, every seat should see a pair, a high card (Saffron or coin) and a salted double, even if only a few turns are played. The deal depends only on the seed, so it holds whoever sits where and whether seats are human or bot. Searched demo-1 to demo-41023: 8 seeds qualify (about 1 in 5,000). Chose demo-3904 because each player's pair is in a different suit (Chili, Turmeric, Cinnamon, Oregano), high cards mix Saffron and coins, and the four salted doubles differ. Strict test: the high card and salted double are outside the pair. Self-test now fails if a rules change breaks the demo deal. Browser-tested locally (demo game played to the end; switching back to 3 players restores a random seed) and online (host and guest both on seed demo-3904); existing local and online tests pass. |
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

### Closed in v1.22b

| ID | Issue | Resolution |
| --- | --- | --- |
| U21 | Scoring and cash-out too fast to follow | Track-by-track scoring slowed to 1.5 s per track; season results wait until every human clicks OK (online guests each on their own screen; the host sees who is still choosing; "Bot plays for" also clears a disconnected guest). Final scoring panel: cash-out rank, each player's three stored cards with the bid outlined, the Deck Bot's flipped cards, points; then specialization per player (or a note when an option is off); waits for OK. Bots-only games continue on their own |
| U22 | Latest log scrolled | Shows the last 16 lines, no scroll box |
| U23 | Season results not prominent | Large centered panel for everyone, tooltips on each column heading and on each track's lead bonus |
| U24 | Reference card content | Card-style reference beside your own hand (not selectable, marked Reference): spice icons, quantities and ranges as on the printed card without the zero, plus coins; click to enlarge for the bidding, order, end-of-season and scoring summary |
| U25 | Pitch walkthrough | "Pitch walkthrough" button: 10 steps on the real board with a hand-built 4-player deal played through the engine (market with coin, double, salt and Saffron lots; secret bids; a purchase with a skip, a salt block and a knockdown at the top; storing; others buying; restock; end-of-season movement; scoring; endgame and options). Next, Back, Start game (opens the publisher demo table), Exit. No hands shown, nothing recorded |

### Closed in v1.22a

| ID | Issue | Resolution |
| --- | --- | --- |
| U20 | Lots renumbered after one was bought | Each lot keeps its number until the market is restocked; a bought lot shows as a greyed "Lot 2, Bought by …" slot; buying log lines name the lot number |
| G8 | No way to test without the specialization bonus | "Specialization bonus" option (default on) in local games, online lobby and simulator; when off, no bonus, no +N hint, and bots stop planning for it |
| T2 | Cash-out felt passive (R&R pitch) | "Endgame" option: Cash-out (default) or Final auction. Final auction: after season 3's end-of-season movement, extras are dealt, stored cards return to hand, one more auction (Deck Bot included), buy as usual but store nothing, discard unbid cards, then score season 3; no cash-out points |

### Closed in v1.21d–e

| ID | Issue | Resolution |
| --- | --- | --- |
| N4 | At the R&R pitch, coin extras could be stored and it looked like a bug ([41:48](https://fathom.video/calls/906177727?timestamp=2508)) | No change: Isaac confirmed Nov 19 that only a Saffron or coin base card is unstorable; extras can be stored |
| U19 | Pitch demos need every player to see the main choices quickly | v1.21e: "Demo to publisher" button creates an online 4-player table. Seed `demo-3904`. Starting hands: P1 Saffron 77, Curry 73 x2 (salt), Chili pair (19, 15, 14), Cinnamon 33, Oregano 59; P2 Coin 82 (+5), Turmeric 56 x2 (salt), Turmeric pair (52, 51, 50), Garlic 36, Cinnamon 32; P3 Coin 79 (+2), Oregano 65 x2 (salt), Cinnamon pair (29, 26, 24), Curry 71, Chili 16; P4 Coin 80 (+2), Saffron 74, Cinnamon 34 x2 (salt), Oregano pair (62, 57), Turmeric 55, Garlic 44 |

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

### Endgame comparison: cash-out vs. final auction (Nov 19, 2026; v1.22a; no decision yet)

Method: 250 bot games per player count (seeds `endgame-<players>-0` to `-249`, 2,000 games), each played once with the cash-out and once with the final auction; specialization on. Both modes play identically until the end of season 3 (checked on 100 seeds), so "no endgame" is the cash-out game minus its cash-out points. "Endgame points" is what each player gained from the endgame (for the final auction, its tops and coins plus its effect on season 3 scoring and specialization). Bots were not tuned for the final auction. Gaps and winners count players only, not the Deck Bot.

| Players | Endgame | Endgame points per player | Gap 1st–last | Gap 1st–2nd | Endgame changed the winner |
|---|---|---|---|---|---|
| 2 | Cash-out | 3.9 | 17.9 | 17.9 | 13% |
| 2 | Final auction | 4.3 | 17.7 | 17.7 | 11% |
| 3 | Cash-out | 3.0 | 27.6 | 13.3 | 14% |
| 3 | Final auction | 3.1 | 27.5 | 13.5 | 14% |
| 4 | Cash-out | 4.3 | 31.0 | 11.4 | 21% |
| 4 | Final auction | 2.3 | 29.7 | 10.9 | 20% |
| 5 | Cash-out | 6.4 | 38.1 | 11.2 | 31% |
| 5 | Final auction | 2.4 | 35.0 | 10.6 | 26% |

Reading: at 2–3 players the two endgames are about equal. At 4–5 players the final auction moves fewer points (2.3–2.4 vs. 4.3–6.4 per player) and spreads scores slightly less, but it still changes the winner in a fifth to a quarter of games, because the last purchases shift season 3 leads. Whether it feels more strategic is a question for human play.

### Storing check (Nov 19, 2026; v1.21e)

Method: 1,000 bot games (seeds `storecheck-<players>-0` to `-249`, 250 each at 2, 3, 4 and 5 players), with the engine wrapped to check every storing rule as it happens: 31,500 player purchases, 2,250 Deck Bot purchases, 3,000 season ends, 1,000 cash-outs (250 with the Deck Bot). No violations of the rules as written in `docs/RULES.md`:

| Rule | Result |
| --- | --- |
| Store exactly one card from each lot bought, from that lot | Pass (31,500 of 31,500) |
| Saffron or coin base card never stored | Pass (4,286 such lots) |
| Storing never moves anyone | Pass |
| Deck Bot stores nothing | Pass |
| Season end: cards left in hand move you, best hand bid goes first, Deck Bot first | Pass (3,000) |
| After seasons 1 and 2: stored cards return to hand, plus 3 dealt | Pass (2,000) |
| Cash-out: three stored cards, ranked by best bid, points 7/2/0, 10/5/2/0, 15/10/5/2/0 | Pass (1,000) |

Coin extras were stored 2,379 times and Saffron extras 2,564 times, both allowed (confirmed by Isaac Nov 19; N4 closed without change). For reference, if coins were ever made unstorable: 161 of 31,500 purchases (0.5%) would leave nothing to store, and 51 of 4,000 player-games would reach the cash-out with fewer than three stored cards (seeds `nocoin-*`, same method).

### Physical coin supply (Nov 11, 2026; v1.21c rules; no decision yet)

Question: how many printed coins, in which denominations, for the physical game. 1,600 bot games (400 per player count; 2-player games include a scoring Deck Bot). Each payout is paid as it happens in the fewest coins; the table is the most coins out at once (95th percentile, 5 players), by when players trade small coins up.

| Set | Trade up | 2s | 5s | 10s | Larger |
| --- | --- | --- | --- | --- | --- |
| 2/5/10 | Never | 83 | 38 | 9 | – |
| 2/5/10 | After seasons 1 and 2 | 60 | 23 | 21 | – |
| 2/5/10 | After every season | 55 | 16 | 34 | – |
| 2/5/20 | After every season | 55 | 28 | – | 14 twenties |
| 2/5/10/20 | After every season | 55 | 16 | 10 | 14 twenties |
| 2/5/10/25 | After every season | 55 | 16 | 11 | 11 twenty-fives |

Other findings: total points on the table at game end p95 / max: 2p+bot 256 / 277, 3p 264 / 287, 4p 327 / 364, 5p 403 / 430. About 9–10 fives are paid per season (p95 12). A fourth denomination only replaces 10s, saving about 10 coins. Recommended to Isaac: 2s, 5s and 10s, about 50 / 30 / 30 (110 coins, 550 points), with a rule to trade up between seasons.

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

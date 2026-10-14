# Saffron Salt — rules as implemented (v1.21c)

This is the rules reference for the digital playtest edition, version 1.21c. It supersedes the analog v1.20 rules document wherever they differ; the differences are listed at the end. Points replace the physical coins.

## Goal

Over three seasons, bid for lots of spice cards, climb the seven spice tracks, and finish with the most points.

## Components

**Cards (83).** Cards 1–78 are spices:

| Spice | Cards | Extra cards in its lot | Double icon | Salt |
|---|---|---|---|---|
| Chili | 1–19 | +3 | 19 | none |
| Cinnamon | 20–34 | +2 | 34 | 33, 34 |
| Garlic | 35–46 | +2 | 46 | 45, 46 |
| Turmeric | 47–56 | +1 | 56 | 54, 55, 56 |
| Oregano | 57–65 | +1 | 65 | 63, 64, 65 |
| Curry | 66–73 | +1 | 73 | 70–73 |
| Saffron | 74–78 | +1 | none | none |

Cards 79–83 are coin cards: 79 and 80 are worth 2 points (+2 extra cards), 81 and 82 are worth 5 (+1), 83 is worth 7 (+1). Coin cards count as their own suit when bidding. A double icon moves its owner two spaces.

**Tracks** (spaces counted from the bottom; space 1 is the start, the last space is the top):

| Track | Spaces | MOQ space | Top pays | Lead pays | "2/3" cube | "4" cube |
|---|---|---|---|---|---|---|
| Chili | 11 | 5 | 2 | 5 | 9 | 3 |
| Cinnamon | 11 | 6 | 2 | 5 | 9 | 4 |
| Garlic | 11 | 7 | 2 | 5 | 9 | 5 |
| Turmeric | 11 | 7 | 2 | 5 | 9 | 5 |
| Oregano | 9 | 5 | 2 | 5 | 7 | 3 |
| Curry | 8 | 4 | 2 | 5 | 6 | — |
| Saffron | 7 | 2 | 5 | 7 | — | — |

On the board, tracks run Chili, Cinnamon, Garlic, Turmeric, Oregano, Curry, Saffron from left to right.

## Setup

1. Every player's marker starts on space 1 of every track.
2. **Neutral cubes** occupy spaces:
   - 2–3 players: one cube on the "2/3" space and one on the "4" space of every track that has them, **plus one on Saffron space 4** (one empty space above the MOQ).
   - 4 players: only the "4" cubes (Curry has none).
   - 5 players: no cubes.
3. Deal 7 cards to each player. Each player secretly chooses one card for the market; choices can be changed until everyone has chosen, then they're revealed together.
4. In 2-player games, also place the top card of the deck in the market for the Deck Bot.
5. Each market card is the **base** of a lot: deal the extra cards shown on its badge next to it, **faceup**. A Saffron or coin base card is laid sideways as a reminder that it can't be stored.

## Each season

Three seasons, each with three auctions, then the end of the season.

### An auction

1. **Bid.** Everyone secretly bids one card, or two cards of the same suit (coins pair with coins). Any pair beats any single; otherwise the higher card number wins. Keep enough cards in hand to bid in every remaining auction this season. Bids can be changed until all bids are in.
2. **Buy.** In bid order, highest first, each player buys one lot:
   - Cash any coin cards in the lot for their points.
   - Move up the track of every spice card in the lot (two spaces for a double icon). When several cards interact, the buyer chooses the order.
   - Store one card from the lot; a Saffron or coin **base** card can't be stored, so choose from the other cards. Discard the rest.
3. **Restock.** The bids become the new base cards: from each pair, the higher card goes to the market and the lower is discarded. Each new base card gets its extra cards straight away, **except after a season's third auction**: then the base cards wait without extras until the end of the season (below).

### Moving on the tracks

- Cards move you only when you **buy** them in a lot, or when they're **left in your hand at the end of a season**. Storing a card never moves you. Facedown cards never move anyone or get cashed (no lot is dealt facedown from v1.21a).
- **Skipping:** move to the next space up that isn't occupied by another marker or a neutral cube; occupied spaces don't count.
- **Salt:** a salted card can't skip. If the space directly above you is occupied, that movement is lost.
- **The top space** pays its points each time you reach it (5 on Saffron, 2 elsewhere), and again for each movement you'd make while already there. Reaching an occupied top knocks that marker down to the MOQ space.
- Markers share a space only on the start space, and on the MOQ space when knocked down.

### End of a season

1. **Storage.** In 2-player games the Deck Bot goes first (see below). Then, in order of the best bid each hand could make, players reveal the cards left in hand and move for each one (choosing the order when it matters), then discard them.
2. **Scoring,** track by track:
   - The single marker furthest ahead **leads** and scores the lead bonus (7 Saffron, 5 elsewhere). A tie for the lead scores nothing; it can only happen on the start space.
   - Every other player at or above the **MOQ** (Minimum Order Quantity) space scores 2. A leader doesn't also score the MOQ.
   - Neutral cubes never score.
3. The waiting base cards get their extra cards.
4. After seasons 1 and 2: stored cards return to hand, and each player is dealt 3 more. The market carries over.

## End of the game

1. **Cash-out.** After season 3, everyone reveals their three stored cards and makes the best bid they can. Points by rank: 2–3 players 7 / 2 / 0; 4 players 10 / 5 / 2 / 0; 5 players 15 / 10 / 5 / 2 / 0. In 2-player games the Deck Bot also bids (as in an auction) and takes a rank.
2. **Specialization.** Each player scores a bonus for tracks their marker never left: 7 for one, 17 for two, 30 for three or more.
3. Most points wins; tied players share the win.

## Two players: the Deck Bot

- **Bidding:** flip a card from the deck. If it's 57 or higher, flip one more; otherwise flip two more. Its bid is the best bid among those cards. Afterward its highest bid card goes to the market and the other flipped cards are discarded.
- **Its lot:** if it bids highest, the lowest bidder chooses its lot; if it's second, the highest bidder chooses; if it's last, it takes the remaining lot. It moves like a player (choosing the order best for itself) but stores nothing.
- **End of season:** it goes first in storage and advances one space on **each track it isn't leading, except Saffron**. A tie for the lead counts as not leading.
- **Scoring:** it scores like a player, and players must be ahead of it to lead a track. Optionally, play without keeping its score: it still moves and blocks leads but scores nothing.

## Changes from the v1.20 rules document

| Version | Change |
|---|---|
| v1.20b | New track layout (lengths, MOQ spaces, "2/3" and "4" cube spaces); Curry has no "4" cube. Deck Bot season-end rule: advance on each track it isn't leading, never Saffron. |
| v1.21a | Saffron and coin lots are dealt **faceup**; their base card can't be stored. Facedown cards never move or cash. After a season's third auction, the new lots get their extras only after end-of-season storage. Optional Deck Bot scoring. Bids can be changed until all are in. |
| v1.21b | Neutral cube on Saffron space 4 in 2–3 player games. |
| v1.21c | Market-seeding choices can be changed until all are in. |

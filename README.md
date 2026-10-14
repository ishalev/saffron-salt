# Saffron Salt

Digital playtest edition of **Saffron Salt**, a spice-trading auction game by Isaac and Mitch.

- **Play:** https://kindfortress.com/saffron-salt/
- **Current version:** see the top line of [RELEASES.md](RELEASES.md)
- **Design decisions and test results:** kept in the Saffron Salt Issues and Decisions Log (Claude Doc)

## What's here

| Folder | Contents |
|---|---|
| `game/` | Everything that goes on the web server: `index.html` (the whole game), `relay.php` (online play), `games.php` (game logs), `feedback.php` (player feedback; **template only**) |
| `tools/` | Simulation and analysis scripts, and browser tests. See [tools/README.md](tools/README.md) |
| `RELEASES.md` | One entry per version |

## Deploying

Upload the files in `game/` to the `saffron-salt` folder on the server. **Never upload the template `feedback.php` over the server's copy**: the server copy holds the real notification email and review password, and those must never be committed here.

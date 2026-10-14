#!/bin/sh
# Serves a test copy of game/ at http://localhost:8772 with a test review password (pw123).
# Your real feedback settings are never used. Needs PHP 7.4+ (php -S).
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
SITE=/tmp/saffron-test-site
rm -rf "$SITE" && mkdir -p "$SITE"
cp "$HERE/../../game/index.html" "$HERE/../../game/relay.php" "$HERE/../../game/games.php" "$SITE/"
sed "s/\$REVIEW_PASSWORD = 'change-me';/\$REVIEW_PASSWORD = 'pw123';/" "$HERE/../../game/feedback.php" > "$SITE/feedback.php"
cd "$SITE" && exec php -S localhost:8772

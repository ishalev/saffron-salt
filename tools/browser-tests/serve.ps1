# Serves a test copy of game/ at http://localhost:8772 with a test review password (pw123).
# Windows version of serve.sh. Your real feedback settings are never used. Needs PHP 7.4+ (php -S).
$ErrorActionPreference = 'Stop'
$game = Join-Path $PSScriptRoot '..\..\game'
$site = Join-Path $env:TEMP 'saffron-test-site'
if (Test-Path $site) { Remove-Item -Recurse -Force $site }
New-Item -ItemType Directory $site | Out-Null
Copy-Item (Join-Path $game 'index.html'), (Join-Path $game 'relay.php'), (Join-Path $game 'games.php') $site
$fb = [IO.File]::ReadAllText((Join-Path $game 'feedback.php'))
$old = "`$REVIEW_PASSWORD = 'change-me';"
if (-not $fb.Contains($old)) { throw "feedback.php template no longer contains $old" }
# Write without a byte-order mark: PHP would send it as output before headers.
[IO.File]::WriteAllText((Join-Path $site 'feedback.php'), $fb.Replace($old, "`$REVIEW_PASSWORD = 'pw123';"), (New-Object Text.UTF8Encoding $false))
Set-Location $site
php -S localhost:8772

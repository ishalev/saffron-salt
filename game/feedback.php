<?php
// Saffron Salt — playtest feedback.
// Players submit from the results screen; each submission is saved here and emailed to you.
// Review everything at feedback.php in your browser (password below).

// ====== SETTINGS: edit these two lines ======
$NOTIFY_EMAIL    = 'you@example.com';   // where new-feedback emails go
$REVIEW_PASSWORD = 'change-me';         // password for the review page
// ============================================

const MAX_TEXT = 4000;
const MAX_META = 300000;
$dir = __DIR__ . '/saffron-feedback';
$configured = $REVIEW_PASSWORD !== 'change-me' && $REVIEW_PASSWORD !== '';

function ensure_dir($dir) {
  if (!is_dir($dir)) {
    if (!@mkdir($dir, 0755, true)) return false;
    file_put_contents("$dir/.htaccess", "Require all denied\nDeny from all\n");
    file_put_contents("$dir/index.html", '');
  }
  return true;
}
function h($s) { return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }
function clip($s, $n) { $s = is_string($s) ? trim($s) : ''; return function_exists('mb_substr') ? mb_substr($s, 0, $n) : substr($s, 0, $n); }

// ---------- Submit (JSON POST from the game) ----------
if ($_SERVER['REQUEST_METHOD'] === 'POST' && stripos($_SERVER['CONTENT_TYPE'] ?? '', 'application/json') !== false) {
  header('Content-Type: application/json; charset=utf-8');
  header('Cache-Control: no-store');
  $raw = file_get_contents('php://input');
  if (strlen($raw) > MAX_META + 6 * MAX_TEXT * 4) { http_response_code(413); echo '{"error":"too large"}'; exit; }
  $in = json_decode($raw);
  if (!is_object($in)) { http_response_code(400); echo '{"error":"bad request"}'; exit; }
  if (!empty($in->website)) { echo '{"ok":true}'; exit; } // spam trap
  $name = clip($in->name ?? '', 100);
  if ($name === '') { http_response_code(400); echo '{"error":"name required"}'; exit; }
  $email = clip($in->email ?? '', 200);
  if ($email !== '' && !filter_var($email, FILTER_VALIDATE_EMAIL)) { http_response_code(400); echo '{"error":"bad email"}'; exit; }
  $entry = [
    'id' => date('Ymd-His') . '-' . bin2hex(random_bytes(3)),
    'received' => date('c'),
    'name' => $name,
    'email' => $email,
    'best' => clip($in->best ?? '', MAX_TEXT),
    'change' => clip($in->change ?? '', MAX_TEXT),
    'confused' => clip($in->confused ?? '', MAX_TEXT),
    'other' => clip($in->other ?? '', MAX_TEXT),
    'meta' => isset($in->meta) && is_object($in->meta) && strlen(json_encode($in->meta)) <= MAX_META ? $in->meta : null,
  ];
  if (!ensure_dir($dir) || file_put_contents("$dir/{$entry['id']}.json", json_encode($entry)) === false) {
    http_response_code(500); echo '{"error":"could not save"}'; exit;
  }
  if ($NOTIFY_EMAIL && $NOTIFY_EMAIL !== 'you@example.com') {
    $m = $entry['meta'];
    $host = preg_replace('/[^A-Za-z0-9.-]/', '', $_SERVER['HTTP_HOST'] ?? 'localhost');
    $host = preg_replace('/^www\./', '', $host);
    $lines = [
      "New Saffron Salt feedback from {$entry['name']}" . ($email ? " <$email>" : ''),
      '',
      $m ? ("Game: {$m->playerCount} players, seed {$m->seed}, rules v{$m->rulesVersion}") : '',
      $m && isset($m->scoreLine) ? "Scores: {$m->scoreLine}" : '',
      '',
      "Best part:\n" . ($entry['best'] ?: '(blank)'),
      '',
      "What they'd change:\n" . ($entry['change'] ?: '(blank)'),
      '',
      "Confusing:\n" . ($entry['confused'] ?: '(blank)'),
      '',
      "Other comments:\n" . ($entry['other'] ?: '(blank)'),
      '',
      'Review all feedback: https://' . ($_SERVER['HTTP_HOST'] ?? $host) . strtok($_SERVER['REQUEST_URI'] ?? '/feedback.php', '?'),
    ];
    $headers = "From: Saffron Salt <noreply@$host>\r\nContent-Type: text/plain; charset=UTF-8\r\n";
    if ($email) $headers .= "Reply-To: $email\r\n";
    @mail($NOTIFY_EMAIL, "Saffron Salt feedback from {$entry['name']}", implode("\n", $lines), $headers);
  }
  echo '{"ok":true}';
  exit;
}

// ---------- Review page ----------
$token = $configured ? hash_hmac('sha256', 'saffron-review', $REVIEW_PASSWORD) : '';
$authed = $configured && isset($_COOKIE['ssfb']) && hash_equals($token, $_COOKIE['ssfb']);
if ($configured && $_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['password'])) {
  if (hash_equals($REVIEW_PASSWORD, (string)$_POST['password'])) {
    setcookie('ssfb', $token, ['expires' => time() + 30 * 86400, 'path' => '/', 'httponly' => true, 'samesite' => 'Lax', 'secure' => !empty($_SERVER['HTTPS'])]);
    header('Location: ' . strtok($_SERVER['REQUEST_URI'], '?')); exit;
  }
  $loginError = true;
}
if ($authed && isset($_GET['logout'])) { setcookie('ssfb', '', ['expires' => 1, 'path' => '/']); header('Location: ' . strtok($_SERVER['REQUEST_URI'], '?')); exit; }

$entries = [];
if ($authed && is_dir($dir)) {
  foreach (glob("$dir/*.json") as $f) { $e = json_decode(file_get_contents($f)); if ($e) $entries[] = $e; }
  usort($entries, fn($a, $b) => strcmp($b->id, $a->id));
}
if ($authed && isset($_GET['replay'])) {
  $id = preg_replace('/[^0-9a-f-]/', '', $_GET['replay']);
  foreach ($entries as $e) if ($e->id === $id && isset($e->meta->replay)) {
    header('Content-Type: application/json'); header("Content-Disposition: attachment; filename=\"saffron-salt-{$e->meta->seed}-replay.json\"");
    echo json_encode($e->meta->replay); exit;
  }
  http_response_code(404); echo 'No replay for that entry.'; exit;
}
if ($authed && isset($_GET['csv'])) {
  header('Content-Type: text/csv; charset=utf-8'); header('Content-Disposition: attachment; filename="saffron-salt-feedback.csv"');
  $out = fopen('php://output', 'w');
  fputcsv($out, ['received', 'name', 'email', 'players', 'seed', 'rules', 'scores', 'best part', 'would change', 'confused', 'other']);
  foreach ($entries as $e) fputcsv($out, [$e->received, $e->name, $e->email, $e->meta->playerCount ?? '', $e->meta->seed ?? '', $e->meta->rulesVersion ?? '', $e->meta->scoreLine ?? '', $e->best, $e->change, $e->confused, $e->other]);
  exit;
}
header('Content-Type: text/html; charset=utf-8');
?><!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Saffron Salt feedback</title>
<style>
  body { font-family: Georgia, 'Times New Roman', serif; background: #fbf6ee; color: #3a2a20; margin: 0; line-height: 1.5; }
  main { max-width: 900px; margin: 0 auto; padding: 28px 18px 60px; }
  h1 { font-size: 40px; margin: 0 0 4px; }
  .muted { color: #85725f; }
  .entry { background: #fff; border: 1.5px solid #dccdb9; border-radius: 10px; padding: 16px 18px; margin: 14px 0; }
  .entry h2 { font-size: 20px; margin: 0; }
  .q { font-weight: bold; margin: 10px 0 2px; font-size: 15px; }
  .a { white-space: pre-wrap; margin: 0; }
  a, button { color: #3a2a20; }
  button, input { font: inherit; }
  input[type=password] { padding: 6px 10px; border: 1.5px solid #dccdb9; border-radius: 6px; }
  button { padding: 6px 14px; border: 1.5px solid #3a2a20; background: #3a2a20; color: #fbf6ee; border-radius: 6px; cursor: pointer; }
  .bar { display: flex; gap: 16px; flex-wrap: wrap; align-items: center; margin: 10px 0 20px; }
</style></head><body><main>
<h1>Saffron Salt feedback</h1>
<?php if (!$configured): ?>
  <p>The review page is turned off until you set <code>$REVIEW_PASSWORD</code> at the top of feedback.php.</p>
<?php elseif (!$authed): ?>
  <form method="post"><p><label for="pw">Password</label><br><input id="pw" type="password" name="password" autofocus> <button>Sign in</button></p>
  <?php if (!empty($loginError)) echo '<p style="color:#c8232c">That password is not right.</p>'; ?></form>
<?php else: ?>
  <div class="bar"><span class="muted"><?= count($entries) ?> submission<?= count($entries) === 1 ? '' : 's' ?></span><a href="?csv=1">Download all as a spreadsheet (CSV)</a><a href="?logout=1">Sign out</a></div>
  <?php if (!$entries) echo '<p>No feedback yet.</p>'; ?>
  <?php foreach ($entries as $e): $m = $e->meta; ?>
  <article class="entry">
    <h2><?= h($e->name) ?><?php if ($e->email): ?> <span class="muted" style="font-size:15px">&lt;<a href="mailto:<?= h($e->email) ?>"><?= h($e->email) ?></a>&gt;</span><?php endif; ?></h2>
    <div class="muted"><?= h(date('M j, Y g:i a', strtotime($e->received))) ?><?php if ($m): ?> — <?= h($m->playerCount) ?> players, seed <?= h($m->seed) ?>, rules v<?= h($m->rulesVersion) ?><?php if (!empty($m->scoreLine)) echo ' — ' . h($m->scoreLine); ?><?php endif; ?></div>
    <?php foreach (['best' => 'Best part of the game', 'change' => 'What they might change', 'confused' => 'Anything confusing', 'other' => 'Other comments'] as $k => $label): ?>
      <p class="q"><?= $label ?></p><p class="a"><?= $e->$k !== '' ? h($e->$k) : '<span class="muted">(blank)</span>' ?></p>
    <?php endforeach; ?>
    <?php if ($m && isset($m->replay)): ?><p style="margin:12px 0 0"><a href="?replay=<?= h($e->id) ?>">Download this game’s replay</a> <span class="muted">— open it in the game under “Replay a game”.</span></p><?php endif; ?>
  </article>
  <?php endforeach; ?>
<?php endif; ?>
</main></body></html>

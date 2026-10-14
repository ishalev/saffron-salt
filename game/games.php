<?php
// Saffron Salt — game log storage (v1.21a).
// Every finished game played on this site is saved here. The "All games on this site"
// view in Game logs reads them back, using the password set in feedback.php.

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');

const MAX_RECORD = 600000;   // bytes per game record
const MAX_GAMES = 2000;      // oldest games are removed beyond this

function fail($msg, $status = 400) { http_response_code($status); echo json_encode(['error' => $msg]); exit; }
function review_password() {
  $src = @file_get_contents(__DIR__ . '/feedback.php');
  if ($src && preg_match('/\$REVIEW_PASSWORD\s*=\s*\'((?:[^\'\\\\]|\\\\.)*)\'/', $src, $m)) return stripcslashes($m[1]);
  return '';
}
function check_password($given) {
  $pw = review_password();
  if ($pw === '' || $pw === 'change-me') fail('not configured', 403);
  if (!is_string($given) || !hash_equals($pw, $given)) fail('bad password', 403);
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') fail('POST only', 405);
$raw = file_get_contents('php://input');
if (strlen($raw) > MAX_RECORD + 1000) fail('too large', 413);
$in = json_decode($raw);
if (!is_object($in) || !isset($in->op)) fail('bad request');

$dir = __DIR__ . '/saffron-games';
if (!is_dir($dir)) {
  if (!@mkdir($dir, 0755, true)) fail('cannot create data folder', 500);
  file_put_contents("$dir/.htaccess", "Require all denied\nDeny from all\n");
  file_put_contents("$dir/index.html", '');
}
$idOk = fn($id) => is_string($id) && preg_match('/^[a-z0-9]{6,24}$/', $id);

switch ($in->op) {
  case 'save': {
    $r = $in->record ?? null;
    if (!is_object($r) || !$idOk($r->id ?? null)) fail('bad record');
    $json = json_encode($r);
    if (strlen($json) > MAX_RECORD) fail('record too large', 413);
    $r->savedAt = date('c');
    file_put_contents("$dir/{$r->id}.json", json_encode($r));
    if (mt_rand(1, 20) === 1) {
      $files = glob("$dir/*.json");
      if (count($files) > MAX_GAMES) { usort($files, fn($a, $b) => filemtime($a) - filemtime($b)); foreach (array_slice($files, 0, count($files) - MAX_GAMES) as $f) @unlink($f); }
    }
    echo json_encode(['ok' => true]);
    break;
  }
  case 'flag': {
    $id = $in->id ?? null;
    if (!$idOk($id) || !file_exists("$dir/$id.json")) fail('not found', 404);
    $r = json_decode(file_get_contents("$dir/$id.json"));
    if ($r) { $r->feedback = true; file_put_contents("$dir/$id.json", json_encode($r)); }
    echo json_encode(['ok' => true]);
    break;
  }
  case 'list': {
    check_password($in->password ?? null);
    $rows = [];
    foreach (glob("$dir/*.json") as $f) {
      $r = json_decode(file_get_contents($f));
      if (!$r) continue;
      unset($r->result, $r->replay);
      $r->replay = file_exists($f) && strpos(file_get_contents($f), '"replay":{') !== false;
      $rows[] = $r;
    }
    usort($rows, fn($a, $b) => strcmp($b->at ?? '', $a->at ?? ''));
    echo json_encode(['ok' => true, 'games' => $rows]);
    break;
  }
  case 'get': {
    check_password($in->password ?? null);
    $id = $in->id ?? null;
    if (!$idOk($id) || !file_exists("$dir/$id.json")) fail('not found', 404);
    echo '{"ok":true,"record":' . file_get_contents("$dir/$id.json") . '}';
    break;
  }
  default: fail('unknown op');
}

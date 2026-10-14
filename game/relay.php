<?php
// Saffron Salt — online play relay.
// Stores each table's shared state and each player's latest message in a small
// JSON file. The game itself runs in the host's browser.
// Upload next to index.html. Needs PHP 7.4+ and a writable folder (created automatically).

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');

const MAX_BODY = 400000;    // bytes per shared document
const MAX_PRESENCE = 8000;  // bytes per player message
const PEER_TIMEOUT = 12;    // seconds without a check-in before a player counts as gone
const TABLE_TTL = 259200;   // delete tables untouched for 3 days

function fail($msg, $status = 400) { http_response_code($status); echo json_encode(['error' => $msg]); exit; }

if ($_SERVER['REQUEST_METHOD'] !== 'POST') fail('POST only', 405);
$raw = file_get_contents('php://input');
if (strlen($raw) > MAX_BODY + 2000) fail('too large', 413);
$in = json_decode($raw);
if (!is_object($in) || !isset($in->op)) fail('bad request');

$dir = __DIR__ . '/saffron-tables';
if (!is_dir($dir)) {
  if (!@mkdir($dir, 0755, true)) fail('cannot create data folder', 500);
  file_put_contents("$dir/.htaccess", "Require all denied\nDeny from all\n");
  file_put_contents("$dir/index.html", '');
}

if ($in->op === 'ping') { echo json_encode(['ok' => true]); exit; }

$code = isset($in->code) ? $in->code : '';
if (!is_string($code) || !preg_match('/^[A-Z]{4}$/', $code)) fail('bad code');
$key = (isset($in->key) && is_string($in->key) && preg_match('/^[A-Za-z0-9_-]{1,64}$/', $in->key)) ? $in->key : null;
$docName = isset($in->doc) ? $in->doc : '';
$file = "$dir/$code.json";

// Only an explicit write may create a table file.
if (!file_exists($file) && $in->op !== 'set') { echo json_encode(['ok' => true, 'body' => null, 'docs' => new stdClass, 'peers' => []]); exit; }

$fp = fopen($file, 'c+');
if (!$fp) fail('cannot open table', 500);
flock($fp, LOCK_EX);
$t = json_decode(stream_get_contents($fp));
if (!is_object($t)) $t = (object)['docs' => new stdClass, 'rev' => (object)['lobby' => 0, 'state' => 0], 'pres' => new stdClass];
$now = microtime(true);
$out = ['ok' => true];
$dirty = false;

switch ($in->op) {
  case 'get':
    $out['body'] = isset($t->docs->$docName) ? $t->docs->$docName : null;
    break;

  case 'set':
    if (!in_array($docName, ['lobby', 'state'], true)) { $out = ['error' => 'bad doc']; break; }
    if (!isset($in->body) || !is_object($in->body)) { $out = ['error' => 'bad body']; break; }
    if (strlen(json_encode($in->body)) > MAX_BODY) { $out = ['error' => 'document too large']; break; }
    $t->docs->$docName = $in->body;
    $t->rev->$docName = (isset($t->rev->$docName) ? $t->rev->$docName : 0) + 1;
    $dirty = true;
    break;

  case 'presence':
    if (!$key) { $out = ['error' => 'bad key']; break; }
    $p = isset($in->pres) && is_object($in->pres) ? $in->pres : new stdClass;
    if (strlen(json_encode($p)) > MAX_PRESENCE) { $out = ['error' => 'message too large']; break; }
    $t->pres->$key = (object)['p' => $p, 't' => $now];
    $dirty = true;
    break;

  case 'leave':
    if ($key && isset($t->pres->$key)) { unset($t->pres->$key); $dirty = true; }
    break;

  case 'poll':
    $have = isset($in->have) && is_object($in->have) ? $in->have : new stdClass;
    $docs = new stdClass;
    foreach (['lobby', 'state'] as $d) {
      $rev = isset($t->rev->$d) ? $t->rev->$d : 0;
      $seen = isset($have->$d) ? intval($have->$d) : 0;
      if ($rev > $seen && isset($t->docs->$d)) $docs->$d = ['rev' => $rev, 'body' => $t->docs->$d];
    }
    $out['docs'] = $docs;
    if ($key && isset($t->pres->$key)) { $t->pres->$key->t = $now; $dirty = true; }
    $peers = [];
    foreach ($t->pres as $k => $v) {
      if ($now - $v->t <= PEER_TIMEOUT) $peers[] = ['key' => $k, 'pres' => $v->p];
      elseif ($now - $v->t > 60) { unset($t->pres->$k); $dirty = true; }
    }
    $out['peers'] = $peers;
    break;

  default:
    $out = ['error' => 'unknown op'];
}

if ($dirty) {
  ftruncate($fp, 0);
  rewind($fp);
  fwrite($fp, json_encode($t));
  fflush($fp);
}
flock($fp, LOCK_UN);
fclose($fp);

// Occasionally clear out old tables.
if ($in->op === 'set' && mt_rand(1, 20) === 1) {
  foreach (glob("$dir/*.json") as $f) if (time() - filemtime($f) > TABLE_TTL) @unlink($f);
}

echo json_encode($out);

# Final two-voice (Version B) pitch video: draft 2's shots, re-cued to the spliced Isaac + Mitch audio.
import wave, json, sys
from vlib import *

def dur(p):
    w = wave.open(p); return w.getnframes() / w.getframerate()
SD = [dur(f'two/section{k}.wav') for k in range(1, 6)]
LEAD, GAP, TAIL = 1.0, 0.8, 3.0
ST = []; t = LEAD
for d in SD: ST.append(t); t += d + GAP
TOTAL = ST[4] + SD[4] + TAIL
import difflib, re
OLDW = {int(k): v for k, v in json.load(open('words/words.json')).items()}
NEWW = {int(k): v for k, v in json.load(open('two/w/words.json')).items()}
def _n(w): return re.sub(r'[^a-z0-9]', '', w.lower())
ANCH = {}
for k in range(1, 6):
    a = [_n(w[2]) for w in OLDW[k]]; b = [_n(w[2]) for w in NEWW[k]]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    ANCH[k] = [(OLDW[k][m.a + i][0], NEWW[k][m.b + i][0]) for m in sm.get_matching_blocks() for i in range(m.size)]
def remap(sec, t):
    A = ANCH[sec]
    if t <= A[0][0]: return max(0.0, A[0][1] - (A[0][0] - t))
    if t >= A[-1][0]: return A[-1][1] + (t - A[-1][0])
    for (o0, n0), (o1, n1) in zip(A, A[1:]):
        if o0 <= t <= o1: return n0 + (n1 - n0) * (t - o0) / max(1e-6, o1 - o0)
def c(sec, w): return ST[sec - 1] + remap(sec, w)   # cue: section, OLD solo word time -> new time
def cn(sec, word, k=0, end=False):                   # cue by a word in the NEW audio
    hits = [x for x in NEWW[sec] if _n(x[2]) == word]
    return ST[sec - 1] + hits[k][1 if end else 0]

R = Rec('rec2/full'); R.build_master()
B = json.load(open('cards/boxes.json'))

# crops (master coords, 1600x1900 frames)
MKT = (220, 240, 1160, 652)
TW1 = (113, 780, 1060, 596)   # all tracks, auction layout
TZ1 = (0, 795, 960, 540)      # Chili/Cinnamon/Garlic, auction layout
TW2 = (113, 720, 1060, 596)   # all tracks, storage/scoring layout
TZ2 = (0, 745, 960, 540)
KEEP = (220, 560, 1160, 652)
CARD = (0, 0, 1920, 1080)
def ph(n): return f'img2/p{n}.png'
LAND = (0, 378, 4032, 2268)
def port(y): return (0, y, 3024, 1701)

def space(cx, cy): return (cx - 62, cy - 15, 124, 30)   # one track space

scenes = []
def S(name, at, src, crop, ev=None, hl=(), cam=None):
    s = dict(name=name, at=at, src=src, crop=crop, hl=list(hl), rec=R)
    s['ev'] = ev or [(at, 'hold', 0.0)]
    s['cam'] = cam or (at, at + 6, 1.0, 1.04, 0.5, 0.5)
    scenes.append(s)

# ---------- Section 1: Hello ----------
S('title', 0.0, 'cards/title.png', CARD, cam=(0, c(1, 17.7), 1.0, 1.05, 0.5, 0.5),
  hl=[(c(1, 8.7), c(1, 12.2), tuple(B['title.tag'])), (c(1, 12.4), c(1, 16.6), tuple(B['title.meta']))])
S('photo hands', c(1, 17.7), ph(6104), LAND, cam=(c(1, 17.7), c(1, 21.2), 1.0, 1.06, 0.5, 0.5))
S('photo board', c(1, 21.2), ph(6723), LAND, cam=(c(1, 21.2), c(1, 25.1), 1.06, 1.0, 0.5, 0.5))
S('photo lots', c(1, 25.1), ph(6720), LAND, cam=(c(1, 25.1), c(1, 29.6), 1.0, 1.06, 0.5, 0.8))
S('photo coins', c(1, 29.6), ph(6719), LAND, cam=(c(1, 29.6), c(2, 0.0), 1.0, 1.05, 0.5, 0.5))

# ---------- Section 2: The auction ----------
S('photo market', c(2, 0.0), 'img2/p6163r.png', port(1760), cam=(c(2, 0.0), c(2, 2.5), 1.0, 1.04, 0.5, 0.5))   # rotated 180 (Isaac 11/17)
g = (c(2, 2.5), c(2, 36.5), 1.0, 1.06, 0.5, 0.4)
LOTS = (318, 298, 964, 138); HAND = (240, 575, 508, 104)
S('market', c(2, 2.5), 'master', MKT, [(c(2, 2.5), 'hold', 4.0)], cam=g,
  hl=[(c(2, 2.6), c(2, 4.7), LOTS), (c(2, 4.9), c(2, 9.4), HAND)])
ANISE = (1128, 292, 198, 68); CUMIN = (1128, 360, 150, 66); BIDS = (1125, 290, 202, 272)
S('reveal', c(2, 9.6), 'master', MKT, [(c(2, 9.6), 'hold', 8.5)], cam=g,
  hl=[(c(2, 9.6), c(2, 11.4), ANISE), (c(2, 11.6), c(2, 13.6), CUMIN), (c(2, 13.9), c(2, 16.1), BIDS)])
S('pick 1', c(2, 14.4), 'master', MKT, [(c(2, 14.4), 'hold', 22.5)], cam=g)
S('pick 2', c(2, 15.7), 'master', MKT, [(c(2, 15.7), 'hold', 36.5)], cam=g)
S('pick 3', c(2, 16.9), 'master', MKT, [(c(2, 16.9), 'hold', 48.5)], cam=g)
S('pick 4', c(2, 18.0), 'master', MKT, [(c(2, 18.0), 'hold', 54.3)], cam=g,
  hl=[(c(2, 21.5), c(2, 23.3), BIDS)])
FIRST = [(411, 337, 64, 87), (579, 337, 64, 87), (747, 337, 64, 87), (985, 337, 64, 87)]
S('new market', c(2, 23.4), 'master', MKT, [(c(2, 23.4), 'hold', 56.5)], cam=g,
  hl=[(c(2, 23.6) + 1.0 * k, c(2, 23.6) + 1.0 * k + 1.2, b) for k, b in enumerate(FIRST)])

# ---------- Section 3: The tracks ----------
S('photo tracks', c(3, 0.0), ph(6113), LAND, cam=(c(3, 0.0), c(3, 1.6), 1.0, 1.03, 0.5, 0.5))
MOQS = [space(199, 1138), space(346, 1104), space(494, 1070), space(642, 1070), space(790, 1070), space(937, 1070), space(1085, 1104)]
S('tracks wide', c(3, 1.6), 'master', TW1, [(c(3, 1.6), 'hold', 60.9)], cam=(c(3, 1.6), c(3, 15.6), 1.0, 1.04, 0.5, 0.5),
  hl=[(c(3, 8.1), c(3, 9.6), b) for b in MOQS] + [(c(3, 11.3), c(3, 15.3), (191, 1164, 17, 16))])
gz = (c(3, 15.6), c(3, 46.0), 1.0, 1.08, 0.2, 0.5)
S('skip', c(3, 15.6), 'master', TZ1,
  [(c(3, 15.6), 'hold', 60.9), (c(3, 19.8), 'play', 61.95, 4.0), (c(3, 21.8), 'hold', 63.0)], cam=gz,
  hl=[(c(3, 16.0), c(3, 19.6), (328, 1266, 16, 16)), (c(3, 22.0), c(3, 23.4), space(346, 1138))])
S('salt', c(3, 23.6), 'master', TZ1,
  [(c(3, 23.6), 'hold', 78.9), (c(3, 26.8), 'play', 79.1, 2.0), (c(3, 29.6), 'hold', 81.2)], cam=gz,
  hl=[(c(3, 23.8), c(3, 26.6), (486, 1198, 16, 16)), (c(3, 29.5), c(3, 31.0), (486, 1164, 16, 16)), (c(3, 31.3), c(3, 34.2), (486, 1198, 16, 16))])
S('knock', c(3, 34.6), 'master', TZ1,
  [(c(3, 34.6), 'hold', 241.4), (c(3, 38.7), 'play', 241.55, 3.0), (c(3, 42.2), 'hold', 243.6)], cam=gz,
  hl=[(c(3, 34.8), c(3, 37.0), space(199, 940)), (c(3, 37.3), c(3, 38.7), (192, 932, 14, 16)), (c(3, 40.0), c(3, 42.6), space(199, 1144))])
S('keep', c(3, 46.0), 'master', KEEP,
  [(c(3, 46.0), 'hold', 237.5), (c(3, 46.6), 'play', 237.7, 3.0), (c(3, 48.4), 'hold', 238.6)], cam=(c(3, 46.0), c(4, 0.0), 1.0, 1.05, 0.9, 0.3),
  hl=[(c(3, 47.6), c(3, 51.8), (1111, 723, 76, 103))])

# ---------- Section 4: Scoring ----------
S('storage', c(4, 0.0), 'master', TW2,
  [(c(4, 0.0), 'hold', 349.7), (c(4, 1.7), 'play', 349.7, 1.0), (c(4, 4.6), 'hold', 353.0)], cam=(c(4, 0.0), c(4, 4.8), 1.0, 1.03, 0.4, 0.4),
  hl=[(c(4, 0.3), c(4, 1.8), (480, 971, 26, 25)), (c(4, 3.0), c(4, 4.8), (480, 840, 26, 24))])
S('scoring', c(4, 4.8), 'master', TW2,
  [(c(4, 4.8), 'hold', 381.0), (c(4, 5.5), 'play', 381.1, 1.0)], cam=(c(4, 4.8), c(4, 8.0), 1.0, 1.03, 0.5, 0.4))
S('chili scoring', c(4, 8.0), 'master', TZ2,
  [(c(4, 8.0), 'hold', 382.0), (c(4, 12.6), 'play', 393.1, 3.0), (c(4, 14.1), 'hold', 394.0)], cam=(c(4, 8.0), c(4, 19.0), 1.0, 1.06, 0.2, 0.3),
  hl=[(c(4, 8.4), c(4, 12.4), (192, 844, 14, 16)), (c(4, 12.8), c(4, 14.0), (143, 800, 112, 32)), (c(4, 14.2), c(4, 18.8), (143, 866, 112, 172))])
CASH = 'img2/cashout.png'; CC = (0, 0, 1707, 960)
S('cash-out', c(4, 19.0), CASH, CC, cam=(c(4, 19.0), c(4, 29.1), 1.0, 1.05, 0.3, 0.4),
  hl=[(c(4, 20.3), c(4, 22.4), (396, 176, 800, 270)), (c(4, 22.5), c(4, 23.8), (396, 178, 800, 54)),
      (c(4, 23.9), c(4, 26.9), (396, 540, 470, 280)), (c(4, 27.0), c(4, 29.0), (396, 686, 476, 58))])
S('results', c(4, 29.1), 'img2/results2.png', CARD, cam=(c(4, 29.1), c(5, 0.0), 1.0, 1.05, 0.5, 0.4))

# ---------- Section 5: Close ----------
S('photo play', c(5, 0.0), ph(6216), port(1000), cam=(c(5, 0.0), c(5, 5.4), 1.0, 1.05, 0.5, 0.5))
S('close', c(5, 5.4), 'cards/close.png', CARD, cam=(c(5, 5.4), TOTAL, 1.0, 1.04, 0.5, 0.5),
  hl=[(c(5, 11.1), cn(5, 'want') - 0.3, tuple(B['close.url'])), (cn(5, 'email'), cn(5, 'screen', end=True) + 0.6, tuple(B['close.mail']))])

if __name__ == '__main__':
    only = sys.argv[1] if len(sys.argv) > 1 else None
    if only == 'list':
        for s in scenes: print(f"{s['at']:7.2f} {s['name']}")
        sys.exit()
    import numpy as np
    def ld(p):
        w = wave.open(p); return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
    sil = lambda d: np.zeros(int(round(d * 44100)), np.int16)
    parts = [sil(LEAD)]
    for k in range(1, 6):
        parts.append(ld(f'two/section{k}.wav')); parts.append(sil(GAP if k < 5 else TAIL))
    x = np.concatenate(parts); w = wave.open('two/full.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(44100); w.writeframes(x.tobytes()); w.close()
    assemble(scenes, TOTAL)
    run(['-i', 'seg2/video.mp4', '-i', 'two/full.wav', '-vf', f'fade=in:0:15,fade=out:st={TOTAL - 1.2:.2f}:d=1.2',
         '-af', f'afade=out:st={TOTAL - 0.8:.2f}:d=0.8', '-c:v', 'libx264', '-crf', '18', '-preset', 'slow', '-pix_fmt', 'yuv420p',
         '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-shortest', 'saffron-salt-pitch-final-B.mp4'])
    print('total', round(TOTAL, 2))

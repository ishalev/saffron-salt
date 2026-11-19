# Build two-voice section WAVs from Isaac's solo sections and Mitch's take.
import wave, json, numpy as np, subprocess
FF = r"C:/Users/ishal/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-9.0.2-full_build/bin/ffmpeg.exe"
SR = 44100
subprocess.run([FF, '-hide_banner', '-loglevel', 'error', '-y', '-i', 'mitch/vox.wav', '-ac', '1', '-ar', str(SR),
  '-af', 'acompressor=threshold=0.125:ratio=3:attack=5:release=120', 'two/mitch_comp.wav'], check=True)
def load(p):
    w = wave.open(p); return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)
IS = {k: load(f'audio/section{k}.wav') for k in range(1, 6)}
MI = load('two/mitch_comp.wav')
IW = {int(k): v for k, v in json.load(open('words/words.json')).items()}
MW = json.load(open('mitch/words.json'))

def span(words, t0, t1):
    """first word starting at ~t0 to last word starting at ~t1 (start times, 0.05 tolerance)"""
    ws = [w for w in words if t0 - 0.05 <= w[0] <= t1 + 0.05]
    return ws[0][0], ws[-1][1], ws
def cut(sig, words, t0, t1):
    a, b, ws = span(words, t0, t1)
    nxt = [w[0] for w in words if w[0] > b - 0.01]
    prv = [w[1] for w in words if w[1] < a + 0.01]
    s = max(a - 0.15, (prv[-1] + a) / 2 if prv else 0)
    e = min(b + 0.30, (nxt[0] + b) / 2 if nxt else b + 0.30)
    seg = sig[int(s * SR):int(e * SR)].copy()
    f = int(0.012 * SR); r = np.linspace(0, 1, f)
    seg[:f] *= r; seg[-f:] *= r[::-1]
    return seg, ' '.join(w[2] for w in ws)

def rms_db(x): return 20 * np.log10(np.sqrt(np.mean(x ** 2)) / 32768 + 1e-12)
# speech-only level: average of 50 ms frames above -45 dBFS
def speech_db(x):
    n = int(0.05 * SR); fr = x[:len(x) // n * n].reshape(-1, n)
    e = np.sqrt((fr ** 2).mean(1)) / 32768; e = e[20 * np.log10(e + 1e-12) > -45]
    return 20 * np.log10(np.sqrt((e ** 2).mean()))
gain = 10 ** ((speech_db(np.concatenate(list(IS.values()))) - speech_db(MI)) / 20)
gdb = 20 * np.log10(gain); print('mitch gain dB', round(gdb, 2))
subprocess.run([FF, '-hide_banner', '-loglevel', 'error', '-y', '-i', 'two/mitch_comp.wav',
  '-af', f'volume={gdb:.2f}dB,alimiter=limit=0.89:attack=3:release=60:level=false', 'two/mitch_lim.wav'], check=True)
MI = load('two/mitch_lim.wav'); gain = 1.0

I = lambda k, a, b: ('I', k, a, b)
M = lambda a, b: ('M', 0, a, b)
PLAN = {
 1: [I(1, 0.0, 2.5), M(1.4, 14.3), I(1, 16.4, 31.0)],
 2: [I(2, 0.0, 19.7), M(19.6, 33.5)],
 3: [M(40.5, 55.0), I(3, 15.6, 33.9), M(61.0, 71.9), I(3, 46.0, 54.5)],
 4: [M(76.7, 94.0), I(4, 19.0, 37.5)],
 5: [M(101.3, 105.8), I(5, 5.4, 14.2), M(111.5, 116.3)],
}
GAP = np.zeros(int(0.45 * SR), np.float32)
pieces = {}
for k, plan in PLAN.items():
    out = []; meta = []; t = 0.0
    for j, (who, sk, a, b) in enumerate(plan):
        if who == 'I': seg, txt = cut(IS[sk], IW[sk], a, b)
        else: seg, txt = cut(MI, MW, a, b); seg = seg * gain
        if j: out.append(GAP); t += len(GAP) / SR
        meta.append((who, round(t, 3), round(len(seg) / SR, 3), txt[:60] + ' ... ' + txt[-30:]))
        out.append(seg); t += len(seg) / SR
    x = np.clip(np.concatenate(out), -32768, 32767).astype(np.int16)
    w = wave.open(f'two/section{k}.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(x.tobytes()); w.close()
    print(f'== section {k}: {len(x) / SR:.2f}s')
    for m in meta: print('  ', m)
    pieces[k] = meta
json.dump(pieces, open('two/pieces.json', 'w'))

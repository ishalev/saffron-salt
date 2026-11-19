import sys, types, wave, json, numpy as np
sys.modules['av'] = types.ModuleType('av')
from faster_whisper import WhisperModel
d = sys.argv[1]
m = WhisperModel("small.en", device="cpu", compute_type="int8")
out = {}
for k in range(1, 6):
    w = wave.open(f"{d}/s{k}.wav")
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    segs, _ = m.transcribe(a, language="en", word_timestamps=True, vad_filter=False, beam_size=5)
    words = [(round(x.start, 2), round(x.end, 2), x.word.strip()) for s in segs for x in s.words]
    out[k] = words
    print(f"== section {k}")
    print(" ".join(f"{s:.1f}:{t}" for s, e, t in words))
json.dump(out, open(f"{d}/words.json", "w"), indent=0)

import sys, types, wave, json, numpy as np
sys.modules['av'] = types.ModuleType('av')
from faster_whisper import WhisperModel
m = WhisperModel("small.en", device="cpu", compute_type="int8")
w = wave.open("mitch/vox16.wav")
a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
segs, _ = m.transcribe(a, language="en", word_timestamps=True, vad_filter=False, beam_size=5)
words = [(round(x.start, 2), round(x.end, 2), x.word.strip()) for s in segs for x in s.words]
json.dump(words, open("mitch/words.json", "w"))
line = []
for s, e, t in words:
    line.append(f"{s:.1f}:{t}")
print(" ".join(line))

# Helpers for draft 2: master video from screencast frames, scenes with holds/plays,
# fading highlights, slow camera moves and crossfades at cue times.
import subprocess, json, os, bisect
FF = r"C:/Users/ishal/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-9.0.2-full_build/bin/ffmpeg.exe"
FPS = 30
W4, H4 = 3840, 2160
RED = '0xC8202F'

def run(a):
    subprocess.run([FF, '-hide_banner', '-loglevel', 'error', '-y'] + a, check=True)

class Rec:
    def __init__(self, d):
        self.d = d
        L = json.load(open(f'{d}/log.json'))
        self.F = L['frames']; self.f0 = self.F[0]
        self.ev = [(ms / 1000 - self.f0, l) for ms, l in L['events']]
        self.master = f'{d}/master.mp4'
    def build_master(self):
        if os.path.exists(self.master): return
        lines = []
        for i, t in enumerate(self.F):
            dur = (self.F[i + 1] - t) if i + 1 < len(self.F) else 2.0
            lines.append(f"file 'frames/{i:06d}.jpg'\nduration {dur:.4f}\n")
        lines.append(f"file 'frames/{len(self.F) - 1:06d}.jpg'\n")
        open(f'{self.d}/frames.txt', 'w').write(''.join(lines))
        run(['-f', 'concat', '-safe', '0', '-i', f'{self.d}/frames.txt', '-vf', f'fps={FPS},format=yuv420p',
             '-c:v', 'libx264', '-crf', '12', '-preset', 'veryfast', self.master])
    def t(self, pat, k=0):
        hits = [t for t, l in self.ev if pat in l]
        if len(hits) <= k: raise KeyError(pat)
        return hits[k]
    def frame_at(self, t):
        return max(0, bisect.bisect_right(self.F, t + self.f0) - 1)

def sc(v, c):
    """map a box in source coords (x,y,w,h) to 4K scene coords given crop c"""
    x, y, w, h = v; cx, cy, cw, ch = c
    k = W4 / cw
    return int((x - cx) * k), int((y - cy) * k), int(w * k), int(h * k)

N = [0]
def tmp(ext='mp4'):
    N[0] += 1; os.makedirs('seg2', exist_ok=True); return f'seg2/{N[0]:03d}.{ext}'

def piece_files(scene):
    """render the scene's base at 4K: list of pieces concatenated"""
    c = scene['crop']; x, y, w, h = c
    vfc = f"crop={w}:{h}:{x}:{y},scale={W4}:{H4}:flags=lanczos,setsar=1"
    outs = []
    for p in scene['pieces']:
        kind, t0, d = p[0], p[1], p[2]
        o = tmp()
        if scene['src'] == 'master':
            if kind == 'hold':
                png = tmp('png')
                run(['-ss', f'{t0:.3f}', '-i', scene['rec'].master, '-frames:v', '1', '-vf', vfc, png])
                run(['-loop', '1', '-framerate', str(FPS), '-i', png, '-t', f'{d:.3f}', '-c:v', 'libx264', '-crf', '14', '-preset', 'ultrafast', '-pix_fmt', 'yuv420p', o])
            else:
                slow = p[3] if len(p) > 3 else 1.0
                run(['-ss', f'{t0:.3f}', '-i', scene['rec'].master, '-t', f'{d / slow:.3f}', '-vf', f'{vfc},setpts={slow}*PTS,' + (f'minterpolate=fps={FPS}:mi_mode=blend' if slow > 1 else f'fps={FPS}'), '-t', f'{d:.3f}',
                     '-c:v', 'libx264', '-crf', '14', '-preset', 'ultrafast', '-pix_fmt', 'yuv420p', o])
        else:  # still image
            run(['-loop', '1', '-framerate', str(FPS), '-i', scene['src'], '-t', f'{d:.3f}', '-vf', f'format=rgb24,{vfc},format=yuv420p',
                 '-c:v', 'libx264', '-crf', '14', '-preset', 'ultrafast', o])
        outs.append(o)
    if len(outs) == 1: return outs[0]
    o = tmp()
    ins = sum([['-i', f] for f in outs], [])
    fc = ''.join(f'[{i}:v]' for i in range(len(outs))) + f'concat=n={len(outs)}:v=1:a=0[v]'
    run(ins + ['-filter_complex', fc, '-map', '[v]', '-c:v', 'libx264', '-crf', '14', '-preset', 'ultrafast', '-pix_fmt', 'yuv420p', o])
    return o

def render_scene(scene, vis0, L):
    """vis0 = global time when the scene becomes visible; L = rendered length"""
    # scene['ev'] = [(global_start, 'hold', master_t) | (global_start, 'play', master_t[, slow])]
    # a 'play' runs until the next event; after the last play, it holds its final frame.
    evs = scene.get('ev') or [(scene['at'], 'hold', 0.0)]
    vis1 = vis0 + L
    pieces = []
    for k, e in enumerate(evs):
        s = vis0 if k == 0 else max(vis0, e[0])
        en = evs[k + 1][0] if k + 1 < len(evs) else vis1
        en = min(en, vis1)
        if en - s < 1 / FPS: continue
        if e[1] == 'hold': pieces.append(('hold', e[2], en - s))
        else: pieces.append(('play', e[2], en - s) + tuple(e[3:]))
    scene['pieces'] = pieces
    base = piece_files(scene)
    fc = '[0:v]format=yuv420p[b0];'
    cur = 'b0'; ins = ['-i', base]
    for j, (g0, g1, box) in enumerate(scene.get('hl', [])):
        t0 = max(0.0, g0 - vis0); t1 = min(L, g1 - vis0)
        if t1 <= 0 or t0 >= L: continue
        bx, by, bw, bh = sc(box, scene['crop'])
        pad = 18
        o2 = pad + 14
        fc += (f"color=c=black:s={W4}x{H4}:r={FPS}:d={L:.3f},format=gray,"
               f"drawbox=x={bx - o2}:y={by - o2}:w={bw + 2 * o2}:h={bh + 2 * o2}:color=0x606060:t=14,"
               f"drawbox=x={bx - pad}:y={by - pad}:w={bw + 2 * pad}:h={bh + 2 * pad}:color=white:t=12[m{j}];"
               f"color=c={RED}:s={W4}x{H4}:r={FPS}:d={L:.3f},format=rgba[c{j}];"
               f"[c{j}][m{j}]alphamerge,fade=t=in:st={t0:.3f}:d=0.5:alpha=1,fade=t=out:st={max(t0 + 0.5, t1 - 0.5):.3f}:d=0.5:alpha=1[h{j}];"
               f"[{cur}][h{j}]overlay=format=auto[o{j}];")
        cur = f'o{j}'
    g0, g1, z0, z1, fx, fy = scene['cam']
    n0 = (vis0 - g0) * FPS; span = max(1.0, (g1 - g0) * FPS)
    z = f"{z0}+({z1}-{z0})*min(1\\,max(0\\,(on+{n0:.2f})/{span:.2f}))"
    fc += f"[{cur}]zoompan=z='{z}':x='{fx}*(iw-iw/zoom)':y='{fy}*(ih-ih/zoom)':d=1:s=1920x1080:fps={FPS},format=yuv420p[v]"
    o = tmp()
    run(ins + ['-filter_complex', fc, '-map', '[v]', '-t', f'{L:.3f}', '-r', str(FPS), '-c:v', 'libx264', '-crf', '15', '-preset', 'fast', '-pix_fmt', 'yuv420p', o])
    return o

def assemble(scenes, total, X=0.5):
    """scenes: list with 'at' (global cue time). first at 0."""
    files = []
    for i, s in enumerate(scenes):
        b_prev = s['at']; b_next = scenes[i + 1]['at'] if i + 1 < len(scenes) else total
        vis0 = 0.0 if i == 0 else b_prev - X / 2
        vis1 = total if i + 1 == len(scenes) else b_next + X / 2
        L = vis1 - vis0
        print(f"scene {i:2d} at {s['at']:6.2f} len {L:5.2f} {s.get('name', '')}", flush=True)
        files.append(render_scene(s, vis0, L))
    ins = sum([['-i', f] for f in files], [])
    fc = ''; cur = '0:v'
    for i in range(1, len(files)):
        off = scenes[i]['at'] - X / 2
        out = f'x{i}'
        fc += f"[{cur}][{i}:v]xfade=transition=fade:duration={X}:offset={off:.3f}[{out}];"
        cur = out
    fc = fc.rstrip(';')
    run(ins + ['-filter_complex', fc, '-map', f'[{cur}]', '-c:v', 'libx264', '-crf', '16', '-preset', 'medium', '-pix_fmt', 'yuv420p', 'seg2/video.mp4'])

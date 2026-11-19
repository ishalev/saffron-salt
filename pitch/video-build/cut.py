import wave, sys, array, math, json, os
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
w=wave.open(src,'rb'); ch,sw,sr,n=w.getnchannels(),w.getsampwidth(),w.getframerate(),w.getnframes()
raw=w.readframes(n); a=array.array('h',raw)
mono=array.array('h',[(a[i]+a[i+1])//2 for i in range(0,len(a),2)]) if ch==2 else a
W=int(sr*0.01); THR=-50
lv=[]
for i in range(0,len(mono),W):
    seg=mono[i:i+W]; r=math.sqrt(sum(x*x for x in seg)/len(seg)); lv.append(20*math.log10(r/32768+1e-12))
loud=[l>=THR for l in lv]
# speech runs (merge gaps < 0.25s)
runs=[];s=None
for i,v in enumerate(loud+[False]):
    if v and s is None: s=i
    if not v and s is not None: runs.append([s,i]); s=None
m=[runs[0]]
for r in runs[1:]:
    if r[0]-m[-1][1] < 25: m[-1][1]=r[1]
    else: m.append(r)
m=[r for r in m if r[1]-r[0]>=5]  # drop blips <50ms
# sections: split where gap >= 3s
secs=[[m[0]]]
for r in m[1:]:
    if r[0]-secs[-1][-1][1] >= 300: secs.append([r])
    else: secs[-1].append(r)
print(len(secs),"sections")
PRE,POST,MAXGAP=0.15,0.20,0.45
info=[]
for k,sec in enumerate(secs,1):
    pieces=[]
    for j,r in enumerate(sec):
        st=r[0]*0.01-PRE; en=r[1]*0.01+POST
        if j>0:
            gap=r[0]*0.01-sec[j-1][1]*0.01
            if gap<=MAXGAP+0.0: st=sec[j-1][1]*0.01+POST  # keep natural short gap whole
        pieces.append((max(st,0),en))
    # merge overlapping
    mp=[list(pieces[0])]
    for p in pieces[1:]:
        if p[0]<=mp[-1][1]: mp[-1][1]=max(mp[-1][1],p[1])
        else: mp.append(list(p))
    data=array.array('h')
    for st,en in mp:
        seg=mono[int(st*sr):int(en*sr)]
        f=int(sr*0.01)  # 10ms fades at joins
        seg=array.array('h',seg)
        for i in range(min(f,len(seg))):
            seg[i]=int(seg[i]*i/f); seg[-1-i]=int(seg[-1-i]*i/f)
        data.extend(seg)
    p=os.path.join(out,f"section{k}_raw.wav")
    o=wave.open(p,'wb'); o.setnchannels(1); o.setsampwidth(2); o.setframerate(sr); o.writeframes(data.tobytes()); o.close()
    orig=(sec[-1][1]-sec[0][0])*0.01
    info.append((k,sec[0][0]*0.01,orig,len(data)/sr))
    print(f"section {k}: starts {sec[0][0]*0.01:6.1f}s  original {orig:5.1f}s -> tightened {len(data)/sr:5.1f}s")
print(f"total tightened speech {sum(i[3] for i in info):.1f}s")

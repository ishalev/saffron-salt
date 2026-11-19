import subprocess, wave, os
B=r"C:/Users/ishal/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-9.0.2-full_build/bin/ffmpeg.exe"
PH=r"G:/My Drive/Games/Saffron Salt/02 Exploration/v1.16 - saffron +1face down, bonus auction 10-5-2/Test 260721 - CARY/IMG_%s.jpeg"
M='rec/master.mp4'; BG='0xFBF5EE'; os.makedirs('seg',exist_ok=True)
def dur(p):
    w=wave.open(p); return w.getnframes()/w.getframerate()
S=[dur(f'audio/section{k}.wav') for k in range(1,6)]
LEAD,GAP,TAIL=1.0,0.8,3.0
OUT='-r 30 -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p -an'.split()
def run(args): subprocess.run([B,'-hide_banner','-loglevel','error','-y']+args,check=True)
CROPS={'market':(200,80,1200,675),'tracks':(110,636,1070,602),'top':(0,0,1600,900),'modal':(400,395,800,450)}
n=[0]
def nxt(): n[0]+=1; return f'seg/{n[0]:02d}.mp4'
segs=[]
def still(img,d,z0=1.0,z1=1.08,pre=''):
    o=nxt(); fr=int(d*30)
    vf=f"{pre}format=rgb24,scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160,zoompan=z='{z0}+({z1}-{z0})*on/{fr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={fr}:s=1920x1080:fps=30,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p"
    run(['-loop','1','-i',img,'-frames:v',str(fr),'-vf',vf]+OUT+[o]); segs.append(o)
def clip(kind,t,d):
    o=nxt()
    if kind=='full': vf=f"scale=-2:1080:flags=lanczos,pad=1920:1080:(ow-iw)/2:0:color={BG}"
    else:
        x,y,w,h=CROPS[kind]; vf=f"crop={w}:{h}:{x}:{y},scale=1920:1080:flags=lanczos"
    run(['-ss',str(t),'-i',M,'-t',f'{d:.3f}','-vf',vf+',fps=30']+OUT+[o]); segs.append(o)
# results still: header + score charts from the final frame
run(['-ss','245.5','-i',M,'-frames:v','1','-filter_complex',"[0]crop=1040:215:280:55[a];[0]crop=1040:192:280:1015[b];[a][b]vstack,scale=1840:-2:flags=lanczos,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color="+BG,'img/results.png'])
# Section 1
d1=LEAD+S[0]+GAP; still('cards/title.png',9.0,1.0,1.04); still(PH%'6723',7.5); still(PH%'6720',6.5,1.08,1.0); clip('top',5.0,d1-23.0)
# Section 2
d2=S[1]+GAP; a=12.0; b=12.5; clip('market',4.0,a); clip('market',92.0,b); clip('market',109.0,d2-a-b)
# Section 3
d3=S[2]+GAP; a=23.0; b=18.5; clip('tracks',14.0,a); clip('tracks',42.2,b); clip('tracks',63.0,d3-a-b)
# Section 4
d4=S[3]+GAP; parts=[('tracks',69.3,12.7),('tracks',82.0,4.7),('modal',86.7,5.1),('tracks',231.8,4.9),('modal',236.7,5.0)]
for k,t,d in parts: clip(k,t,d)
still('img/results.png',d4-sum(p[2] for p in parts),1.0,1.03)
# Section 5
d5=S[4]+TAIL; clip('market',186.4,6.0); still('cards/close.png',d5-6.0,1.0,1.03)
open('seg/list.txt','w').write(''.join(f"file '{os.path.basename(s)}'\n" for s in segs))
run(['-f','concat','-safe','0','-i','seg/list.txt','-c','copy','seg/video.mp4'])
# audio
run(['-f','lavfi','-t',str(LEAD),'-i','anullsrc=r=44100:cl=mono','audio/lead.wav'])
run(['-f','lavfi','-t',str(TAIL),'-i','anullsrc=r=44100:cl=mono','audio/tail.wav'])
order=['lead.wav']+sum([[f'section{k}.wav','silence.wav'] for k in range(1,5)],[])+['section5.wav','tail.wav']
open('audio/full.txt','w').write(''.join(f"file '{f}'\n" for f in order))
run(['-f','concat','-safe','0','-i','audio/full.txt','audio/full.wav'])
total=LEAD+sum(S)+4*GAP+TAIL
run(['-i','seg/video.mp4','-i','audio/full.wav','-vf',f'fade=in:0:15,fade=out:st={total-1.2:.2f}:d=1.2','-af',f'afade=out:st={total-0.8:.2f}:d=0.8','-c:v','libx264','-crf','18','-preset','slow','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','-shortest','saffron-salt-pitch.mp4'])
print('sections',[round(x,2) for x in S],'total',round(total,2))

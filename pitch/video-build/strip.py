import sys, subprocess
FF=r"C:/Users/ishal/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-9.0.2-full_build/bin/ffmpeg.exe"
t0,t1,step=map(float,sys.argv[1:4]); x,y,w,h=map(int,sys.argv[4].split(',')); cols=int(sys.argv[5]); out=sys.argv[6]; sc=float(sys.argv[7]) if len(sys.argv)>7 else 1
n=int((t1-t0)/step+0.5); rows=(n+cols-1)//cols
vf=rf"fps=1/{step},crop={w}:{h}:{x}:{y},scale=iw*{sc}:-2,drawtext=text='%{{eif\:t*{step}*0+{t0}+n*{step}\:d\:1}}':fontsize=20:fontcolor=white:box=1:boxcolor=black:x=4:y=4:fontfile='C\:/Windows/Fonts/arial.ttf',tile={cols}x{rows}"
subprocess.run([FF,'-loglevel','error','-y','-ss',str(t0),'-i','rec2/full/master.mp4','-t',str(t1-t0),'-vf',vf,'-frames:v','1',out],check=True)

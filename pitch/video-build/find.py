import subprocess, numpy as np, sys
FF=r"C:/Users/ishal/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-9.0.2-full_build/bin/ffmpeg.exe"
W,H=1600,1900
def frame(t):
    b=subprocess.run([FF,'-loglevel','error','-ss',str(t),'-i','rec2/full/master.mp4','-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True,check=True).stdout
    return np.frombuffer(b,np.uint8).reshape(H,W,3).astype(int)
def blobs(img,rgb,x0,x1,y0,y1,tol=40,minpix=30):
    sub=img[y0:y1,x0:x1]; m=(np.abs(sub-np.array(rgb)).sum(2)<tol)
    ys,xs=np.nonzero(m)
    if not len(ys): return []
    # cluster by rows (gap>6)
    order=np.argsort(ys); ys,xs=ys[order],xs[order]; out=[]; start=0
    for i in range(1,len(ys)+1):
        if i==len(ys) or ys[i]-ys[i-1]>6:
            yy,xx=ys[start:i],xs[start:i]
            if len(yy)>=minpix: out.append((int(xx.min()+x0),int(yy.min()+y0),int(xx.max()-xx.min()+1),int(yy.max()-yy.min()+1),len(yy)))
            start=i
    return out

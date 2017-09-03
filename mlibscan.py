import os,sys
from datetime import datetime,timedelta
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.aac import AAC

audio_ext={"mp3":lambda x: MP3(x).info.length,
           "flac":lambda x:FLAC(x).info.length,
           "aac":lambda x:AAC(x).info.length
          }
playtime=0

def scan_lib(path):
    global playtime
    for cdir,lsdir,lsf in os.walk(path):
        for f in lsf:
           try:
               playtime+=audio_ext[f[len(f)-f[::-1].index('.'):]](os.path.join(cdir,f))
           except KeyError:
              pass
        for d in lsdir:
            scan_lib(os.path.abspath(d))

scan_lib(sys.argv[1])
t = datetime(1,1,1) + timedelta(seconds=int(playtime)) 
print("Days:\tHours:\tMin:\tSec:")
print("%d\t%d\t%d\t%d" % (t.day-1, t.hour,t.minute,t.second))



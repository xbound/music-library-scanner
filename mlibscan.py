import os,sys,argparse,json
from datetime import datetime,timedelta
try:
    from mutagen.mp3 import MP3
    from mutagen.flac import FLAC
    from mutagen.aac import AAC
    from mutagen.aiff import AIFF
    from mutagen.asf import ASF
except ImportError as e:
    print("Mutagen library is not intalled...")
    sys.exit(1)

audio_ext={"mp3":lambda x: MP3(x).info.length,
           "aac":lambda x: AAC(x).info.length,
           "wmv":lambda x: ASF(x).info.length,
           "wma":lambda x: ASF(x).info.length,
           "asf":lambda x: ASF(x).info.length,
           "flac":lambda x: FLAC(x).info.length,
           "aiff":lambda x: AIFF(x).info.length}
json_list = []

def scan_lib(path):
    playtime = 0
    audio_files = 0
    folder_audio = 0
    audio_subfolders = 0
    for entry in os.listdir(path):
        entry = os.path.join(path,entry)
        if os.path.isdir(entry):
            dir_playtime,dir_audios,dir_faudio,dir_subfolders = scan_lib(entry)
            playtime +=dir_playtime
            audio_files += dir_audios
            audio_subfolders += 1 if dir_playtime > 0 else 0
        else:
           try:
               ext = entry[len(entry)-entry[::-1].index('.'):]
               if args.filter:
                   if ext in args.filter:
                        playtime += audio_ext[ext](entry)
                        audio_files+=1
                        folder_audio += 1
               else:
                   playtime += audio_ext[ext](entry)
                   audio_files += 1
                   folder_audio += 1
           except (KeyError,ValueError):
               if args.skipped: print("Skipped:",entry)
    if args.each:
        if args.json:
            json_list.append(make_json_obj(path,playtime,audio_files,folder_audio,audio_subfolders))
        if not args.quiet:
            print_info(path,audio_files,folder_audio,audio_subfolders,playtime)

    return playtime,audio_files,folder_audio,audio_subfolders

def convert_pt(sec):
    t = datetime(1,1,1) + timedelta(seconds=int(sec))
    return t.day-1, t.hour,t.minute,t.second

def print_info(path,audio_files,folder_audio,audio_subfolders,playtime):
    print("\nLibrary:",path)
    print("Amount of audio subfolders:",audio_subfolders)
    print("Amount of audio files in library:",folder_audio)
    print("Total amount of audio files in library:",audio_files)
    print("Total playing time:\nDays\tHours\tMin\tSec\n%d\t%d\t%d\t%d\n" % convert_pt(playtime))

def make_json_obj(path,playtime,audio_files,folder_audio,subfolders):
             return {"path":path,
            "playtime":str(playtime),
            "all-tracks":str(audio_files),
            "tracks":str(folder_audio),
            "subfolders":str(subfolders)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p","--path",help="path to music folder/library",type=str,required=True)
    parser.add_argument("-f","--filter",help="scan only for audio files with specific extensions",nargs="+")
    parser.add_argument("-e","--each",help="show info for each subfolder/library",action="store_true")
    parser.add_argument("-s","--skipped",help="print skipped files",action="store_true")
    parser.add_argument("--json",help="save output as json format file")
    parser.add_argument("-q","--quiet",help="do not print output on console",action="store_true")
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit()
    args = parser.parse_args()
    try:
        playtime,audio_files,folder_audio,audio_subfolders = scan_lib(os.path.realpath(args.path))
    except KeyboardInterrupt:
        sys.exit(1)
    if not args.quiet:
        if not args.each: print_info(args.path,audio_files,folder_audio,audio_subfolders,playtime)
    if args.json:
        if not args.each:
            with open(args.json,"w+") as f:
                 json.dump(make_json_obj(args.path,playtime,audio_files,folder_audio,audio_subfolders),f)
        else:
            with open(args.json,"w+") as f:
                json.dump(json_list,f)

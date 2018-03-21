# Python Music Library Scanner

Simple python script for scanning music folders. Script can provide information about amount of tracks in folder and its subfolders and information about total library's playtime.

Supported audio extensions: MP3, AAC, ASF, WMW, WMA, FLAC, AIFF.

## Prerequisites

* Python 2.7+ (Python3.5 recommended)
* [Mutagen](https://mutagen.readthedocs.io/) library installed

        $ pip install -r requirements.txt


## Usage

In order to get help you can type script name without any arguments 
	
	$ python3 mlibscan.py
	
Or type:
	
	$ python3 mliscan.py -h
	
Script arguments:

     -h, --help            shows help message and exits
    -p PATH, --path PATH  path to music folder/library
    -f [FILTER ...], --filter [FILTER ...]
                  	      scans only for audio files with specific extensions
     
	-e, --each            outputs info for each subfolder
	-s, --skipped         prints skipped files
  	--json FILE           saves output as json in file
  	-q, --quiet           would not print output on console
  	
  
## Example

 Show info about ~/Music folder:
 	
 	$ python3 mliscan.py -p ~/Music
 	
 	Library: /home/user/Music/
	Amount of audio subfolders: 1
	Amount of audio files in library: 95
	Total amount of audio files in library: 135
	Total playing time:
	Days	Hours	Min	Sec
	0		12		48	67
	
Show info about folder and all its subfolders:
	
	$ python3 mliscan.py -p ~/Music -e
	
	Library: /home/user/Music/Best EDM of 2017
	Amount of audio subfolders: 0
	Amount of audio files in library: 40
	Total amount of audio files in library: 40
	Total playing time:
	Days	Hours	Min	Sec
	0		2		17	18
	
	Library: /home/user/Music/
	Amount of audio subfolders: 1
	Amount of audio files in library: 95
	Total amount of audio files in library: 135
	Total playing time:
	Days	Hours	Min	Sec
	0		12		48	67


Include only audio with .mp3 extension:
	
	$ python3 mliscan.py -p ~/Music -e -f mp3
	
Save ouput in JSON format to file:
	
	$ python3 mliscan.py -p ~/Music -e -f mp3  --json new_file.txt
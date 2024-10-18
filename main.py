import os
import defs
from defs import shell

stream = open('stream.txt', 'r')
data = stream.readlines()
stream.close()

#get stream data
stream_name = data[0].strip().split(";")[1]
stream_link = data[1].strip().split(";")[1]
del data[1]
del data[0]

#Separate song data
songs = []
for music in data:
    songs.append(music.replace(" ", "|").strip().replace("|", " ").split(";"))

#Program Start
print("Stream: " + stream_name)
print("Link: " + stream_link)
print("Song Data: " + str(songs))

#download stream
stream_file = "stream.mp4"
if not os.path.isfile(stream_file):
    print("Downloading stream, please wait")
    ytdl = shell(['yt-dlp', stream_link, '-o', stream_file])
    print("Stream downloaded")
else:
    print("Stream file exists, cutting songs")

#Split songs from stream
for song in songs:
    if not os.path.isfile("output/" + song[0] + ".mp4"): #MP4 Version
        ff = shell(['ffmpeg', '-y', '-ss', song[1], '-to', song[2], '-i', stream_file, '-c', 'copy', "output/" + song[0] + ".mp4"])
        if str(ff.returncode) != "0":
            print("Error cutting song: " + song[0])
    if not os.path.isfile("output/" + song[0] + ".mp3"): #MP3 Version
        ff = shell(['ffmpeg', '-y', '-i', "output/" + song[0] + ".mp4", "output/" + song[0] + ".mp3"])
        if str(ff.returncode) != "0":
            print("Error cutting song: " + song[0])
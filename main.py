import os
import defs
import music_tag
from defs import shell

stream = open('stream.txt', 'r')
data = stream.readlines()
stream.close()

#get stream data
stream_name = data[0].strip().split(";")[1]
stream_link = data[1].strip().split(";")[1]
streamer_name = data[2].strip().split(";")[1]
mp3_image = data[3].strip().split(";")[1]
upload_to_youtube = data[4].strip().split(";")[1]
del data[4]
del data[3]
del data[2]
del data[1]
del data[0]

#Separate song data
songs = []
for music in data:
    songs.append(music.replace(" ", "|").strip().replace("|", " ").split(";"))

#Program Start
print("Streamer: " + streamer_name + " [ " + mp3_image + " ]")
print("Stream: " + stream_name)
print("Link: " + stream_link)
print("Song Data: " + str(songs))

#download stream
#stream_file = "stream.mp4"
stream_file = "/tmp/stream/" + stream_name + ".mkv"
if not os.path.isfile(stream_file):
    print("Downloading stream, please wait")
    stream_file = "/tmp/stream/" + stream_name
    ytdl = shell(['yt-dlp', stream_link, '-o', stream_file])
    stream_file = "/tmp/stream/" + stream_name + ".mkv"
    print("Stream downloaded, processing songs")
else:
    print("Stream file exists, processing songs")

#Split songs from stream
stream_name = stream_name.strip()
shell(['mkdir', '-p', "output/" + stream_name])
shell(['mkdir', '-p', "output/" + stream_name + "/mp3"])
shell(['mkdir', '-p', "output/" + stream_name + "/mp4"])
song_num = 1
for song in songs:
    mp3_path = "output/" + stream_name + "/mp3/" + song[0] + ".mp3"
    mp4_path = "output/" + stream_name + "/mp4/" + song[0] + ".mp4"
    if not os.path.isfile(mp4_path): #MP4 Version
        ff = shell(['ffmpeg', '-y', '-ss', song[1], '-to', song[2], '-i', stream_file, '-c', 'copy', mp4_path])
        if str(ff.returncode) != "0":
            print("Error cutting song: " + song[0])
    if not os.path.isfile("output/" + stream_name + "/mp3/" + song[0] + ".mp3"): #MP3 Version
        ff = shell(['ffmpeg', '-y', '-i', mp4_path, mp3_path])
        tg = music_tag.load_file(mp3_path)
        tg['title'] = song[0].split(" - ")[0].replace(" ", "|").strip().replace("|", " ")
        tg['title'] = song[0].split(" - ")[0].replace(" ", "|").strip().replace("|", " ")
        tg['artist'] = streamer_name
        tg['tracknumber'] = song_num
        song_num += 1
        tg['album'] = stream_name
        if os.path.isfile(mp3_image):
            with open(mp3_image, 'rb') as img_in:
                tg['artwork'] = img_in.read()
        tg.save()
        if str(ff.returncode) != "0":
            print("Error cutting song: " + song[0])
    if upload_to_youtube == "yes":
        print("Uploading " + song[0])
        up = shell(['./yt-upload', '[' + streamer_name + ']' + ' ' + song[0], stream_link, mp4_path])
        if str(up.returncode) != "0":
            print("Upload failed!")
print("All songs saved and tags applied")
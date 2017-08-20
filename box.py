import web
import pygame
import time
import random
import glob
import clint

# VARS
global currentSong
global songThread
global mixer_init
global randomSongNext
global pauseStatus
global playStatus
global songList
global playPause

songListMusic = sorted(glob.glob("music/*.ogg"))
randomSongNext = "Nothing"
currentSong = "Nothing"
playStatus = 0
pauseStatus = 0
songListStripped = [j.strip("music/").strip(".ogg") for j in songListMusic]
playPause = "Play/Pause"

#DEFINING URLS

urls = (
  '/', 'index',
  '/api/0.2/song/', 'apiSong',
  '/api/0.2/ctrl/', 'apiCtrl',
  '/jukebox', 'jukebox')

app = web.application(urls, globals(), True)
render = web.template.render('templates/')

# WEB SHIT

class index:
    def GET(self):
        web.redirect('/jukebox')

class apiCtrl:
        def GET(self):
            data = web.input()
            ctrl = data.ctrl
            print ctrl
            if currentSong == "nothing":
                print "LOG: SONG NOT SET"
            if ctrl == "play":
                musicPlay(currentSong)

            web.seeother('/jukebox')

class apiSong:
        def GET(self):
            data = web.input()
            print("LOG: SONG SET: "+ data.song)
            global currentSong
            currentSong = data.song
            time.sleep(1)
            web.seeother('/jukebox')

class jukebox:
    def GET(self):
        time.sleep(1)
        global currentSong
        return render.jukeboxv2("Jukebox", str(currentSong.strip("music/").strip(str(".ogg"))), "A jukebox of sorts.", songListStripped, playPause)

# ACTUAL MUSIC SHIT

def musicPlay(song):
    global playStatus
    if playStatus == 0:
        pygame.mixer.music.load("music/" + song + ".ogg")
        pygame.mixer.music.play()
        playStatus = 1
        playPause = "Pause"
    elif playStatus == 1:
        if pauseStatus == 0:
            pygame.mixer.music.stop()
            playStatus = 0
            playPause = "Play"

def musicStop():
    pygame.mixer.music.stop()
    playStatus = 0

# Y U NO WERK

if __name__ == "__main__":
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.mixer.init()
    playStatus = 0
    print songListMusic
    print songListStripped
    app.run()

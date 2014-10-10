#!/usr/bin/env python

import subprocess
import time
import os
import signal
from grooveshark import Client
from multiprocessing import Process

class MusicPlayerObject(object):

    def __init__(self):
        self.client = Client()
        self.client.init()
        self.playing = False

    def is_playing(self):
        return self.playing

    def stop(self):
        p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
        out, err = p.communicate()

        for line in out.splitlines():
            if 'mplayer' in line:
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)

        self.playing = False
        print "Setting False"

    def find(self, search, index):

        song_list = []

        max = 11
        i = 1
        for song in self.client.search(search, type='Songs'):
            if i < max:
                song_list.append(repr(i) + "." + song.name + " by " + song.artist.name + " from " + song.album.name)
                i+=1

        if index:
            result = song_list[0]
        else:
            result = "\n".join(song_list)

        return result

    def play(self, search):

        self.playing = True;
        p = Process(target=self.actually_play, args=(search))
        p.start()

    def actually_play(self, search):

        popen_object = None

        song = self.client.search(search, type='Songs')[0]

        if song:
            print(song)

            FNULL = open(os.devnull, 'w')
            popen_object = subprocess.Popen(['mplayer', song.stream.url], shell=False, stdout=FNULL, stderr=subprocess.STDOUT, bufsize=1)

            while popen_object.poll() is None:
                time.sleep(1.0)

            self.playing = False;


if __name__ == "__main__":
    player = MusicPlayerObject()

    while True:
        time.sleep(1.0)
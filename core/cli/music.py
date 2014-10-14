import subprocess
import time
import os
import signal
from grooveshark import Client
from multiprocessing import Process

class MusicClient(object):

    """ Music client which wraps grooveshark api, allowing music to be streamed """
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

    def find(self, search, index=None,max_results=11):
        """ Return a song list or single song """
        song_results = self.client.search(search, type='Songs')[:max_results]

        if index:
            index = int(index)
            result_count = len(song_results)

            if index > -1 and index < result_count:
                result = song_results[index]
            else:
                result = []
        else:
            result = song_results

        return result

    def search(self, search):
        """ Returns formatted string list of song results from the search term provided """
        return "\n".join([repr(i) + "." + song.name + " by " + song.artist.name + " from " + song.album.name for index, song in enumerate(self.find(search), start=1)])

    def play(self, song):
        self.playing = True;
        p = Process(target=self.actually_play, args=(song))
        p.start()

    def actually_play(self, song):
        popen_object = None

        if song:
            print(song["title"])

            FNULL = open(os.devnull, 'w')
            popen_object = subprocess.Popen(['mplayer', song["url"]], shell=False, stdout=FNULL, stderr=subprocess.STDOUT, bufsize=1)

            while popen_object.poll() is None:
                time.sleep(1.0)

            self.playing = False

# if __name__ == "__main__":
#     player = MusicPlayerObject()

#     while True:
#         time.sleep(1.0)

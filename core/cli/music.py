import subprocess
import time
import os
import signal
from grooveshark import Client

class MusicClient(object):
    """ Music client which wraps grooveshark api, allowing music to be streamed
    """
    def __init__(self):
        self.client = Client()
        self.client.init()

    def stop(self):
        p = subprocess.Popen(["ps", "-A"], stdout=subprocess.PIPE)
        out, err = p.communicate()

        for line in out.splitlines():
            if "mplayer" in line:
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)

    def find(self, search, index=None, max_results=11):
        """ Find a song via grooveshark api search.

        Args:
            search (string): song title to search for.
            index (None, int): index value of song selection.
            max_results (int, optional): number of results to return from the search.

        Returns:
            result (tuple, grooveshark.classes.Song, list): song result list
        """
        song_results = list(self.client.search(search, type="Songs"))[:max_results]

        if isinstance(index, int):
            index = int(index)
            result_count = len(song_results)

            if -1 < index < result_count:
                result = song_results[index]
            else:
                result = []
        else:
            result = song_results

        return result

    def search(self, search):
        """ Returns formatted string list of song results from the search term provided

        Args:
            (string): Formatted list of song search results
        """
        return "\n".join([repr(index) + "." + song.name + " by " + song.artist.name + " from " + song.album.name for index, song in enumerate(self.find(search), start=1)])

    @staticmethod
    def change_volume(volume):
        if 10 < volume < 90:
            volume_percentage = volume+"%"
            subprocess.call(["amixer", "-D", "pulse", "sset", "Master", volume_percentage])

            return "Set Volume: " + volume_percentage

    def play(self, song):
        """ Play song subprocess callback, via mplayer

        Args:
            queued (int): flag for tracking whether a queued song is playing
            song (dict): song dictionary retrieved from queue list
        """
        popen_object = None

        print("Playing " + song["title"] + " by " + song["artist"])
        FNULL = open(os.devnull, "w")
        popen_object = subprocess.Popen(["mplayer", song["url"]], shell=False, stdout=FNULL, stderr=subprocess.STDOUT, bufsize=1)

        while popen_object.poll() is None:
            time.sleep(1.0)


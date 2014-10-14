from core.cli.music import MusicClient
from data.music import MusicDataAccess
import json

class MusicCommand(object):
    """ Manages the command processing for music """

    def __init__(self):
        self.music_client = MusicClient()
        self.music_data = MusicDataAccess()

    def stop(self):
        self.music_client.stop()

    def skip(self):
        self.music_client.stop()
        self.play_next()

        return "skipping the track"

    def list(self):
        return "\n".join([song["title"] for song in json.loads(self.music_data.get_queue())])

    def clear(self):
        self.music_data.clear_queue()

        return "music queue cleared!"

    def search(self, search):
        return self.music_client.search(search)

    def queue(self, song):
        song_info = song.split(",")

        if len(song_info) > 1:
            try:
                index = max(int(song_info[1]) -1, 0)
            except ValueError:
                index = 0
        else:
            index = 0

        search = song_info[0]

        song = self.music_client.find(search, index)

        if song:
            self.music_data.queue(song)
            return "song queued"
        else:
            return "unable to queue, song not found"

    def play_next(self):
        if not self.music_client.is_playing():
            song = self.music_data.play_next()
            if song:
                self.music_client.play(song)

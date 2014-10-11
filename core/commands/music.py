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
        return "\n".join([song["song_name"] for song in json.loads(self.music_data.get_queue())])

    def clear(self):
        self.music_data.clear_queue()

        return "music queue cleared!"

    def search(self, song):
        return self.music_client.find(search)

    def queue(self, song):
        song = self.music_client.find(search)
        self.music_data.queue(song)
        return "song queued"

    def play_next(self):
        if not self.music_client.is_playing():
            song = self.music_data.play_next()
            if song:
                self.music_client.play(song)
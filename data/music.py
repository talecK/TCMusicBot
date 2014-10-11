from datetime import datetime
from bson.json_util import dumps
from data.database import MongoConnection

class MusicDataAccess(object):

    """ DAO for music management """
    def __init__(self):
        self.storage = MongoConnection(db="tc_music", collection="song_queue")

    def queue(self, song):
        self.storage.use_collection('song_queue').insert({"song_name": song, "added_at": datetime.now()})
        return self

    def clear_queue():
        self.storage.use_collection('song_queue').remove({})
        return self

    def get_queue(self):
        queue_list = self.storage.use_collection('song_queue').find().sort([("added_at", 1)])
        return dumps(queue_list)

    def play_next(self):
        songs = self.storage.use_collection('song_queue').find().sort([("added_at", 1)])
        if songs.count() > 0:
            song = songs[0]["song_name"]
            self.remove_from_queue(song)
            self.add_to_played(song)
        else:
            song = ""

        return song

    def remove_from_queue(self, song):
        self.storage.use_collection('song_queue').remove({"song_name": song})
        return self

    def add_to_played(self, song):
        self.storage.use_collection('played_songs').insert({"song_name": song, "played_on": datetime.now()})
        return self

    def get_play_count(self, song):
        return self.storage.use_collection('played_songs').find({"song_name": song}).count()

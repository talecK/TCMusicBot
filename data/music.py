from datetime import datetime
from bson.json_util import dumps
from grooveshark.classes.song import Song
from data.database import MongoConnection

class MusicDataAccess(object):

    """ DAO for music management """
    def __init__(self):
        self.storage = MongoConnection(db="tc_music", collection="song_queue")

    def queue(self, song):
        self.storage.use_collection('song_queue').insert(extract_song_data(song).update({"added_at": datetime.now()})
        return self

    def clear_queue():
        self.storage.use_collection('song_queue').remove({})
        return self

    def get_queue(self):
        queue_list = self.storage.use_collection('song_queue').find().sort([("added_at", 1)])
        return queue_list

    def play_next(self):
        songs = self.storage.use_collection('song_queue').find().sort([("added_at", 1)])
        if songs.count() > 0:
            song = songs[0]
            self.remove_from_queue(song)
            self.add_to_played(song)
        else:
            song = None

        return song

    def find_in_queue(self, title=None, id=None):
        if title:
            return self.storage.use_collection('song_queue').find({"title": title})
        elif id:
            return self.storage.use_collection('song_queue').find({"_id": self.storage.get_key(id)})

        return None

    def remove_from_queue(self, title=None, id=None):
        if title:
            return self.storage.use_collection('song_queue').remove({"title": title})
        elif id:
            return self.storage.use_collection('song_queue').remove({"_id": self.storage.get_key(id)})

        return None

    def add_to_played(self, song):
        self.storage.use_collection('played_songs').insert(extract_song_data(song).update({"played_on": datetime.now()})
        return self

    def get_play_count(self, title):
        return self.storage.use_collection('played_songs').find({"title": title}).count()


def extract_song_data(song):
    """
        Extracts grooveshark song object into a dictionary
    """
    if isinstance(song, Song):
        return {
            'title': song.name,
            'artist': song.artist.name,
            'album': song.album.name,
            'track': song.track,
            'url': song.stream.url,
            'duration': song.duration
        }
    elif isinstance(song, dict):
        return {
            'title': song["title"],
            'artist': song["artist"],
            'album': song["album"],
            'track': song["track"],
            'url': song["url"],
            'duration': song["duration"]
        }

    return {}

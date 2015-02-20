from datetime import datetime
from bson.json_util import dumps
from grooveshark.classes.song import Song
from pafy.pafy import Pafy
from data.database import MongoConnection

class MusicDataAccess(object):

    """ DAO for music management
    """
    def __init__(self):
        self.storage = MongoConnection(db="tc_music", collection="song_queue")

    def queue(self, song, queued_by='User'):
        """ Adds a song object to the queue.

        Args:
            song (grooveshark.classes.Song): song returned from grooveshark api to be added into the music queue.

        Returns:
            self (MusicDataAccess)
        """
        queue_song = extract_song_data(song)

        if queue_song:
            if queued_by == 'Radio':
                queue_song.update({'queued_by_radio': True})
            queue_song.update({"queued_by": queued_by,"queued_at": datetime.now()})
            self.storage.use_collection("song_queue").insert(queue_song)

        return self

    def clear_queue(self):
        """ Clears the music queue.

        Returns:
            self (MusicDataAccess)
        """
        self.storage.use_collection("song_queue").remove({})
        return self

    def get_queue(self):
        """ Retrieves the current music queue.

        Returns:
            queue_list (pymongo.cursor.Cursor[grooveshark.classes.Song]): Returns a mongo cursor collection of songs.
        """
        return self.storage.use_collection("song_queue").find().sort([("queued_by_radio", 1),("queued_at", 1)])

    def get_queue_count(self):
        return self.storage.use_collection("song_queue").count()

    def play_next(self):
        """ Retrieves the next song to play from the queue.

        Returns:
            song (None, dict): Will return the song as a dictionary or None if nothing is found.
        """
        try:
            song = self.storage.use_collection("song_queue").find().sort([("queued_by", -1),("queued_at", 1)]).limit(1).next()

            self.remove_from_queue(id=song["_id"])
            self.add_to_played(song)
        except StopIteration as e:
            song = None

        return song

    def find_in_queue(self, title=None, id=None):
        """ Searches the queue for a song by title, or id.

        Args:
            title (None, string): song title to be searched, or None when searching by id.
            id (None, string): song object id to be searched, or None when searching by title.

        Returns:
            song (None, pymongo.cursor.Cursor[grooveshark.classes.Song]): Will return the cursor with the song result, or None if not found.
        """
        song = None

        if title:
            song = self.storage.use_collection("song_queue").find({"title": title})
        elif id:
            song = self.storage.use_collection("song_queue").find({"_id": self.storage.get_key(id)})

        return song

    def remove_from_queue(self, title=None, id=None, queued_by=None):
        """ Removes a song from the queue by song title, or id.

        Args:
            title (None, string): song title to be searched, or None when searching by id.
            id (None, string): song object id to be searched, or None when searching by title.

        Returns:
            result (boolean): Will return true when a song is removed, False otherwise.
        """
        result = False

        if title:
            result = self.storage.use_collection("song_queue").remove({"title": title})
        elif id:
            result = self.storage.use_collection("song_queue").remove({"_id": self.storage.get_key(id)})
        elif queued_by:
            result = self.storage.use_collection("song_queue").remove({"queued_by": queued_by})

        return result

    def add_to_played(self, song):
        """ Adds a song which was played from the queue to the played list.

        Args:
            song (dict): song returned from queue that has been played.

        Returns:
            self (MusicDataAccess)
        """
        if song:
            song.update({"played_on": datetime.now()})
            self.storage.use_collection("played_songs").insert(song)

        return self

    def get_play_count(self, title):
        """ Retrieve the playcount for a song title.

        Args:
            title (string): song title to get playcount for.

        Returns:
            (int): the number of plays a song title has.
        """
        return self.storage.use_collection("played_songs").find({"title": title}).count()

    def get_last_played(self):
        """ Retrieve the last played song

        Returns:
            (None, grooveshark.classes.Song)
        """
        try:
            song = self.storage.use_collection("played_songs").find().sort([("played_on", -1)]).limit(1).next()
        except StopIteration as e:
            song = None

            return song

def extract_song_data(song):
    """ Extracts grooveshark song object into a dictionary.

    Args:
        song (grooveshark.classes.Song, dict): song to extract information from

    Returns:
        (dict): the formatted dictionary of song data.
    """
    if isinstance(song, Song):
        return {
            "title": song.name,
            "artist": song.artist.name,
            "album": song.album.name,
            "track": song.track,
            "url": song.stream.url,
            "duration": song.duration
        }
    elif isinstance(song, Pafy):
        return {
            "title": song.title,
            "artist": 'Youtube',
            "album": 'Youtube',
            "track": 'Youtube',
            "url": song.getbestaudio().url,
            "duration": song.duration
        }
    elif isinstance(song, dict):
        return {
            "title": song["title"],
            "artist": song["artist"],
            "album": song["album"],
            "track": song["track"],
            "url": song["url"],
            "duration": song["duration"],
            "queued_by": song["queued_by"]
        }

    return {}

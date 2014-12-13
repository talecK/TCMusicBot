from datetime import datetime
from bson.json_util import dumps
from data.database import MongoConnection
from data.music import extract_song_data
class ServerDataAccess(object):

    """ DAO for server stat management
    """
    def __init__(self):
        self.storage = MongoConnection(db='tc_music', collection='server_stats')

    def get_volume():
        pass

    def set_volume(volume):
        pass

    def get_currently_playing():
        stats = self.storage.use_collection('server_stats').find_one()

        if stats['status'] == 'playing':
            return stats['currently_playing']

        return {}

    def set_currently_playing(song):

        if isinstance(song, Song):
            self.storage.use_collection('server_stats').find_one().update({'currently_playing': extract_song_data(song)})

    def get_total_songs_played():
        pass

    def get_server_status():
        pass

    def set_server_status(status):
        pass

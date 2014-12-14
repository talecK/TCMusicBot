from datetime import datetime
from bson.json_util import dumps
from data.database import MongoConnection
from data.music import extract_song_data

class ServerDataAccess(object):

    """ DAO for server stat management
    """
    def __init__(self):
        self.storage = MongoConnection(db='tc_music', collection='server_stats')

    def create_server_statistics(self):
        # Remove any previous server stats from previous sessions
        self.storage.use_collection('server_stats').remove()

        # Rebuild the server stats entry
        self.storage.use_collection('server_stats').insert({
            'currently_playing': {},
            'status': 'polling',
            'volume': '50'
        })

    def get_volume(self):
        return self.storage.use_collection('server_stats').find_one({}, {'volume': true})

    def set_volume(self, volume):
        return self.storage.use_collection('server_stats').update_one({},{'volume': volume})

    def get_currently_playing(self):
        result = {}
        stats = self.storage.use_collection('server_stats').find_one()

        if stats['status'] == 'playing':
            result = stats['currently_playing']

        return result

    def set_currently_playing(self, song=None):

        if isinstance(song, Song):
            return self.storage.use_collection('server_stats').update_one({}, {'currently_playing': extract_song_data(song), 'status': 'playing'})
        else:
            return self.storage.use_collection('server_stats').update_one({}, {'currently_playing': {}, 'status': 'polling'})

        return False

    def get_total_songs_played(self):
        return self.storage.use_collection('server_stats').find_one({}, {'total_songs_played': true})

    def set_total_songs_played(self, total_songs):
        return self.storage.use_collection('server_stats').update_one({},{'total_songs_played': total_songs})

    def get_server_status(self):
        return self.storage.use_collection('server_stats').find_one({}, {'status': true})

    def set_server_status(self, status):
        return self.storage.use_collection('server_stats').update_one({}, {'status': status})

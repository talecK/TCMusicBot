from datetime import datetime
from bson.json_util import dumps
from data.database import MongoConnection
from grooveshark import Song
from data.music import extract_song_data

class ServerDataAccess(object):

    """ DAO for server stat management
    """
    def __init__(self):
        self.storage = MongoConnection(db='tc_music', collection='server_stats')
        self.stats_id = None

    def create_server_statistics(self):
        # Remove any previous server stats from previous sessions
        self.storage.use_collection('server_stats').remove()

        # Rebuild the server stats entry
        stats_id = self.storage.use_collection('server_stats').insert({
            'currently_playing': {},
            'status': 'polling',
            'volume': '50'
        })

        self.stats_id = self.storage.get_key(stats_id)

    def get_volume(self):
        return self.storage.use_collection('server_stats').find_one({'_id': self.stats_id}, {'volume': True})

    def set_volume(self, volume):

        return self.storage.use_collection('server_stats').update({'_id': self.stats_id},{'volume': volume})

    def get_currently_playing(self):
        result = {}
        stats = self.storage.use_collection('server_stats').find_one({'_id': self.stats_id})

        if stats['status'] == 'playing':
            result = stats['currently_playing']

        return result

    def set_currently_playing(self, song=None):

        if isinstance(song, Song):
            return self.storage.use_collection('server_stats').update({'_id': self.stats_id}, {'currently_playing': extract_song_data(song), 'status': 'playing'})
        else:
            return self.storage.use_collection('server_stats').update({'_id': self.stats_id}, {'currently_playing': {}, 'status': 'polling', 'volume': '50'})

        return False

    def get_total_songs_played(self):
        return self.storage.use_collection('server_stats').find_one({'_id': self.stats_id}, {'total_songs_played': True})

    def set_total_songs_played(self, total_songs):
        return self.storage.use_collection('server_stats').update({'_id': self.stats_id},{'total_songs_played': total_songs})

    def get_server_status(self):
        return self.storage.use_collection('server_stats').find_one({'_id': self.stats_id}, {'status': True})

    def set_server_status(self, status):
        return self.storage.use_collection('server_stats').update({'_id': self.stats_id}, {'status': status})

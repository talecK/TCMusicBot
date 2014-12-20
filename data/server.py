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

    def create_server_statistics(self):
        # Rebuild the server stats entry
        stats_id = self.set_currently_playing()

        print "Setting server id " +  str(stats_id)

    def get_radio(arg):
        return self.storage.use_collection('server_stats').find_one({'radio': True})

    def set_radio(self, genre):
        return self.storage.use_collection('server_stats').update({}, {'$set':{'radio': genre}}, upsert=False)

    def get_volume(self):
        return self.storage.use_collection('server_stats').find_one({'volume': True})

    def set_volume(self, volume):
        return self.storage.use_collection('server_stats').update({}, {'$set':{'volume': volume}},upsert=False)

    def get_currently_playing(self):
        result = {}
        stats = self.storage.use_collection('server_stats').find_one()

        if stats['status'] == 'playing':
            result = stats['currently_playing']

        return result

    def set_currently_playing(self, song=None):

        if isinstance(song, dict):
            print "Setting server status to playing"
            return self.storage.use_collection('server_stats').update({}, {'$set':{'currently_playing': extract_song_data(song), 'status': 'playing'}},upsert=False)
        else:
            print "Server polling..."
            return self.storage.use_collection('server_stats').update({}, {'$set':{'currently_playing': {}, 'status': 'polling', 'volume': '50'}},upsert=True)

    def get_total_songs_played(self):
        return self.storage.use_collection('server_stats').find_one({'total_songs_played': True})

    def set_total_songs_played(self, total_songs):
        return self.storage.use_collection('server_stats').update({}, {'$set':{'total_songs_played': total_songs}},upsert=False)

    def increment_total_songs_played(self):
        return self.storage.use_collection('server_stats').update({}, {'$inc':{'total_songs_played': 1}},upsert=False)

    def get_server_status(self):
        return self.storage.use_collection('server_stats').find_one({'status': True})

    def set_server_status(self, status):
        return self.storage.use_collection('server_stats').update({}, {'$set':{'status': status}},upsert=False)

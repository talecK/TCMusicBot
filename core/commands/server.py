from data.music import MusicDataAccess, extract_song_data
from data.server import ServerDataAccess
from grooveshark import Song
import numbers, re

class ServerCommand(object):

    """ Manages the server related tasks
    """
    def __init__(self):
        self.server_data = ServerDataAccess()

    """ Initialize the server statistics document
    """
    def stats_init(self):
        self.server_data.create_server_statistics()

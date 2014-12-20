from core.cli.server import change_volume
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

    def change_volume(self, volume=None):
        numeric_volume = re.sub("[^0-9]", "", volume)

        if volume and numeric_volume:
            volume_delta = int(numeric_volume)
            resp = change_volume(volume_delta)

            # Set the server volume in the server stats document for easier retrieval
            if "Set Volume:" in resp:
                self.server_data.set_volume(volume_delta)
        else:
            resp = self.server_data.get_volume()

        return resp

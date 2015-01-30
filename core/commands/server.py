from core.cli.server import change_volume
from data.server import ServerDataAccess
import re
import json


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
        if volume:

            if self.is_number(volume):
                numeric_volume = re.sub("[^0-9]", "", volume)
            else:
                volume_delta = self.count_volume_delta(volume)
                numeric_volume = self.server_data.get_volume()['volume'] + volume_delta

            if numeric_volume:
                new_volume = int(numeric_volume)
                resp = change_volume(new_volume)

                # Set the server volume in the server stats document for easier retrieval
                if "Set Volume:" in resp:
                    self.server_data.set_volume(new_volume)
        else:
            resp = "Volume is {0}".format(self.server_data.get_volume()['volume'])

        return resp

    @staticmethod
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def count_volume_delta(strVol):
        delta = 0
        for ch in strVol:
            if ch == '+':
                delta += 3
            elif ch == '-':
                delta -= 3

        return delta
from core.cli.music import MusicClient
from data.music import MusicDataAccess, extract_song_data
from data.server import ServerDataAccess
from grooveshark import Song, Radio
from pafy.pafy import Pafy

class MusicCommand(object):

    """ Manages the command processing for music
    """
    def __init__(self):
        self.music_client = MusicClient()
        self.music_data = MusicDataAccess()
        self.server_data = ServerDataAccess()
        self.command_user = ''

    @staticmethod
    def format_song(song):
        return song["title"] + " by " + song["artist"] + " from " + song["album"] + " queued by " + song["queued_by"]

    def stop(self):
        """ Stops the current playing song
        """
        
        self.skip()
        self.clear()

        return "I dropped the beat."

    def skip(self):
        """ Skips the current playing song

        Returns:
            (string): response message
        """
        self.server_data.set_server_status('polling')
        self.music_client.stop()

        return "I liked that song."

    def list(self):
        """ Lists the songs which are currently queued to play

        Returns:
            (string): Formatted result of queued song list.
        """
        # list the last played song only if it is currently playing.
        result = self.currently_playing()

        result += "\n".join([self.format_song(song) for song in self.music_data.get_queue()])

        return result

    def currently_playing(self):
        song = self.is_playing()

        if not song:
            return ""
        else:
            return "**Currently Playing** " + self.format_song(extract_song_data(song)) + "\n"

    def clear(self):
        """ Clears all songs out of the queue
        """
        self.music_data.clear_queue()

        return "music queue cleared!"

    def radio(self, genre=None, prefetch=1):
        if not genre:
            genre = Radio.GENRE_METAL  # Metal default, because its the best |M|

        music_collection = []
        try:
            for index, song in enumerate(self.music_client.radio(genre), start=1):
                music_collection.append(extract_song_data(song))
                if index == prefetch:
                    break
        except Exception as e:
            music_collection = []

        return music_collection

    def search(self, search):
        """ Searches and returns results for a song title.

        Args:
            search (string): the song title to search for.

        Return:
            (string): Formatted result of search result list.
        """
        return self.music_client.search(search)

    def queue_immediate(self, songs):
        for song in songs:
            self.music_data.queue(song)

    def queue(self, title):
        """ Queues a song up by the title, with an optional index in the case of multiple results for a title.

        Args:
            title (string): {song_title}, (optional) {index}

        Returns:
            response_msg (string): response status message of whether song was queued.
        """
        song_info = title.split(",")

        if len(song_info) > 1:
            try:
                index = max(int(song_info[1].strip()) - 1, 0)
            except ValueError:
                index = 0
        else:
            index = 0

        search = song_info[0].strip()

        song = self.music_client.find(search=search, index=index)

        if isinstance(song, Song):
            self.music_data.queue(song, queued_by=self.command_user)
            response_msg = "Queued: " + self.format_song(extract_song_data(song))
        else:
            response_msg = "Unable to queue, song not found"

        return response_msg

    def queue_youtube(self, url):
        """ Queues a song up by the youtube url

        Args:
            title (string): {url}

        Returns:
            response_msg (string): response status message of whether song was queued.
        """

        song = self.music_client.youtube(url)
        
        if isinstance(song, Pafy):
            self.music_data.queue(song, queued_by=self.command_user)
            response_msg = "Queued: " + song.title
        else:
            response_msg = "Unable to queue, youtube audio not found"

        return response_msg

    @staticmethod
    def list_radio_genres():

        response_msg = "Radio Genres"
        response_msg += "============"
        response_msg += "\n".join([genre.split('_')[1] for genre in dir(Radio) if genre.startswith('GENRE_')])

        return response_msg

    def enable_radio(self, genre):

        try:
            genre_found = getattr(Radio, "GENRE_{0}".format(genre.upper()))

            if genre_found:
                # Enable radio with genre
                self.server_data.set_radio(genre_found)

                response_msg = "Enabled {0} radio".format(genre)
            else:
                response_msg = "Unable to find a radio station for '{0}'".format(genre)

        except Exception as e:
            response_msg = "Something went wrong. {0}".format(str(e))

        return response_msg

    def disable_radio(self):
        # Disable radio
        self.server_data.set_radio('')

        # Remove any songs queued by radio
        self.music_data.remove_from_queue(queued_by='Radio')

        return "Disabled radio mode."

    def queue_radio(self):
        # Check if radio mode has been enabled
        radio_genre = self.server_data.get_radio()

        # When radio mode is enabled, attempt to prefetch songs to mix into the queue.
        # Only fetch radio songs if there is less than 2 songs in the queue.
        # This is to allow for some buffer room.
        if radio_genre and radio_genre['radio'] and self.music_data.get_queue_count() < 2:
            songs = self.radio(radio_genre['radio'], prefetch=1)
            songs[0]["queued_by"] = 'Radio'
            if songs:
                print "Queued " + songs[0]["title"] + " by " + songs[0]["artist"] + " from  " + songs[0]["album"]
                self.music_data.queue(songs[0], queued_by='Radio')

    def play_next(self):
        """ Plays the next song in the queue if one exists. If radio mode is enabled,
        will attempt to retrieve a song from the radio genre currently playing.
        """
        song = self.music_data.play_next()

        if song:
            # Add the playing song in the server stats
            self.set_playing(song)

            # Creates a semaphore to stop the process from trying to play a song while another is currently playing,
            # without blocking the process
            self.server_data.set_server_status("playing")
            self.music_client.play(song)

            # Were finished playing the song, remove the semaphore to allow the next song to queue up
            self.server_data.set_server_status("polling")

            # If queue is empty, set server status to polling
            self.set_playing(None)

    def set_playing(self, song=None):
        self.server_data.set_currently_playing(song)

    def is_playing(self):
        return self.server_data.get_currently_playing()
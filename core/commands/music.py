from core.cli.music import MusicClient
from data.music import MusicDataAccess, extract_song_data
from grooveshark import Song
import numbers, re

class MusicCommand(object):

    """ Manages the command processing for music
    """
    def __init__(self):
        self.music_client = MusicClient()
        self.music_data = MusicDataAccess()
        self.is_playing = False

    @staticmethod
    def format_song(song):
        return song["title"] + " by " + song["artist"] + " from " + song["album"]

    def change_volume(self, volume):
        volume_delta = re.sub("[^0-9]", "", volume)

        if volume_delta:
            return self.music_client.change_volume(int(volume_delta)

    def stop(self):
        """ Stops the current playing song
        """
        self.music_client.stop()
        self.set_playing(False)

        return "song stopped"

    def skip(self):
        """ Skips the current playing song

        Returns:
            (string): response message
        """
        self.music_client.stop()
        self.play_next()

        return "skipping the track"

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
        song = ""
        if self.is_playing:
            last_played = self.music_data.get_last_played()

            if last_played:
                song = "**Currently Playing** " + self.format_song(extract_song_data(last_played))

        return song

    def clear(self):
        """ Clears all songs out of the queue
        """
        self.music_data.clear_queue()

        return "music queue cleared!"

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
            self.music_data.queue(song)
            response_msg = "Queued: " + self.format_song(extract_song_data(song))
        else:
            response_msg = "Unable to queue, song not found"

        return response_msg

    def play_next(self, queue):
        """ Plays the next song in the queue if one exists.
        """
        song = self.music_data.play_next()
        if song:

            # Creates a semaphore to stop the process from trying to play a song while another is currently playing,
            # without blocking the process
            queue.append("playing")
            self.music_client.play(song)

            # Were finished playing the song, remove the semaphore to allow the next song to queue up
            del queue[0]

    def set_playing(self, playing):
        self.is_playing = playing
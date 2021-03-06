from core.bots.base import SkypeBot
import time
from core.commands.music import MusicCommand
from core.commands.server import ServerCommand
import multiprocessing

class MusicBot(SkypeBot):

    """ Bot for playing music from skype chat.

    ChatCommand format: {delimeter}{owner} {command} {args}
    """
    def __init__(self):
        super(MusicBot, self).__init__(name="Skype MusicBot")
        self.music_command = MusicCommand()
        self.server_command = ServerCommand()

    def register_command_owner(self):
        """ Register chat command owner name
        """
        self.command_handler.register_owner("musicbot")

    def register_command_delimiter(self):
        """ Register chat command delimiter
        """
        self.command_handler.register_delimiter("@")

    def register_commands(self):
        """ Register the list of commands and callback functions
        """
        self.command_handler.register(name="help", obj=self, func="help", description="this message")
        self.command_handler.register(name="stop", obj=self.music_command, func="stop", description="stop the music")
        self.command_handler.register(name="skip", obj=self.music_command, func="skip", description="skip the current track")
        self.command_handler.register(name="list", obj=self.music_command, func="list", description="list the current queue")
        self.command_handler.register(name="playing", obj=self.music_command, func="currently_playing", description="the currently playing song", aliases=["blame"])
        self.command_handler.register(name="volume", obj=self.server_command, func="change_volume", description="set the system volume", accepts_args=True, aliases=["vol", "v"])
        self.command_handler.register(name="clear", obj=self.music_command, func="clear", description="clear the current queue")
        self.command_handler.register(name="search", obj=self.music_command, func="search", description="search {search term}, {optional index}", accepts_args=True, aliases=["s"])
        self.command_handler.register(name="queue", obj=self.music_command, func="queue", description="queue {search term}, {optional index}", accepts_args=True, aliases=["q"])
        self.command_handler.register(name="queue_youtube", obj=self.music_command, func="queue_youtube", description="queue_youtube {youtube_url}", accepts_args=True, aliases=["qy"])
        self.command_handler.register(name="queue_file", obj=self.music_command, func="queue_file", description="queue_file {Url to an audio file}", accepts_args=True, aliases=["qf"])
        self.command_handler.register(name="radio_on", obj=self.music_command, func="enable_radio", description="radio_on {genre} : enables radio genre to feed the song queue", accepts_args=True)
        self.command_handler.register(name="radio_off", obj=self.music_command, func="disable_radio", description="disables any active radio and removes related songs from current queue")
        self.command_handler.register(name="radio_list", obj=self.music_command, func="list_radio_genres", description="list available radio genres")
        self.command_handler.register(name="undo", obj=self.music_command, func="undo", description="remove last song in queue", aliases=["u"])

    def help(self):
        """ Command Callback function

        Returns:
            text (string): Formatted list of the registered commands for this bot.
        """
        text = "TC Music Bot, supported commands\n"
        text += "======================\n"
        text += "\n".join(self.command_handler.registered_commands())

        return text

    def bootstrap(self):
        super(MusicBot, self).bootstrap()
        self.server_command.stats_init()

    def run(self):
        """ Bot main run loop
        """
        while True:
            time.sleep(1.0)
            if self.server_command.get_server_status()["status"] == 'polling':
                p = multiprocessing.Process(target=self.music_command.play_next)
                p.start()

            self.music_command.queue_radio()

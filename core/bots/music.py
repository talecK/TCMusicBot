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
        self.command_handler.register(name="playing", obj=self.music_command, func="currently_playing", description="the currently playing song")
        self.command_handler.register(name="volume", obj=self.music_command, func="change_volume", description="set the system volume", accepts_args=True, aliases=["vol", "v"])
        self.command_handler.register(name="clear", obj=self.music_command, func="clear", description="clear the current queue")
        self.command_handler.register(name="search", obj=self.music_command, func="search", description="search {search term}, {optional index}", accepts_args=True, aliases=["s"])
        self.command_handler.register(name="queue", obj=self.music_command, func="queue", description="queue {search term}, {optional index}", accepts_args=True, aliases=["q"])

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
            if len(self.queue) == 0:
                p = multiprocessing.Process(target=self.music_command.play_next, args=(self.queue,))
                p.start()

            # Set the currently playing flag based on whether there is a song currently playing.
            if self.queue:
                self.music_command.set_playing(True)
            else:
                self.music_command.set_playing(False)

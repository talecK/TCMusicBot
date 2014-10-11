from core.bots.base import SkypeBot
from core.commands.music import MusicCommand

class MusicBot(SkypeBot):

    """ Bot for playing music from skype chat.
    """
    def __init__(self):
        super(MusicBot, self).__init__(name="Skype MusicBot")

    def register_command_owner(self):
        self.command_handler.register_owner("musicbot")

    def register_command_delimiter(self):
        self.command_handler.register_delimiter("@")

    def register_commands(self):
        music_command = MusicCommand()

        commands = [
            {
                "help" : { "obj": self, "func": "help", "accepts_args": false, "description": "this message"},
                "stop" : { "obj": music_command, "func": "stop", "accepts_args": false, "description": "stop the music"},
                "skip" : { "obj": music_command, "func": "skip", "accepts_args": false, "description": "skip the current track"},
                "list" : { "obj": music_command, "func": "list", "accepts_args": false, "description": "list the current queue"},
                "clear" : { "obj": music_command, "func": "clear", "accepts_args": false, "description": "clear the current queue"},
                "search" : { "obj": music_command, "func": "search", "accepts_args": true, "description": "search {search term}, {optional index}"},
                "queue" : { "obj": music_command, "func": "queue", "accepts_args": true, "description": "queue {search term}, {optional index}"}
            }
        ]

        self.command_handler.register(commands)

    def help(self):
        text =  "TC Music Bot, supported commands\n"
        text +="======================\n"
        text += "\n".join([name + ' - ' + cmd["description"] for name, cmd in self.command_handler.registered_commands()])

        return text

    def run(self):
        self.music_command.play_next()
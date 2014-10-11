from abc import ABCMeta, abstractmethod
from Skype4Py import cmsReceived, Skype
from core.handler import CommandHandler

class SkypeBot(object):
    __metaclass__ = ABCMeta

    """
        Base Interface Class to define the interactions of a SkypeBot

        :param command_handler [core.handler.CommandHandler]
        :param name [string]
    """
    def __init__(self, name="Skype Bot"):
        self.command_handler = CommandHandler()
        self.skype = Skype(Events=self)
        self.skype.FriendlyName = name
        self.skype.Attach()

    def MessageStatus(self, msg, status):
        if status == cmsReceived:
            msg.MarkAsSeen()
            reply_with = self.command_handler.handle(msg, status)

            if reply_with:
                self.__reply(msg, reply_with)

    def __reply(msg_client, msg):
        """ Send message to chat via Skype Msg Module """
        msg_client.Chat.SendMessage(msg)

    def bootstrap(self):
        """ Bootstraps the Bot config to run """
        self.register_command_delimiter()
        self.register_command_owner()
        self.register_commands()

    @abstractmethod
    def run(self):
        """ Method which will facilitate running the Bot """
        pass

    @abstractmethod
    def register_command_delimiter(self):
        """ Register the delimiter in which signifies a command is being sent """
        pass

    @abstractmethod
    def register_command_owner(self):
        """ Register the current bot name which will respond to commands in skype """
        pass

    @abstractmethod
    def register_commands(self):
        """ Register the bot commands """
        pass

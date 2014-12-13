from abc import ABCMeta, abstractmethod
# from Skype4Py import cmsReceived, Skype
from core.handler import CommandHandler
import multiprocessing

class SkypeBot(object):
    __metaclass__ = ABCMeta

    """ Abstract Base Class to define the interactions of a SkypeBot

    Args:
        name (string, optional): Name given to the SkypeBot
    """
    def __init__(self, name="Skype Bot"):
        self.command_handler = CommandHandler()
        self.skype = Skype(Events=self)
        self.skype.FriendlyName = name
        self.mgr = multiprocessing.Manager()
        self.queue = self.mgr.list()

    def MessageStatus(self, msg, status):
        """ Event handler for sending messages

        Args:
            msg (Skype4Py.SmsMessage): Skype Message
            status (int): status code
        """
        if status == cmsReceived:
            msg.MarkAsSeen()
            reply_with = self.command_handler.handle(msg, status)

            if reply_with:
                self.__reply(msg, reply_with)

    def __reply(self, msg_client, msg):
        """ [Internal] Send message to chat via Skype Msg Module

        Args:
            msg_client (Skype4Py.Chat): Skype Chat client instance
            msg (Skype4Py.SmsMessage): Skype Message
        """
        msg_client.Chat.SendMessage(msg)

    def bootstrap(self):
        """ Bootstraps the Bot config to run and attach to the skype client
        """
        self.register_command_delimiter()
        self.register_command_owner()
        self.register_commands()
        self.skype.Attach()

    @abstractmethod
    def run(self):
        """ Method which will facilitate running the Bot.
        """
        pass

    @abstractmethod
    def register_command_delimiter(self):
        """ Register the delimiter in which signifies a command is being sent.
        """
        pass

    @abstractmethod
    def register_command_owner(self):
        """ Register the current bot name which will respond to commands in skype.
        """
        pass

    @abstractmethod
    def register_commands(self):
        """ Register the bot commands.
        """
        pass

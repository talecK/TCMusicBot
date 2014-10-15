import re

class CommandHandler(object):
    """Handler to process incoming Skype messages to built-in commands
    """
    def __init__(self):
        self.commands = {}
        self.command_owner = ""
        self.command_delimiter = ""

    def register_owner(self, name):
        self.command_owner = name

    def register_delimiter(self, delim):
        self.command_delimiter = delim

    def register(self, commands):
        """ Registers commands which are to be managed

        Args:
            commands (list, dict): the dictionary or list of dictionaries of command data to add
                Example format:
                    {
                        ":cmd_name" :
                        {
                            "obj": "MyObject",
                            "func": "some_processing_function",
                            "accepts_args": true
                        }
                    }
        """
        if commands:
            if not isinstance(commands,list):
                commands = [commands]

            for command in commands:
                self.commands.update(command)

    def handle(self, msg, status):
        """ Performs the check on whether we have the means to handle the function, and passes the information
        onto the class method to process the request.

        Args:
            msg
            status

        Returns:
            (None, any): will return any values which are returned via the callback methods, or None.
        """
        cmd, args = self.extract_command_args(msg)

        if cmd in self.commands:
            cmd = self.commands[cmd]

            if cmd['accepts_args']:
                return_val = getattr(cmd['obj'], cmd['func'])(args)
            else:
                return_val = getattr(cmd['obj'], cmd['func'])

            if return_val is not None:
                return return_val

    def registered_commands(self):
        """ Get the list of commands registered with this handler.

        Returns:
            (list): formatted list of the commands registered to this command handler.
        """
        return [ self.command_delimiter + self.command_owner + ' ' + cmd + ' - ' + self.commands[cmd]["description"] for cmd in self.commands.keys()]

    def extract_command_args(self,msg):
        """ Extract the command and any arguments from the message passed in.

        Args:
            msg (Skype4Py.SmsMessage): skype message to extract information from

        Returns:
            (tuple): all match groups for the regex format to retrieve the command and any arguments
        """
        match_format = re.compile('{0}{1} (\w+) (.*)'.format(re.escape(self.command_delimiter), re.escape(self.command_owner)), re.IGNORECASE)
        matches = re.match(match_format, msg.Body)

        return matches.groups()

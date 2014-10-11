class CommandHandler(object):
    """Handler to process incoming messages to built-in commands
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
        """ :param commands - single or collection of dicts for registering commands

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
        """Performs the check on whether we have the means to handle the function, and passes the information
            onto the class method to process the request."""

        cmd, args = self.__extract_command_args(msg)

        if cmd in self.commands:
            cmd = self.commands[cmd]

            if cmd['accepts_args']:
                getattr(cmd['obj'], cmd['func'])(*args)
            else:
                getattr(cmd['obj'], cmd['func'])

    def registered_commands(self):
        """ Get the list of commands registered with this handler. """
        return [ self.command_delimiter + self.command_owner + ' ' + cmd for cmd in self.commands.keys()]

    def __extract_command_args(msg):
        """ Extract the command and any arguments from the message passed in. """
        match_format = re.compile('{0}{1} (\w+) (.*)'.format(re.escape(self.command_delimiter), re.escape(self.command_owner)))
        matches = re.match(match_format, msg.Body, re.IGNORECASE)

        return matches.groups()

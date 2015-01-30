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

    def handle(self, msg, status, user='User'):
        """ Performs the check on whether we have the means to handle the function, and passes the information
        onto the class method to process the request.

        Args:
            msg
            status

        Returns:
            (None, any): will return any values which are returned via the callback methods, or None.
        """
        cmd, args = self.extract_command_args(msg)

        return self.fire_command(cmd, args, user)

    def register(self, name, obj, func, description="", accepts_args=False, aliases=[]):
        """ Registers commands which are to be managed

        Args:
            name                 (string): The name of the command
            obj                     (Object): The object that will perform the handling of the command
            func                   (Object): The function that will be called on the object
            description        (string): Command's desciption text
            accepts_args    (boolean): Dictates whether or not the command will accept incoming arguments
            aliases              (list): Any aliases the command will respond to
        """
        self.commands.update({name: {"obj": obj, "func": func, "description": description, "accepts_args": accepts_args, "aliases": aliases}})

    def registered_commands(self):
        """ Get the list of commands registered with this handler.

        Returns:
            (list): formatted list of the commands registered to this command handler.
        """
        return [self.command_delimiter + self.command_owner + " " + cmd + "[" + ",".join(self.commands[cmd]["aliases"]) + "] - " + self.commands[cmd]["description"] for cmd in self.commands.keys()]

    def extract_command_args(self, msg):
        """ Extract the command and any arguments from the message passed in.

        Args:
            msg (Skype4Py.SmsMessage): skype message to extract information from

        Returns:
            (tuple): all match groups for the regex format to retrieve the command and any arguments
        """
        match_format = re.compile("{0}{1} (\w+) ?(.*)".format(re.escape(self.command_delimiter), re.escape(self.command_owner)), re.IGNORECASE)
        matches = re.match(match_format, msg.Body)

        if matches:
            return matches.groups()

        return None, None

    def fire_command(self, cmd, args, user):
        if not cmd in self.commands:
            cmd = self.find_alias(cmd)

        if cmd and cmd in self.commands:
            cmd = self.commands[cmd]

            cmd_handler = cmd["obj"]
            cmd_handler.command_user = user
            cmd_function = cmd["func"]

            if cmd["accepts_args"]:
                return_val = cmd_handler.__getattribute__(cmd_function)(args)
            else:
                return_val = cmd_handler.__getattribute__(cmd_function)()

            return return_val

    def find_alias(self, cmd):
        for command in self.commands:
            if "aliases" in self.commands[command] and cmd in self.commands[command]["aliases"]:
                return command

        return None

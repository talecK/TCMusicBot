import unittest
from mock import Mock
from core.handler import CommandHandler


class CommandHandlerTest(unittest.TestCase):

    def setUp(self):

        self.command = {"test": {"obj": self, "func": "sampleFunc", "accepts_args": True, "description": "this is a test"} }

        self.commands = [
            {
                "test": {"obj": self, "func": "sampleFunc", "accepts_args": True, "description": "this is a test"}
            }
        ]

        self.aliases = {
            "test": ["t"]
        }

        self.cmd_handler = CommandHandler()

    def tearDown(self):
        self.cmd_handler = None

    def testHandlerRegistersCommandsWithListOfCommands(self):
        self.cmd_handler.register_owner('testbot')
        self.cmd_handler.register_delimiter('!')
        self.cmd_handler.register(self.commands)

        registered_command_list = self.cmd_handler.registered_commands()
        expected_command_list = ['!testbot test - this is a test']
        self.assertEqual(registered_command_list, expected_command_list)

    def testHandlerRegistersCommandsWithSingleCommand(self):
        self.cmd_handler.register_owner('testbot')
        self.cmd_handler.register_delimiter('!')
        self.cmd_handler.register(self.command)

        registered_command_list = self.cmd_handler.registered_commands()
        expected_command_list = ['!testbot test - this is a test']
        self.assertEqual(registered_command_list, expected_command_list)

    def testHandlerCanAcceptCommandAliases(self):
        self.cmd_handler.register_owner('testbot')
        self.cmd_handler.register_delimiter('!')
        self.cmd_handler.register(self.command)
        self.cmd_handler.register_aliases(self.aliases)

        msg = Mock(Body="!testbot t this is a test")
        function_return = self.cmd_handler.handle(msg, 200)

        self.assertEqual(function_return, "this is a test")

    def testHandlerCanParseMessages(self):
        self.cmd_handler.register_owner('testbot')
        self.cmd_handler.register_delimiter('!')
        self.cmd_handler.register(self.command)

        msg = Mock(Body="!testbot test this is a test")
        cmd, argvals = self.cmd_handler.extract_command_args(msg)

        self.assertEqual(cmd, "test")
        self.assertEqual(argvals, "this is a test")

    def testHandlerCallsRegisteredFunctions(self):
        self.cmd_handler.register_owner('testbot')
        self.cmd_handler.register_delimiter('!')
        self.cmd_handler.register(self.command)

        msg = Mock(Body="!testbot test this is a test")
        function_return = self.cmd_handler.handle(msg, 200)

        self.assertEqual(function_return, "this is a test")

    # Functions for testing commands callback functionality
    def sampleFunc(self, args):
        return args

if __name__ == "__main__":
    unittest.main()

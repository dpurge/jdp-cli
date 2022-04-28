from collections import OrderedDict
from importlib.metadata import entry_points

from knack import CLICommandsLoader

class JdpCommandsLoader(CLICommandsLoader):
    
    def __init__(self, cli_ctx=None):
        super(JdpCommandsLoader, self).__init__(cli_ctx = cli_ctx)

        self._command_loaders = []
        self._argument_loaders = []

        self.commands = entry_points(group = 'jdp_cli.commands')
        for cmd in self.commands:
            module = cmd.load()
            self._command_loaders.append(module.load_commands)
            self._argument_loaders.append(module.load_arguments)

    def load_command_table(self, args):

        for loader in self._command_loaders:
            loader(self)

        return OrderedDict(self.command_table)

    def load_arguments(self, command):

        for loader in self._argument_loaders:
            loader(self)

        super(JdpCommandsLoader, self).load_arguments(command)
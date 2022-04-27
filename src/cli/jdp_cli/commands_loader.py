from collections import OrderedDict

from knack import ArgumentsContext, CLICommandsLoader
from knack.commands import CommandGroup

class JdpCommandsLoader(CLICommandsLoader):
    def load_command_table(self, args):
        with CommandGroup(self, 'abc', '__main__#{}') as g:
            g.command('str', 'abc_str')
        return OrderedDict(self.command_table)

    def load_arguments(self, command):
        with ArgumentsContext(self, 'abc str') as ac:
            ac.argument('length', type=int)
        super(JdpCommandsLoader, self).load_arguments(command)
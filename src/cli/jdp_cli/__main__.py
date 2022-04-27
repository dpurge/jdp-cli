import sys
from knack import CLI
from .commands_loader import JdpCommandsLoader


def abc_str(length=3):
    import string
    return string.ascii_lowercase[:length]


mycli = CLI(cli_name='jdp', commands_loader_cls = JdpCommandsLoader)
exit_code = mycli.invoke(sys.argv[1:])
sys.exit(exit_code)
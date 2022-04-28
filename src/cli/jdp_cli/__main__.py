import sys
from knack import CLI
from .commands_loader import JdpCommandsLoader

jdp_cli = CLI(cli_name='jdp', commands_loader_cls = JdpCommandsLoader)
exit_code = jdp_cli.invoke(sys.argv[1:])
sys.exit(exit_code)

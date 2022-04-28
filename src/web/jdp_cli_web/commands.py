# from uuid import uuid4
from knack import ArgumentsContext
from knack.commands import CommandGroup
from knack.log import get_logger

import jdp_cli_web.help
from .validators import *

logger = get_logger(__name__)

def create_example(name):
    return "This is create example."

def show_example(name):
    return "This is show example."

def load_commands(cmd_loader):
    with CommandGroup(cmd_loader, 'example', 'jdp_cli_web#{}') as g:
        g.command('create', 'create_example')
        g.command('show', 'show_example')

def load_arguments(cmd_loader):
        
    with ArgumentsContext(cmd_loader, 'example create') as ac:
        ac.argument('name',
            options_list=['--name', '-n'],
            help='Name of the example',
            validator=validate_name,
            type=str.lower)
    
    with ArgumentsContext(cmd_loader, 'example show') as ac:
        ac.argument('name',
            options_list=['--name', '-n'],
            help='Name of the example',
            type=str.lower)

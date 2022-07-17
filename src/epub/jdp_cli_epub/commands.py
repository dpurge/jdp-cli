# from uuid import uuid4
from knack import ArgumentsContext
from knack.commands import CommandGroup
from knack.log import get_logger

import jdp_cli_epub.help
from .validators import *

logger = get_logger(__name__)

def load_commands(cmd_loader):
    with CommandGroup(cmd_loader, 'epub', 'jdp_cli_epub#{}') as g:
        g.command('build-project', 'cmd_build_project')
        g.command('get-vocabulary', 'cmd_get_vocabulary')

def load_arguments(cmd_loader):
        
    with ArgumentsContext(cmd_loader, 'epub build-project') as ac:
        ac.argument('config',
            options_list=['--config', '-c'],
            help='Path to book project file',
            validator=validate_config,
            type=str)
    
    with ArgumentsContext(cmd_loader, 'epub get-vocabulary') as ac:
        ac.argument('book',
            options_list=['--book', '-b'],
            help='Path to book file',
            validator=validate_book,
            type=str)
        ac.argument('filename',
            options_list=['--filename', '-f'],
            help='Name of the output file',
            validator=validate_filename,
            type=str)

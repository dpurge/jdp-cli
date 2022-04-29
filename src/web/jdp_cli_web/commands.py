# from uuid import uuid4
from knack import ArgumentsContext
from knack.commands import CommandGroup
from knack.log import get_logger

import jdp_cli_web.help
from .validators import *

logger = get_logger(__name__)

def load_commands(cmd_loader):
    with CommandGroup(cmd_loader, 'web', 'jdp_cli_web#{}') as g:
        g.command('get-text', 'cmd_get_text')
        g.command('get-words', 'cmd_get_words')

def load_arguments(cmd_loader):
        
    with ArgumentsContext(cmd_loader, 'web get-text') as ac:
        ac.argument('uri',
            options_list=['--uri', '-u'],
            help='Web page URI',
            validator=validate_uri,
            type=str)
    
    with ArgumentsContext(cmd_loader, 'web get-words') as ac:
        ac.argument('uri',
            options_list=['--uri', '-u'],
            help='Web page URI',
            validator=validate_uri,
            type=str)

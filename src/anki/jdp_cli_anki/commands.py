# from uuid import uuid4
from knack import ArgumentsContext
from knack.commands import CommandGroup
from knack.log import get_logger

import jdp_cli_anki.help
from .validators import *

logger = get_logger(__name__)

def load_commands(cmd_loader):
    with CommandGroup(cmd_loader, 'anki', 'jdp_cli_anki#{}') as g:
        g.command('build-project', 'cmd_build_project')
        g.command('get-data', 'cmd_get_data')

def load_arguments(cmd_loader):
        
    with ArgumentsContext(cmd_loader, 'anki build-project') as ac:
        ac.argument('project',
            options_list=['--project', '-p'],
            help='Path to Anki package project file',
            validator=validate_project,
            type=str)
    
    with ArgumentsContext(cmd_loader, 'anki get-data') as ac:
        ac.argument('anki_package',
            options_list=['--anki-package', '-a'],
            help='Path to Anki package file',
            validator=validate_anki_package,
            type=str)
        ac.argument('output',
            options_list=['--output', '-o'],
            help='Path to the output file',
            validator=validate_output,
            type=str)
        ac.argument('output_format',
            options_list=['--output-format', '-f'],
            help='Format of the output file',
            validator=validate_output_format,
            type=str)

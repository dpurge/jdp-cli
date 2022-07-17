from .lib_get_project_config import lib_get_project_config

import pprint

def cmd_build_project(config='jdp-book.toml'):
    cfg = lib_get_project_config(config=config)
    pprint.pprint(cfg)

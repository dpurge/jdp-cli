import os
import tomli

from pathlib import Path
from knack.util import CLIError
from jdp_cli.lib_cli_tools import push_directory
from pydantic.dataclasses import dataclass
from pydantic import validator, ValidationError
from typing import List

@dataclass
class ModelField:
    name: str
    markdown: bool
    template: Path

    @validator('template')
    def check_file_exists(cls, filename):
        if not filename.is_file():
            raise CLIError(f'Field template file does not exist: {filename.resolve()}')
        return filename.resolve()

@dataclass
class ModelTemplate:
    name: str
    qfmt: Path
    afmt: Path

    @validator('qfmt', 'afmt')
    def check_file_exists(cls, filename):
        if not filename.is_file():
            raise CLIError(f'Model template file does not exist: {filename.resolve()}')
        return filename.resolve()

@dataclass
class DeckSection:
    id: int
    name: str

@dataclass
class ModelSection:
    id: int
    name: str
    type: str
    guid: List[str]
    styles: Path
    templates: List[ModelTemplate]
    fields: List[ModelField]

    @validator('type')
    def check_type(cls, type):
        types = 'front-back', 'cloze'
        if not type in types:
            raise CLIError(f'Model type "{type}" not in allowed types: {", ".join(types)}')
        return type

    @validator('styles')
    def check_file_exists(cls, filename):
        if not filename.is_file():
            raise CLIError(f'Model stylesheet file does not exist: {filename.resolve()}')
        return filename.resolve()

@dataclass
class ProjectData:
    filename: Path
    tags: List[str]

    @validator('filename')
    def check_file_exists(cls, filename):
        if not filename.is_file():
            raise CLIError(f'Data file does not exist: {filename.resolve()}')
        return filename.resolve()


@dataclass
class AnkiProject:
    project: Path
    filename: Path
    deck: DeckSection
    model: ModelSection
    data: List[ProjectData]
    audio: List[Path]
    video: List[Path]
    image: List[Path]


    @validator('project')
    def check_file_exists(cls, filename):
        if not filename.is_file():
            raise CLIError(f'Project file does not exist: {filename.resolve()}')
        return filename.resolve()

    @validator('filename')
    def check_filename(cls, filename):
        return filename.resolve()

    @validator('audio', 'video', 'image')
    def check_filelist(cls, filelist):
        for filename in filelist:
            if not filename.is_file():
                raise CLIError(f'Media file does not exist: {filename.resolve()}')
        return [filename.resolve() for filename in filelist]

def get_anki_project(config):
    config_path = Path(config).absolute()
    if not config_path.is_file():
        raise CLIError(f'Project configuration file does not exist: {config_path}')
    
    try:
        with open(config, 'rb') as c:
            data = tomli.load(c)
    except Exception as e:
        raise CLIError(f'Cannot parse project configuration: {e}')

    try:
        with push_directory(config_path.parent):
            cfg = AnkiProject(project=config_path, **data)
    except ValidationError as e:
        raise CLIError(f'Error validating project configuration: {e}')

    return cfg

import os
import tomli

from pathlib import Path
from pydantic import validator, ValidationError
from pydantic.dataclasses import dataclass
from typing import List
from knack.util import CLIError
# from .lib_epub_tools import push_directory
from jdp_cli.lib_cli_tools import push_directory

@dataclass
class EpubSection:
    head: Path
    text: List[Path]

@dataclass
class EpubProject:
    project: Path
    filename: Path
    title: str
    identifier: str
    language: str
    cover: Path
    template: Path
    author: List[str]
    stylesheet: List[Path]
    font: List[Path]
    image: List[Path]
    section: List[EpubSection]

    @validator('project')
    def check_project(cls, project):
        if not project.is_file():
            raise CLIError(f'Project path does not exist: {project.resolve()}')
        return project.resolve()

    @validator('filename')
    def check_filename(cls, filename):
        return filename.resolve()

    @validator('cover')
    def check_file_exists(cls, filename):
        if not filename.is_file():
            raise CLIError(f'File does not exist: {filename.resolve()}')
        return filename.resolve()

    @validator('stylesheet', 'font', 'image')
    def check_files_exist(cls, filenames):
        for filename in filenames:
            if not filename.is_file():
                raise CLIError(f'File does not exist: {filename.resolve()}')
        filenames = [i.resolve() for i in filenames]
        return filenames

    @validator('section')
    def check_sections(cls, sections):
        for section in sections:
            if not section.head.is_file():
                raise CLIError(f'File does not exist: {section.head.resolve()}')

            for text in section.text:
                if not text.is_file():
                    raise CLIError(f'File does not exist: {text.resolve()}')

            section.head = section.head.resolve()
            section.text = [i.resolve() for i in section.text]

        return sections

    @validator('template')
    def check_directory_exists(cls, directory):
        if not directory.is_dir():
            raise CLIError(f'Directory does not exist: {directory}')
        return directory

    # @validator('language')
    # def check_language(cls, language):
    #     return language

def get_epub_project(config):
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
            cfg = EpubProject(project=config_path, **data)
    except ValidationError as e:
        raise CLIError(f'Error validating project configuration: {e}')

    return cfg

import tomli

from pathlib import Path
from pydantic import BaseModel, validator, ValidationError
from typing import List
from knack.util import CLIError

class ProjectConfig(BaseModel):
    project: Path
    title: str
    identifier: str
    filename: str
    language: str
    template: str
    stylesheet: List[str]
    font: List[str]
    image: List[str]
    text: List[str]

    @validator('filename')
    def check_filename(cls, filename):
        return filename

    @validator('language')
    def check_language(cls, language):
        return language

def lib_get_project_config(config):
    config_path = Path(config)
    if not config_path.is_file():
        raise CLIError(f'Project configuration file does not exist: {config_path}')
    
    try:
        with open(config, 'rb') as c:
            data = tomli.load(c)
    except Exception as e:
        raise CLIError(f'Cannot parse project configuration: {e}')

    try:
        cfg = ProjectConfig(project=config_path, **data)
    except ValidationError as e:
        raise CLIError(f'Error validating project configuration: {e}')

    return cfg

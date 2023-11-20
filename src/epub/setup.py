from importlib.metadata import entry_points
from setuptools import setup, find_packages
from pathlib import Path

current_dir = Path(__file__).parent.resolve()

VERSION = "0.0.1"
DESCRIPTION = ''
README = (current_dir / "README.md").read_text(encoding="utf-8")
HISTORY = (current_dir / "HISTORY.md").read_text(encoding="utf-8")


CLASSIFIERS = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.10',
]

DEPENDENCIES = [
    'knack',
    'EbookLib',
    'Jinja2',
    'tomli',
    'pydantic',
    'PyYAML',
    'Markdown',
    'markdown-full-yaml-metadata'
]

setup (
    name = "jdp-cli-epub",
    version = VERSION,
    description = DESCRIPTION,
    long_description = README + '\n\n' + HISTORY,
    long_description_content_type="text/markdown",
    classifiers = CLASSIFIERS,
    packages = find_packages(),
    python_requires = ">=3.10, <4",
    install_requires = DEPENDENCIES,
    setup_requires=['wheel'],
    entry_points = {
        'jdp_cli.commands': [
            'epub = jdp_cli_epub'
        ]
    }
)

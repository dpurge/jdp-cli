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
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
]

DEPENDENCIES = [
    "knack"
]

setup (
    name = "jdp-cli",
    version = VERSION,
    description = DESCRIPTION,
    long_description = README + '\n\n' + HISTORY,
    long_description_content_type="text/markdown",
    classifiers = CLASSIFIERS,
    packages = find_packages(),
    python_requires = ">=3.7, <4",
    install_requires = DEPENDENCIES,
    setup_requires=['wheel'],
    entry_points = {
        "console_scripts": [
            "jdp=jdp_cli:main",
        ]
    }
)

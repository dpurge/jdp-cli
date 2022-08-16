from knack.help_files import helps  # pylint: disable=unused-import

helps['epub'] = """
    type: group
    short-summary: Commands for working with JDP ePub files.
"""

helps['epub build-project'] = """
    type: command
    short-summary: Build JDP ePub project.
    examples:
        - name: Build default project file jdp-book.toml
          text: jdp epub build-project
        - name: Build custom project file
          text: jdp epub build-project --config my-book.toml
        - name: Build default project file jdp-book.toml to the output file
          text: jdp epub build-project --output my-book.epub
"""

helps['epub get-vocabulary'] = """
    type: command
    short-summary: Extract vocabulary from JDP ePub file.
    examples:
        - name: Extract vocabulary to console
          text: jdp epub get-vocabulary --book my-book.epub
        - name: Extract vocabulary to a tab-separated file
          text: jdp epub get-vocabulary --book my-book.epub --filename my-book.csv
        - name: Extract vocabulary to a json file
          text: jdp epub get-vocabulary --book my-book.epub --filename my-book.json
"""

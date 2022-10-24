from knack.help_files import helps  # pylint: disable=unused-import

helps['anki'] = """
    type: group
    short-summary: Commands for working with Anki files.
"""

helps['anki build-project'] = """
    type: command
    short-summary: Build JDP Anki project.
    examples:
        - name: Build default project file jdp-apkg.toml
          text: jdp anki build-project
        - name: Build custom project file
          text: jdp anki build-project --config my-anki.toml
        - name: Build default project file jdp-apkg.toml to the output file
          text: jdp epub build-project --filename my-flashcards.epub
        - name: Build default project file jdp-apkg.toml to the output directory
          text: jdp epub build-project --directory ./out
"""

helps['anki get-data'] = """
    type: command
    short-summary: Extract data from JDP Anki file.
    examples:
        - name: extract data to console
          text: jdp anki get-data --anki-package my-package.apkg
        - name: extract data to a tab-separated file
          text: jdp anki get-data --anki-package my-package.apkg --output my-package.csv
        - name: extract data to a json file
          text: jdp anki get-data --anki-Package my-package.apkg --output my-package.json --format json
"""

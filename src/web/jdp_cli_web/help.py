from knack.help_files import helps  # pylint: disable=unused-import

helps['web'] = """
    type: group
    short-summary: Commands for working with web resources.
"""

helps['web get-text'] = """
    type: command
    short-summary: Get text content from web page
    examples:
        - name: Get text from web page
          text: jdp web get-text --uri http://example.com/
"""

helps['web show'] = """
    type: command
    short-summary: Example show command.
    examples:
        - name: Display example
          text: jdp web show --name EXAMPLE
"""

from knack.help_files import helps  # pylint: disable=unused-import

helps['example'] = """
    type: group
    short-summary: Example commands.
"""

helps['example create'] = """
    type: command
    short-summary: Example create command.
    examples:
        - name: Create example
          text: jdp example create --name EXAMPLE
"""

helps['example show'] = """
    type: command
    short-summary: Example show command.
    examples:
        - name: Display example
          text: jdp example show --name EXAMPLE
"""

import re
from knack.util import CLIError

def validate_name(namespace):
    if not re.match('^[a-z][a-z0-9]{0,9}$', namespace.name.lower()):
        raise CLIError('Name limited to 10 characters. Can only contain letters and numbers, and must start with a letter')

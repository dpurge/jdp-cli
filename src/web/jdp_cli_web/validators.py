import re
from knack.util import CLIError

def validate_uri(namespace):
    if not re.match('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', namespace.uri):
        raise CLIError('Please provide http://... or https://... uri')

def validate_name(namespace):
    if not re.match('^[a-z][a-z0-9]{0,9}$', namespace.name.lower()):
        raise CLIError('Name limited to 10 characters. Can only contain letters and numbers, and must start with a letter')

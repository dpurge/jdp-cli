import json
import yaml
import csv
import frontmatter

from knack.util import CLIError

def get_csv_data(filepath):
    with filepath.open(mode="r", encoding="utf-8") as f:
        records = csv.DictReader(f, delimiter="\t")
        for data in records:
            yield data


def get_markdown_data(filepath):
    with filepath.open(mode="r", encoding="utf-8") as f:
        fm = frontmatter.load(f)

    if not 'fields' in fm.keys():
        raise CLIError(f'File does not specify fields in the metadata: {filepath}')

    fields = fm.get('fields')
    content = fm.content

    for record in content.split("\n\n***\n\n"):
        values = [i.strip() for i in record.split("\n\n---\n\n")]
        yield dict(zip(fields,values))


def get_json_data(filepath):
    with filepath.open(mode="r", encoding="utf-8") as f:
        records = json.load(f)
    for data in records:
        yield data


def get_yaml_data(filepath):
    with filepath.open(mode="r", encoding="utf-8") as f:
        records = yaml.safe_load(f)
    for data in records:
        yield data

data_readers = {
    '.csv' : get_csv_data,
    '.md'  : get_markdown_data,
    '.json': get_json_data,
    '.yaml': get_yaml_data
}

def get_anki_data(filepath):
    suffix = filepath.suffix

    if not suffix in data_readers:
        raise CLIError(f'Cannot read data from file with extension: {suffix}')
        
    reader = data_readers.get(suffix)
    for data in reader(filepath):
        yield data

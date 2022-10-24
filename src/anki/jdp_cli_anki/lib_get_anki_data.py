import json
import yaml
import csv

from knack.util import CLIError

def get_csv_data(filepath):
    with filepath.open(mode="r", encoding="utf-8") as f:
        records = csv.DictReader(f, delimiter="\t")
        for data in records:
            yield data


def get_markdown_data(filepath):
    with filepath.open(mode="r", encoding="utf-8") as f:
        contents = f.read()
    for record in contents.split("\n---\n"):
        data = record.strip()
        yield data


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
    '.csv': get_csv_data,
    '.md': get_markdown_data,
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

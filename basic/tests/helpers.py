import json


def get_fixture(path_to_file):
    with open(f'basic/tests/fixtures/{path_to_file}') as json_file:
        data = json.load(json_file)

    return data

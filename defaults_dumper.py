#!/usr/bin/env python

import json
import sys


def parse_args(args):
    if len(args) < 2:
        sys.exit('expecting a single argument, the file to process')

    file_path = args[1]
    return file_path


def get_json(file_path):
    with open(file_path, 'r') as f:
        contents = f.read()
    return json.loads(contents)


def collect_role_variables(top_level_json):
    variable_map = {}
    roles = top_level_json['roles']
    for role, values in roles.items():
        var_list = None
        if values['defaults']:
            var_list = values['defaults'].keys()
        variable_map[role] = var_list

    return variable_map


def output_variables(variable_map):
    print(json.dumps(variable_map))


def main(args):
    file_path = parse_args(args)
    top_json = get_json(file_path)
    var_map = collect_role_variables(top_json)
    output_variables(var_map)

if __name__ == '__main__':
    main(sys.argv)

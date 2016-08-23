#!/usr/bin/env python
import difflib
import json
import sys


def parse_args(args):
    if len(args) < 3:
        print("Need 2 arguments: var_differ.py file1.json file2.json")
        raise SystemExit

    return sys.argv[1], sys.argv[2]


def get_json(file_path):
    with open(file_path, 'r') as f:
        contents = f.read()
    return json.loads(contents)


def opposite_diff(file_name):
    options = {
        '+': '-',
        '-': '+',
    }

    for current, opposite in options.items():
        if file_name.startswith(current):
            return file_name.replace(current, opposite)


def compare_role_variables(before, after):
    all_role_names = []
    all_role_names.extend(before.keys())
    all_role_names.extend(after.keys())

    # Make sure we only have unique keys.
    all_role_names = set(all_role_names)

    different_vars = {}

    for role_name in all_role_names:
        before_list = before.get(role_name, [])
        after_list = after.get(role_name, [])

        different_vars.setdefault(role_name, [])

        # If both lists are empty, difflib breaks.
        if not before_list and not after_list:
            continue

        diff = difflib.ndiff(before_list, after_list)

        for var in diff:
            if var.startswith('+') or var.startswith('-'):

                # Look for vars that might have just been moved and
                # leave them out of the diff.
                opposite = opposite_diff(var)
                if opposite in different_vars[role_name]:
                    different_vars[role_name].remove(opposite)
                    continue

                # Remove lines that were just moved.
                different_vars[role_name].append(var)

    return different_vars


def output_diff(diffed_vars):
    print(json.dumps(diffed_vars, indent=2))


def main(args):
    before_filepath, after_filepath = parse_args(args)

    before_json = get_json(before_filepath)
    after_json = get_json(after_filepath)

    # TODO(nolanb/palendae): compare roles present in one branch vs another
    diffed_vars = compare_role_variables(before_json, after_json)

    output_diff(diffed_vars)


if __name__ == '__main__':
    main(sys.argv)

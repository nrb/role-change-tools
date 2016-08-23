import json
import sys


def main(filename):
    with open(filename, 'r') as f:
        contents = f.read()

    roles = json.loads(contents)

    for name, changes in roles.items():
        print(name)
        print("File: playbooks/roles/{}/defaults/main.yml".format(name))

        if not changes:
            print('\tNo changes')
            continue

        removals, adds = [], []

        for change in changes:
            if change.startswith('-'):
                removals.append(change[2:])
            elif change.startswith('+'):
                adds.append(change[2:])

        print('\tRemoved variables:')

        if not removals:
            print('\t\tNone removed.')
        else:
            for item in removals:
                print('\t\t{}'.format(item))

        print('\tAdded variables:')

        if not adds:
            print('\t\tNone added.')
        else:
            for item in adds:
                print('\t\t{}'.format(item))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Requires a file name as an argument.")

    main(sys.argv[1])

These are quickly thrown together tools to help with diffing between two versions of ansible role variables.

var_differ.py will take 2 JSON files and produce a diff of the structures.

defaults_dumper.py will dump a list of the default variables within a role suitable for piping in to var_differ.py.


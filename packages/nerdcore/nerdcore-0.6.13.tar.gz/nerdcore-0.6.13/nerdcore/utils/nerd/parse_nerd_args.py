from typing import List, Tuple, Dict

from nerdcore.help.help import run_default_help


def split_unknown_args(unknown_args: List[str]) -> Tuple[Dict[str, bool], List[str]]:
    from collections import OrderedDict
    unknown_named_args = OrderedDict()
    unknown_unnamed_args = []

    iterator = iter(unknown_args)
    for arg in iterator:
        if arg.startswith('--') or arg.startswith('-'):
            if "=" in arg:
                key, value = arg.split("=", 1)  # Split on the first "="
            else:
                key = arg
                try:
                    value = next(iterator)
                    if value.startswith('--') or value.startswith('-'):
                        unknown_unnamed_args.append(value)
                        value = True
                except StopIteration:
                    value = True
            unknown_named_args[key] = value
        else:
            unknown_unnamed_args.append(arg)

    return unknown_named_args, unknown_unnamed_args


def parse_nerd_args():
    import argparse

    # Create argument parser - use custom help
    parser = argparse.ArgumentParser(add_help=False)

    # Special flags - flags that override normal behaviors significantly.
    parser.add_argument('--toggle-light-mode', action='store_true')

    # Action flags - mutually exclusive, overrides default of "run"
    action_flags = parser.add_mutually_exclusive_group()
    action_flags.add_argument('-e', '--edit', action='store_true')
    action_flags.add_argument('-h', '--help', action='store_true')

    # Entity Type flags - mutually exclusive, overrides default of "command"
    entity_type_flags = parser.add_mutually_exclusive_group()
    entity_type_flags.add_argument('-d', '--deployment', action='store_true')

    # Entity is the name of the command or overridden entity_type
    parser.add_argument('entity_name', nargs='?')

    # Parse Arguments
    nerd_args, unknown_args = parser.parse_known_args()

    # Split unknown arguments into named and unnamed
    named_args, unnamed_args = split_unknown_args(unknown_args)

    # Action
    action = 'run'
    if nerd_args.edit is True:
        action = 'edit'
    elif nerd_args.help is True:
        action = 'help'

    # Entity Type
    entity_type = 'command'
    if action == 'help':
        entity_type = 'help'
    elif nerd_args.deployment is True:
        entity_type = 'deployment'

    if entity_type in ['help', 'command'] and nerd_args.entity_name in [None, 'help']:
        run_default_help()

    return nerd_args, named_args, unnamed_args, action, nerd_args.entity_name, entity_type

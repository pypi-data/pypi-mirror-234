import argparse
from tketool.mlsample.SampleSet_Util import *
from tketool.cmd_utils import *

def main():
    parser = argparse.ArgumentParser(description="A simple command line tool")
    commands = {}

    # Only create subparsers once
    subparsers = parser.add_subparsers(dest="command", help='Commands')

    add_cmd(subparsers, set_list, commands)  # Add your functions here
    add_cmd(subparsers, set_info, commands)
    add_cmd(subparsers, delete_set, commands)
    add_cmd(subparsers, set_data_info, commands)
    add_cmd(subparsers, capture_str, commands)
    add_cmd(subparsers, upload, commands)
    add_cmd(subparsers, download, commands)

    args = parser.parse_args()

    if args.command in commands:
        command_params = inspect.signature(commands[args.command]).parameters
        params = {name: getattr(args, name, None) for name in command_params}
        commands[args.command](**params)
    else:
        parser.print_help()

import argparse
from tketool.cmd_utils import *
from tketool.lmc.tasks.translate import *
from tketool.lmc.tasks.code_review import *
from tketool.lmc.prompt_utils import *


def main():
    parser = argparse.ArgumentParser(description="A simple command line tool")
    commands = {}

    # Only create subparsers once
    subparsers = parser.add_subparsers(dest="command", help='Commands')

    add_cmd(subparsers, update_prompt_folder, commands)
    add_cmd(subparsers, codereview, commands)

    args = parser.parse_args()

    if args.command in commands:
        command_params = inspect.signature(commands[args.command]).parameters
        params = {name: getattr(args, name, None) for name in command_params}
        commands[args.command](**params)
    else:
        parser.print_help()

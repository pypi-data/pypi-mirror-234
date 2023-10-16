import inspect, re
from inspect import Parameter


def get_help_info(command_func):
    """Extract parameters help info from function's docstring."""
    doc = inspect.getdoc(command_func)
    if not doc:
        return {}
    pattern = re.compile(r"(\w+)\s*:(.*)")
    matches = pattern.findall(doc)
    helps = {match[0]: match[1].strip() for match in matches}
    return helps


def add_cmd(subparsers, command_func, command_dict):
    cmd_str = command_func.__name__
    doc_lines = command_func.__doc__.strip().split("\n") if command_func.__doc__ else []
    help_info = doc_lines[0] if doc_lines else None

    sig = inspect.signature(command_func)
    arguments_list = []

    param_helps = get_help_info(command_func)

    for name, param in sig.parameters.items():
        # default value and required flag handling
        if param.default == Parameter.empty:
            required = True
            default = None
        else:
            required = False
            default = param.default

        help_param = param_helps.get(name, "")
        arg_type = type(default) if default is not None else str
        single_char = name[0]  # Use the first character of the parameter name

        if name != "self":  # Prevent self from being added as an argument
            arguments_list.append((f'--{name}', f'-{single_char}', arg_type, required, help_param, default))

    cmd_parser = subparsers.add_parser(cmd_str, help=help_info)

    for arg in arguments_list:
        # include default value while adding argument
        cmd_parser.add_argument(arg[1], arg[0], type=arg[2], required=arg[3], help=arg[4], default=arg[5])

    command_dict[cmd_str] = command_func
